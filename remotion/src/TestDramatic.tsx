import React from 'react';
import { AbsoluteFill } from 'remotion';
import { HeroFullBleed } from './components/dramatic_layouts';

export const TestDramatic: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: '#1A1A2E' }}>
      <HeroFullBleed
        kicker="RIYADH · COFFEE"
        headline="أفضل قهوة في الرياض"
        businessName="قهوة الصباح"
        taglines={["حبوب مختارة بعناية", "تحميص طازج يومياً", "جلسة هادئة"]}
        ctaText="زورونا اليوم"
        rating={4.8}
        ratingCount={215}
        hashtags={["#قهوة_الرياض"]}
        trustBadge="مختارة بعناية"
        photoPath="photos/cafes.jpg"
      />
    </AbsoluteFill>
  );
};
