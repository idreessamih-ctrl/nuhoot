import React from 'react';
import { Composition } from 'remotion';
import { NuhootPost, NuhootPostProps } from './NuhootPost';
import {
  DynamicComposer,
  SAMPLE_BLUEPRINT,
} from './DynamicComposer';
import type { DynamicComposerProps } from './DynamicComposer';

// Niche names → composition IDs (hyphens, not underscores)
const NICHES: { id: string; niche: string }[] = [
  { id: 'restaurants', niche: 'restaurants' },
  { id: 'cafes', niche: 'cafes' },
  { id: 'bakeries', niche: 'bakeries' },
  { id: 'salons', niche: 'salons' },
  { id: 'spas', niche: 'spas' },
  { id: 'barbershops', niche: 'barbershops' },
  { id: 'gyms', niche: 'gyms' },
  { id: 'clinics', niche: 'clinics' },
  { id: 'dentists', niche: 'dentists' },
  { id: 'pharmacies', niche: 'pharmacies' },
  { id: 'dermatology', niche: 'dermatology' },
  { id: 'fashion', niche: 'fashion' },
  { id: 'perfumes', niche: 'perfumes' },
  { id: 'law-firms', niche: 'law_firms' },
  { id: 'real-estate', niche: 'real_estate' },
  { id: 'auto-shops', niche: 'auto_shops' },
  { id: 'car-wash', niche: 'car_wash' },
  { id: 'cleaning', niche: 'cleaning' },
  { id: 'hvac-ac', niche: 'hvac_ac' },
  { id: 'event-halls', niche: 'event_halls' },
  { id: 'training-centers', niche: 'training_centers' },
  { id: 'drive-thru-coffee', niche: 'drive_thru_coffee' },
  { id: 'pet-grooming', niche: 'pet_grooming' },
  { id: 'desert-glamping', niche: 'desert_glamping' },
];

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {NICHES.map(({ id, niche }) => (
        <Composition
          key={id}
          id={id}
          component={NuhootPost}
          durationInFrames={1}
          fps={30}
          width={1080}
          height={1080}
          defaultProps={{
            niche,
            headline: 'عنوان تجريبي',
            name: 'اسم المحل',
            taglines: ['سطر أول', 'سطر ثاني', 'سطر ثالث'],
            hashtags: ['#هاشتاق'],
            cta: 'زورونا',
            photoPath: '',
          }}
        />
      ))}

      {/* ─── Dynamic design engine composition ─────────────────────────── */}
      {/* Renders any DesignBlueprint from Kimi via the DynamicComposer.    */}
      {/* Usage:                                                            */}
      {/*   npx remotion still src/index.ts dynamic out.png \               */}
      {/*     --props='{"blueprint":{"composition":[...],"globalStyles":{}}}' */}
      <Composition
        id="dynamic"
        component={DynamicComposer}
        durationInFrames={1}
        fps={30}
        width={1080}
        height={1080}
        defaultProps={{
          blueprint: SAMPLE_BLUEPRINT,
        } as DynamicComposerProps}
      />
    </>
  );
};
