// ─────────────────────────────────────────────────────────────────────
// ICONS — Lucide-based icon wrapper
//   Icon · renders any Lucide icon at a given size/color
//   IconBadge · icon in a circular badge with gradient bg
//
// Source: lucide-react (ISC License — see docs/ATTRIBUTIONS.md)
// ─────────────────────────────────────────────────────────────────────

import React from 'react';
import {
  Star, Heart, CheckCircle, Shield, Clock, Phone, MapPin,
  Truck, Gift, Tag, Flame, Crown, Scissors, Droplet, Sparkles,
  Stethoscope, Pill, Camera, ShoppingBag, Scale, Home, Wrench,
  Car, SprayCan, Wind, Calendar, GraduationCap, Award, Zap,
  Coffee, Utensils, Dumbbell, Scissors as ScissorIcon,
  type LucideIcon,
} from 'lucide-react';
import { BaseBlockProps, ColorConfig, hexRgba, useColors } from './helpers';

// Map of common icon names → Lucide components
const ICON_MAP: Record<string, LucideIcon> = {
  star: Star, heart: Heart, check: CheckCircle, shield: Shield,
  clock: Clock, phone: Phone, location: MapPin, truck: Truck,
  gift: Gift, tag: Tag, flame: Flame, crown: Crown,
  scissors: Scissors, droplet: Droplet, sparkles: Sparkles,
  stethoscope: Stethoscope, pill: Pill, camera: Camera,
  shopping: ShoppingBag, scale: Scale, home: Home, wrench: Wrench,
  car: Car, spray: SprayCan, wind: Wind, calendar: Calendar,
  graduate: GraduationCap, award: Award, zap: Zap,
  coffee: Coffee, utensils: Utensils, gym: Dumbbell,
};

// ─── Icon ─────────────────────────────────────────────────────────────
export interface IconProps extends BaseBlockProps {
  /** Icon name — maps to a Lucide icon. */
  name: string;
  /** Size in px. Default 24. */
  size?: number;
  /** Color override (defaults to colors.accent). */
  color?: string;
  /** Stroke width. Default 2. */
  strokeWidth?: number;
}

export const Icon: React.FC<IconProps> = ({
  name,
  size = 24,
  color,
  strokeWidth = 2,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const LucideComp = ICON_MAP[name.toLowerCase()] || Sparkles;

  return (
    <LucideComp
      size={size}
      color={color ?? c.accent}
      strokeWidth={strokeWidth}
      style={{ display: 'block', ...style }}
    />
  );
};

// ─── IconBadge ────────────────────────────────────────────────────────
export interface IconBadgeProps extends BaseBlockProps {
  /** Icon name. */
  name: string;
  /** Badge size (diameter) in px. Default 48. */
  badgeSize?: number;
  /** Icon size in px. Default 24. */
  iconSize?: number;
  /** Use gradient background. Default true. */
  gradient?: boolean;
}

export const IconBadge: React.FC<IconBadgeProps> = ({
  name,
  badgeSize = 48,
  iconSize = 24,
  gradient = true,
  colors,
  style,
}) => {
  const c = useColors(colors);
  const bg = gradient
    ? `linear-gradient(135deg, ${c.accent}, ${c.accent2})`
    : hexRgba(c.accent, '0.15');

  return (
    <div
      style={{
        width: `${badgeSize}px`,
        height: `${badgeSize}px`,
        borderRadius: '50%',
        background: bg,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        border: gradient ? 'none' : `1px solid ${hexRgba(c.accent, '0.3')}`,
        flexShrink: 0,
        ...style,
      }}
    >
      <Icon name={name} size={iconSize} color={gradient ? c.badgeText : c.accent} colors={c} />
    </div>
  );
};

export { ICON_MAP };
