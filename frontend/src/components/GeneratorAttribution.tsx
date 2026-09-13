import React, { useState } from 'react';
import { SparkleStar } from './SparkleStar';
import { 
  Binary, 
  Cpu, 
  Layers, 
  CheckCircle2, 
  Sparkles, 
  Crosshair, 
  Compass, 
  Flame,
  Camera,
  Wand2,
  Box
} from 'lucide-react';

export const GeneratorAttribution: React.FC = () => {
  const [selectedFamily, setSelectedFamily] = useState<number>(0);

  const families = [
    {
      name: 'Diffusion-Family',
      badge: 'Midjourney v5/v6, SDXL, DALL-E 3, Flux',
      classIdx: 2,
      targetF1: '0.92 F1',
      trainingLossWeight: '0.25 (balanced)',
      fingerprint: 'Latent upsampling residual noise & prompt optical physics',
      indicators: [
        'High-frequency energy spikes along sharp object contours (de-noising steps)',
        'Unnaturally high spatial uniformity across DINOv2 patch tokens (avg similarity > 0.78)',
        'Absence of hardware camera sensor Bayer CFA 2-pixel autocorrelation',
        'Subtle optical physics contradictions (conflicting light rays vs cast shadows)'
      ],
      icon: <Wand2 className="w-5 h-5 text-cyan-400" />,
      accent: 'border-cyan-500/40 bg-cyan-500/5 text-cyan-400'
    },
    {
      name: 'GAN-Family',
      badge: 'StyleGAN2/3, ProGAN, BigGAN, CycleGAN',
      classIdx: 1,
      targetF1: '0.94 F1',
      trainingLossWeight: '0.25 (balanced)',
      fingerprint: 'Transposed conv checkerboard harmonics & eye geometry glitches',
      indicators: [
        'Prominent 4-quadrant symmetric peaks in the 2D Fast Fourier Transform spectrum',
        'Asymmetric pupil contours and mismatched corneal specular catchlights',
        'Hair strand boundary melting into blurry or chaotic background artifacts',
        'Periodic grid lines visible in Spatial Rich Model (SRM) chrominance channels'
      ],
      icon: <Box className="w-5 h-5 text-purple-400" />,
      accent: 'border-purple-500/40 bg-purple-500/5 text-purple-400'
    },
    {
      name: 'Real Camera Hardware',
      badge: 'Canon, Sony, Nikon, iPhone, Pixel Native Raw/JPG',
      classIdx: 0,
      targetF1: '0.96 F1',
      trainingLossWeight: '0.30 (safety priority)',
      fingerprint: 'Bayer CFA mosaic demodulation & authentic 1/f optical physics',
      indicators: [
        'Confirmed 2-pixel periodic lattice in high-pass residual autocorrelation (ratio > 1.050)',
        'Power spectrum strictly follows natural optical 1/f decay law into sensor noise floor',
        'Natural spatial diversity across patch tokens (heterogeneous real-world textures)',
        'Valid EXIF hardware tags and cryptographic C2PA device signatures when present'
      ],
      icon: <Camera className="w-5 h-5 text-[#00e540]" />,
      accent: 'border-[#00e540]/40 bg-[#00e540]/5 text-[#00e540]'
    },
    {
      name: 'Unknown / Novel Synthetic',
      badge: 'Emerging Generators, Hybrids & OOD Latents',
      classIdx: 3,
      targetF1: '0.85 F1',
      trainingLossWeight: '0.20 (out-of-distribution)',
      fingerprint: 'Statistical deviation from authentic camera manifold',
      indicators: [
        'Fails authentic camera sensor checks without matching known GAN/Diffusion clusters',
        'Intermediate confidence logits triggering Smart Abstention protocol',
        'Flags for human-in-the-loop expert review to prevent false accusations',
        'Serves as an active learning trigger to queue novel generator samples for retraining'
      ],
      icon: <Compass className="w-5 h-5 text-amber-400" />,
      accent: 'border-amber-500/40 bg-amber-500/5 text-amber-400'
    }
  ];

  const active = families[selectedFamily];

  return (
    <section id="attribution" className="py-16 bg-[#090d0b] text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Header */}
        <div className="mb-10 text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 text-xs font-mono-code text-[#00e540] uppercase tracking-wider mb-2">
            <Binary className="w-4 h-4" />
            <span>Module B • Multi-Class Generator Attribution</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-black font-syne tracking-tight text-white mb-3">
            GENERATOR FAMILY ATTRIBUTION
          </h2>
          <p className="text-sm sm:text-base text-gray-400">
            Beyond binary Real-vs-AI, SignalScope classifies the underlying generative engine with zero extra compute by tapping the shared 128-dim fusion layer.
          </p>
        </div>

        {/* 4 GENERATOR FAMILY CARDS */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-3 mb-8">
          {families.map((fam, idx) => {
            const isSelected = selectedFamily === idx;
            return (
              <button
                key={fam.name}
                onClick={() => setSelectedFamily(idx)}
                className={`p-4 rounded-2xl border text-left transition-all ${
                  isSelected
                    ? 'bg-[#00e540] text-black border-white shadow-lg'
                    : 'bg-[#0e1611] text-white border-[#1c3323] hover:border-[#00e540]/40'
                }`}
              >
                <div className="flex items-center justify-between mb-2">
                  <div className={`p-1.5 rounded-lg ${isSelected ? 'bg-black text-[#00e540]' : 'bg-white/10'}`}>
                    {fam.icon}
                  </div>
                  <span className={`text-[10px] font-mono-code font-bold px-2 py-0.5 rounded ${
                    isSelected ? 'bg-black text-white' : 'bg-white/5 text-gray-300'
                  }`}>
                    {fam.targetF1}
                  </span>
                </div>
                <div className="font-bold font-syne text-sm sm:text-base">
                  {fam.name}
                </div>
                <div className={`text-[11px] truncate mt-1 ${isSelected ? 'text-black/80' : 'text-gray-400'}`}>
                  {fam.badge}
                </div>
              </button>
            );
          })}
        </div>

        {/* ACTIVE FAMILY SPOTLIGHT */}
        <div className="bg-[#0c130f] rounded-3xl border border-[#1b3623] p-6 lg:p-8">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#1b3623] pb-6 mb-6">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <span className="text-xs font-mono-code text-[#00e540] font-bold">
                  Class #{active.classIdx} • Attribution Target Head (128 → 4)
                </span>
              </div>
              <h3 className="text-2xl sm:text-3xl font-black font-syne text-white">
                {active.name}
              </h3>
              <p className="text-xs text-gray-400 mt-0.5">
                {active.badge}
              </p>
            </div>

            <div className="flex items-center gap-3">
              <div className="px-4 py-2 rounded-xl bg-[#101913] border border-[#1c3523] text-right">
                <span className="text-[10px] font-mono-code text-gray-400 block uppercase">Target F1 Score</span>
                <span className="text-base font-mono-code font-bold text-[#00e540]">{active.targetF1}</span>
              </div>
              <div className="px-4 py-2 rounded-xl bg-[#101913] border border-[#1c3523] text-right">
                <span className="text-[10px] font-mono-code text-gray-400 block uppercase">Loss Weight</span>
                <span className="text-base font-mono-code font-bold text-white">{active.trainingLossWeight}</span>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div className="lg:col-span-4 bg-[#101913] rounded-2xl border border-[#1b3623] p-5 flex flex-col justify-between">
              <div>
                <span className="text-xs font-mono-code text-[#00e540] uppercase font-bold block mb-1">
                  Primary Fingerprint
                </span>
                <p className="text-sm font-display font-semibold text-white leading-snug mb-4">
                  {active.fingerprint}
                </p>
                <div className="text-xs text-gray-400 leading-relaxed space-y-2">
                  <p>
                    <strong>Architecture Efficiency:</strong> By training a 4-class linear projection head on top of the shared 128-dimensional bottleneck layer, we achieve generator attribution with <strong>zero additional compute during feature extraction</strong>.
                  </p>
                  <p>
                    Trained using class-weighted <code>CrossEntropyLoss</code> to handle imbalanced representation across generator families in the training corpus.
                  </p>
                </div>
              </div>

              <div className="mt-6 pt-3 border-t border-[#1c3523] text-[11px] font-mono-code text-[#00e540]">
                ✓ Shared 128-dim Fusion Bottleneck
              </div>
            </div>

            <div className="lg:col-span-8 bg-[#101913] rounded-2xl border border-[#1b3623] p-5">
              <span className="text-xs font-mono-code text-gray-300 uppercase font-bold block mb-3">
                Key Forensic Clues & Extraction Signals:
              </span>
              <div className="space-y-3">
                {active.indicators.map((ind, i) => (
                  <div key={i} className="flex items-start gap-3 p-3 rounded-xl bg-[#090d0b] border border-[#1c3523]">
                    <CheckCircle2 className="w-4 h-4 text-[#00e540] shrink-0 mt-0.5" />
                    <span className="text-xs text-gray-200 leading-relaxed">
                      {ind}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
