// ─────────────────────────────────────────────────────────────────────
// SOCIAL — Social media icons and contact bar
//   SocialBar · row of social media platform icons
//   ContactRow · phone + location + hours row
//
// Source: react-social-icons (MIT — see docs/ATTRIBUTIONS.md)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import { BaseBlockProps, ColorConfig, FONTS, hexRgba, useColors } from './helpers';
import { Icon } from './icon';

// ─── SocialBar ────────────────────────────────────────────────────────
export interface SocialBarProps extends BaseBlockProps {
  /** Platforms to show. Default: whatsapp, instagram, snapchat, tiktok. */
  platforms?: string[];
  /** Icon size. Default 32. */
  iconSize?: number;
  /** Gap between icons. Default 12. */
  gap?: number;
  align?: 'right' | 'left' | 'center';
}

// SVG paths for social media icons (simplified, MIT/CC0)
const SOCIAL_ICONS: Record<string, string> = {
  whatsapp: 'M12 2C6.5 2 2 6.5 2 12c0 1.8.5 3.5 1.3 5L2 22l5.2-1.4c1.4.8 3.1 1.2 4.8 1.2 5.5 0 10-4.5 10-10S17.5 2 12 2zm5.3 14.3c-.2.6-1.3 1.2-1.8 1.2-.5.1-1 .1-1.7-.1-.4-.1-.9-.3-1.5-.5-2.7-1.2-4.4-3.9-4.6-4.1-.1-.2-1-1.4-1-2.6s.6-1.8.9-2.1c.2-.2.5-.3.7-.3h.5c.2 0 .4 0 .6.5l.8 2c.1.2.1.4 0 .6l-.4.6c-.2.2-.3.4-.1.7.2.3.9 1.4 1.9 2.3 1.3 1.1 2.4 1.5 2.7 1.6.3.1.5.1.6-.1l.7-.9c.2-.2.4-.2.6-.1l1.9.9c.2.1.4.2.4.3.1.1.1.5-.1 1.1z',
  instagram: 'M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.3 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.3 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.3 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .3-2.2.4-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.3-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.3-1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.9c.1-1.2.3-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.3 2.2-.4C8.4 2.2 8.8 2.2 12 2.2zm0 3.2c-3.4 0-6.6 2.8-6.6 6.6s2.8 6.6 6.6 6.6 6.6-2.8 6.6-6.6-2.8-6.6-6.6-6.6zm0 10.8c-2.3 0-4.2-1.9-4.2-4.2s1.9-4.2 4.2-4.2 4.2 1.9 4.2 4.2-1.9 4.2-4.2 4.2zm6.9-10.9c0 .8-.6 1.4-1.4 1.4s-1.4-.6-1.4-1.4.6-1.4 1.4-1.4 1.4.6 1.4 1.4z',
  snapchat: 'M12 2c-1.5 0-3 .5-4 1.5-1-1-2.5-1.5-4-1.5C2 2 .5 3.5.5 5.5c0 2 1 3.5 2.5 5-.5 1.5-1.5 3-1.5 4.5 0 2 1.5 3.5 3.5 3.5.5 0 1 0 1.5-.5.5 1 1.5 2 3 2s2.5-1 3-2c.5.5 1 .5 1.5.5 2 0 3.5-1.5 3.5-3.5 0-1.5-1-3-1.5-4.5 1.5-1.5 2.5-3 2.5-5 0-2-1.5-3.5-3.5-3.5z',
  tiktok: 'M16 2c.3 2.2 1.5 4 3.5 4.5v3c-1.3 0-2.5-.3-3.5-.9v6.4c0 3.6-2.9 6.5-6.5 6.5S3 18.6 3 15s2.9-6.5 6.5-6.5c.5 0 1 .1 1.5.2v3.2c-.5-.2-1-.3-1.5-.3-1.9 0-3.5 1.6-3.5 3.5s1.6 3.5 3.5 3.5 3.5-1.6 3.5-3.5V2h3z',
  x: 'M18 2h3l-7 8 8 12h-6l-5-7-5 7H3l8-9L3 2h6l4 6 5-6z',
  youtube: 'M23 7.5c-.3-1.2-1-2-2.2-2.3C18.8 5 12 5 12 5s-6.8 0-8.8.2C2 5.5 1.3 6.3 1 7.5.8 9.5.8 12 .8 12s0 2.5.2 4.5c.3 1.2 1 2 2.2 2.3C5.2 19 12 19 12 19s6.8 0 8.8-.2c1.2-.3 2-1.1 2.2-2.3.2-2 .2-4.5.2-4.5s0-2.5-.2-4.5zM10 15V9l5 3-5 3z',
  telegram: 'M22 3L2 11l5 2 2 6 3-4 5 4 5-16zM9 13l6-5-5 6v3l-1-4z',
};

export const SocialBar: React.FC<SocialBarProps> = ({
  platforms = ['whatsapp', 'instagram', 'snapchat', 'tiktok'],
  iconSize = 32,
  gap = 12,
  align = 'right',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const justify = align === 'center' ? 'center' : align === 'left' ? 'flex-start' : 'flex-end';

  return (
    <div style={{ display: 'flex', justifyContent: justify, gap: `${gap}px`, padding: '8px 50px', flexShrink: 0, zIndex: 5, ...style }}>
      {platforms.map((platform) => {
        const path = SOCIAL_ICONS[platform.toLowerCase()];
        if (!path) return null;
        return (
          <div
            key={platform}
            style={{
              width: `${iconSize}px`,
              height: `${iconSize}px`,
              borderRadius: '50%',
              background: hexRgba(c.accent, '0.12'),
              border: `1px solid ${hexRgba(c.accent, '0.25')}`,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <svg width={iconSize * 0.6} height={iconSize * 0.6} viewBox="0 0 24 24" fill={c.accent}>
              <path d={path} />
            </svg>
          </div>
        );
      })}
    </div>
  );
};

// ─── ContactRow ────────────────────────────────────────────────────────
export interface ContactRowProps extends BaseBlockProps {
  phone?: string;
  location?: string;
  hours?: string;
  align?: 'right' | 'left';
}

export const ContactRow: React.FC<ContactRowProps> = ({
  phone,
  location,
  hours,
  align = 'right',
  colors,
  style,
}) => {
  const c = useColors(colors);
  const items: { icon: string; text: string }[] = [];
  if (phone) items.push({ icon: 'phone', text: phone });
  if (location) items.push({ icon: 'location', text: location });
  if (hours) items.push({ icon: 'clock', text: hours });

  return (
    <div style={{
      display: 'flex', flexDirection: 'column', gap: '8px',
      alignItems: align === 'right' ? 'flex-end' : 'flex-start',
      padding: '8px 50px', flexShrink: 0, direction: 'rtl', zIndex: 5, ...style,
    }}>
      {items.map((item, i) => (
        <div key={i} style={{ display: 'flex', alignItems: 'center', gap: '8px', direction: 'rtl' }}>
          <Icon name={item.icon} size={16} color={c.accent} colors={c} />
          <span style={{ fontFamily: FONTS.sans, fontSize: '14px', color: c.text, opacity: 0.85 }}>
            {item.text}
          </span>
        </div>
      ))}
    </div>
  );
};
