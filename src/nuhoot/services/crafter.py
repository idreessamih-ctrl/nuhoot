"""Crafter service — AI pitch generation via GLM 5.2.

Generates personalized Arabic WhatsApp pitches and 3 sample Instagram post
captions for businesses, using the GLM 5.2 model via the umans.ai
OpenAI-compatible API.

Pipeline:
    Business (investigated) → GLM 5.2 prompt → Pitch (draft) → stored in DB

Every pitch includes a PDPL opt-out clause for Saudi data law compliance.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import structlog
from sqlalchemy.orm import Session

from nuhoot.config import settings
from nuhoot.models.business import Business
from nuhoot.models.pitch import Pitch

logger = structlog.get_logger()

_DEFAULT_TIMEOUT = 30.0
_AI_TEMPERATURE = 0.7

# PDPL compliance — opt-out text appended to every pitch (Saudi data law).
_PDPL_OPT_OUT = "لإلغاء الاشتراك، أرسل إيقاف"

_SYSTEM_PROMPT = (
    "أنت خبير تسويق رقمي تعمل في وكالة تسويق سعودية متخصصة. "
    "مهمتك إنشاء رسائل تسويقية شخصية باللغة العربية للشركات السعودية. "
    "اكتب رسالة احترافية ومخصصة تتضمن: تحية شخصية باسم الشركة، "
    "مقدمة موجزة عن الوكالة، تحليل الحضور الرقمي للشركة، "
    "عرض القيمة المقترحة، ودعوة لجدولة مكالمة. "
    "يجب أن تكون الرسالة باللغة العربية الفصحى المبسطة."
)

_USER_PROMPT_TEMPLATE = (
    "أنشئ محتوى تسويقياً للشركة التالية:\n\n"
    "اسم الشركة: {name}\n"
    "التصنيف: {category}\n"
    "العنوان: {address}\n"
    "التقييم: {rating}\n"
    "عدد المراجعات: {review_count}\n"
    "لديها موقع إلكتروني: {has_website}\n"
    "لديها حساب انستغرام: {has_instagram}\n"
    "نتيجة SEO: {seo_score}\n"
    "نتيجة الحضور الاجتماعي: {social_score}\n\n"
    "أرجع النتيجة بصيغة JSON تحتوي على:\n"
    '- "pitch": رسالة واتساب تسويقية شخصية باللغة العربية تبدأ بتحية باسم الشركة\n'
    '- "sample_posts": قائمة بـ 3 منشورات انستغرام مع هاشتاقات'
)


class CrafterError(Exception):
    """Raised when the Crafter service encounters an unrecoverable error."""


class CrafterService:
    """Generate AI-crafted pitches via GLM 5.2.

    Usage::

        service = CrafterService(db_session)
        pitch = service.craft_pitch(business)
    """

    def __init__(self, db: Session, *, timeout: float = _DEFAULT_TIMEOUT) -> None:
        self.db = db
        self.timeout = timeout

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def craft_pitch(self, business: Business) -> Pitch:
        """Generate a personalized pitch for *business* using GLM 5.2.

        Args:
            business: The investigated Business to craft a pitch for.

        Returns:
            The stored Pitch object with pitch_text and sample_posts.

        Raises:
            CrafterError: If the AI API call fails or the response is invalid.
        """
        logger.info(
            "crafter.craft.start",
            business_id=business.id,
            name=business.name,
        )

        system_prompt = _SYSTEM_PROMPT
        user_prompt = self._build_user_prompt(business)

        content = self._call_ai(system_prompt, user_prompt)
        pitch_text, sample_posts = self._parse_response(content)

        # Ensure PDPL compliance — opt-out text must always be present.
        pitch_text = self._ensure_pdpl_opt_out(pitch_text)

        pitch = Pitch(
            business_id=business.id,
            pitch_text=pitch_text,
            sample_posts=sample_posts,
            language="ar",
            status="draft",
        )
        self.db.add(pitch)
        self.db.commit()
        self.db.refresh(pitch)

        logger.info(
            "crafter.craft.done",
            pitch_id=pitch.id,
            business_id=business.id,
        )
        return pitch

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_user_prompt(self, business: Business) -> str:
        """Build the user prompt with business investigation data."""
        return _USER_PROMPT_TEMPLATE.format(
            name=business.name,
            category=business.category,
            address=business.address or "غير متوفر",
            rating=business.rating if business.rating is not None else "غير متوفر",
            review_count=business.review_count if business.review_count is not None else 0,
            has_website="نعم" if business.has_website else "لا",
            has_instagram="نعم" if business.has_instagram else "لا",
            seo_score=business.seo_score if business.seo_score is not None else "غير متوفر",
            social_score=(
                business.social_score if business.social_score is not None else "غير متوفر"
            ),
        )

    def _call_ai(self, system_prompt: str, user_prompt: str) -> str:
        """Call the GLM 5.2 chat completions API and return the content.

        Raises:
            CrafterError: On timeout, HTTP error, or other request failure.
        """
        url = f"{settings.ai_base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.umans_api_key}",
            "Content-Type": "application/json",
        }
        body: dict[str, Any] = {
            "model": settings.ai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": _AI_TEMPERATURE,
        }

        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(url, json=body, headers=headers)
                response.raise_for_status()
                data: Any = response.json()
        except httpx.TimeoutException as exc:
            raise CrafterError(
                f"AI request timed out after {self.timeout}s",
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise CrafterError(
                f"AI API returned HTTP {exc.response.status_code}",
            ) from exc
        except httpx.HTTPError as exc:
            raise CrafterError(f"AI request failed: {exc}") from exc

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise CrafterError("AI response missing expected content field") from exc

        if not isinstance(content, str):
            raise CrafterError("AI response content is not a string")

        return content

    def _parse_response(self, content: str) -> tuple[str, list[str]]:
        """Parse the AI content JSON into (pitch_text, sample_posts).

        Raises:
            CrafterError: If the content is not valid JSON or missing fields.
        """
        try:
            parsed: Any = json.loads(content)
        except json.JSONDecodeError as exc:
            raise CrafterError(f"Failed to parse AI response as JSON: {exc}") from exc

        if not isinstance(parsed, dict):
            raise CrafterError("AI response is not a JSON object")

        pitch_text = parsed.get("pitch")
        if not pitch_text or not isinstance(pitch_text, str):
            raise CrafterError("AI response missing 'pitch' field")

        sample_posts = parsed.get("sample_posts")
        if not isinstance(sample_posts, list):
            raise CrafterError("AI response missing 'sample_posts' list")

        return pitch_text, list(sample_posts)

    def _ensure_pdpl_opt_out(self, pitch_text: str) -> str:
        """Append the PDPL opt-out text if not already present."""
        if _PDPL_OPT_OUT not in pitch_text:
            return f"{pitch_text}\n\n{_PDPL_OPT_OUT}"
        return pitch_text
