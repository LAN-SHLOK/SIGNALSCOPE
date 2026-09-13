import React, { useState } from 'react';
import { SparkleStar } from './SparkleStar';
import { 
  GitBranch, 
  Cpu, 
  Layers, 
  SlidersHorizontal, 
  ShieldCheck, 
  Activity, 
  Maximize2,
  ChevronRight,
  Zap,
  Sparkles,
  Lock,
  Flame,
  CheckCircle2
} from 'lucide-react';

export const ArchitectureFlow: React.FC = () => {
  const [selectedStream, setSelectedStream] = useState<'stream1' | 'stream2' | 'fusion' | 'boosters'>('stream1');

  const streamDetails = {
    stream1: {
      title: 'STREAM 1: FROZEN DINOv2 FOUNDATION BACKBONE',
      badge: 'Zero Trainable Parameters • 304M Frozen Weights',
      headline: 'Captures high-level visual structure, optical physics, and geometric coherence.',
      points: [
        {
          title: 'DINOv2-reg ViT-L/14 (Native 518×518)',
          desc: 'Trained self-supervised on 142M curated images with zero class labels. Avoids generator-specific shortcut learning.'
        },
        {
          title: 'Multi-Layer Feature Extraction (4,096-dim)',
          desc: 'Captures CLS tokens across 4 distinct depths: Layer 8 (low-level edges/textures), Layer 16 (mid-level shapes), Layer 20 & 24 (high-level semantic physics).'
        },
        {
          title: 'Patch Token Statistics (3,073-dim)',
          desc: 'Analyzes spatial variance across 1,369 patch tokens: mean (1024), standard deviation (1024), maximum values (1024), and average pairwise patch similarity (1).'
        },
        {
          title: 'Why It Defeats Unseen Generators',
          desc: 'Generators evolve their appearance, but they struggle to match the subtle optical physics and natural token variance learned by foundation vision transformers.'
        }
      ]
    },
    stream2: {
      title: 'STREAM 2: FORENSIC SPECTRAL BRANCH',
      badge: 'High-Pass Noise Residuals & Sensor Signatures',
      headline: 'Exposes microscopic noise fingerprints and camera hardware artifacts.',
      points: [
        {
          title: 'Multi-Colorspace SRM High-Pass Filters',
          desc: 'Extracts 3 spatial rich model high-pass kernels across RGB, YCbCr, and HSV (9 channels). Synthetic images exhibit unnatural smoothness in chrominance channels.'
        },
        {
          title: 'SpectralCNN (9ch → 256-dim)',
          desc: 'A lightweight 4-layer conv net trained exclusively on residual maps to learn noise-level generator anomalies.'
        },
        {
          title: 'FFT Azimuthal Frequency Spectrum (128-dim)',
          desc: 'Radially averages 2D Fourier power to detect periodic peaks caused by transposed convolutions and latent diffusion upsampling.'
        },
        {
          title: 'Bayer CFA Autocorrelation (2-dim) & JPEG Ghost (20-dim)',
          desc: 'Detects the physical 2-pixel color filter mosaic present on genuine camera sensors and tracks re-compression history profiles.'
        }
      ]
    },
    fusion: {
      title: 'FUSION DETECTOR & PARALLEL STACKING',
      badge: '7,575-dim Fusion Vector • Dual Task Heads',
      headline: 'Merges semantic and spectral dimensions with CPU-fast LightGBM ensemble.',
      points: [
        {
          title: 'Combined Feature Vector (7,575 Dimensions)',
          desc: 'Concatenates DINOv2 CLS (4096) + Patch Stats (3073) + SRM-CNN (256) + FFT (128) + JPEG Ghost (20) + Bayer (2).'
        },
        {
          title: 'Shared Fusion MLP (7575 → 1024 → 256 → 128)',
          desc: 'GELU-activated bottleneck with dropout regularisation and multi-task learning.'
        },
        {
          title: 'Dual Task Heads',
          desc: 'Binary Head (128 → 1 logit: Real vs AI) + Attribution Head (128 → 4 logits: Real, GAN-family, Diffusion-family, Unknown).'
        },
        {
          title: 'Parallel LightGBM Stacking Meta-Learner',
          desc: 'Trains in 30 seconds on CPU to learn non-linear interactions across high-dimensional features, blended with the neural head.'
        }
      ]
    },
    boosters: {
      title: '10 ZERO-COST INFERENCE BOOSTERS',
      badge: '+8% to +15% AUC Boost • Zero Retraining Compute',
      headline: 'Inference-time optimizations that elevate performance onto the winning podium.',
      points: [
        {
          title: 'Post-Hoc Temperature Scaling (ECE < 0.04)',
          desc: 'Calibrates raw logits using LBFGS on validation data so a 0.88 score mathematically represents an 88% empirical probability.'
        },
        {
          title: '5-View Test-Time Augmentation (TTA)',
          desc: 'Averages predictions across original, horizontal flip, vertical flip, 90% crop, and minor noise to smooth out variance.'
        },
        {
          title: 'Smart 3-Tier Responsible Abstention',
          desc: 'Sorts predictions into Confident AI (>0.75), Confident Real (<0.25), and flags ambiguous images (0.25–0.75) for human review.'
        },
        {
          title: 'Dual Optimal Threshold Selection',
          desc: 'Pre-computed thresholds for Max-F1 (balanced detection) and Conservative Mode (False Positive Rate < 5% to avoid false accusations).'
        }
      ]
    }
  };

  const active = streamDetails[selectedStream];

  return (
    <section id="architecture" className="py-16 bg-[#060a08] text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Section Title */}
        <div className="mb-10 text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 text-xs font-mono-code text-[#00e540] uppercase tracking-wider mb-2">
            <Cpu className="w-4 h-4" />
            <span>Section 3 & 5 • Core Architecture</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-black font-syne tracking-tight text-white mb-3">
            DUAL-STREAM ENGINE & FUSION
          </h2>
          <p className="text-sm sm:text-base text-gray-400">
            Why SignalScope generalizes to unseen AI generators without overfitting to existing training artifacts.
          </p>
        </div>

        {/* INTERACTIVE ARCHITECTURE PIPELINE MAP */}
        <div className="mb-10 bg-[#0c130f] rounded-3xl border border-[#1b3623] p-6 lg:p-8 shadow-2xl relative overflow-hidden">
          {/* Top flow step indicators */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-8">
            <button
              onClick={() => setSelectedStream('stream1')}
              className={`p-4 rounded-2xl border text-left transition-all ${
                selectedStream === 'stream1'
                  ? 'bg-[#00e540] text-black border-white shadow-[0_0_20px_rgba(0,229,64,0.3)]'
                  : 'bg-[#101913] text-white border-[#1c3523] hover:border-[#00e540]/40'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono-code uppercase font-bold px-2 py-0.5 rounded bg-black/20">
                  Stream 1
                </span>
                <Lock className="w-4 h-4" />
              </div>
              <div className="font-bold font-syne text-sm sm:text-base">
                DINOv2 ViT-L/14
              </div>
              <div className={`text-xs mt-1 ${selectedStream === 'stream1' ? 'text-black/80' : 'text-gray-400'}`}>
                Frozen Backbone • 7,169-dim
              </div>
            </button>

            <button
              onClick={() => setSelectedStream('stream2')}
              className={`p-4 rounded-2xl border text-left transition-all ${
                selectedStream === 'stream2'
                  ? 'bg-[#00e540] text-black border-white shadow-[0_0_20px_rgba(0,229,64,0.3)]'
                  : 'bg-[#101913] text-white border-[#1c3523] hover:border-[#00e540]/40'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono-code uppercase font-bold px-2 py-0.5 rounded bg-black/20">
                  Stream 2
                </span>
                <Activity className="w-4 h-4" />
              </div>
              <div className="font-bold font-syne text-sm sm:text-base">
                Forensic Spectral
              </div>
              <div className={`text-xs mt-1 ${selectedStream === 'stream2' ? 'text-black/80' : 'text-gray-400'}`}>
                SRM 9ch + FFT + Bayer
              </div>
            </button>

            <button
              onClick={() => setSelectedStream('fusion')}
              className={`p-4 rounded-2xl border text-left transition-all ${
                selectedStream === 'fusion'
                  ? 'bg-[#00e540] text-black border-white shadow-[0_0_20px_rgba(0,229,64,0.3)]'
                  : 'bg-[#101913] text-white border-[#1c3523] hover:border-[#00e540]/40'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono-code uppercase font-bold px-2 py-0.5 rounded bg-black/20">
                  Fusion
                </span>
                <Layers className="w-4 h-4" />
              </div>
              <div className="font-bold font-syne text-sm sm:text-base">
                MLP + LightGBM
              </div>
              <div className={`text-xs mt-1 ${selectedStream === 'fusion' ? 'text-black/80' : 'text-gray-400'}`}>
                7,575-dim • Dual Heads
              </div>
            </button>

            <button
              onClick={() => setSelectedStream('boosters')}
              className={`p-4 rounded-2xl border text-left transition-all ${
                selectedStream === 'boosters'
                  ? 'bg-[#00e540] text-black border-white shadow-[0_0_20px_rgba(0,229,64,0.3)]'
                  : 'bg-[#101913] text-white border-[#1c3523] hover:border-[#00e540]/40'
              }`}
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-[10px] font-mono-code uppercase font-bold px-2 py-0.5 rounded bg-black/20">
                  Boosters
                </span>
                <Zap className="w-4 h-4" />
              </div>
              <div className="font-bold font-syne text-sm sm:text-base">
                10 Zero-Cost Wins
              </div>
              <div className={`text-xs mt-1 ${selectedStream === 'boosters' ? 'text-black/80' : 'text-gray-400'}`}>
                TTA, Scaling & Abstention
              </div>
            </button>
          </div>

          {/* ACTIVE STREAM DETAIL SHOWCASE */}
          <div className="bg-[#101913] rounded-2xl border border-[#1b3623] p-6 lg:p-8">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4 border-b border-[#1b3623] pb-4">
              <div>
                <span className="text-xs font-mono-code text-[#00e540] font-bold tracking-wider">
                  {active.badge}
                </span>
                <h3 className="text-xl sm:text-2xl font-black font-syne text-white mt-0.5">
                  {active.title}
                </h3>
              </div>
              <div className="text-xs text-gray-400 font-mono-code">
                SignalScope v3 Specification
              </div>
            </div>

            <p className="text-gray-300 text-sm sm:text-base font-medium mb-6">
              {active.headline}
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {active.points.map((pt, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-[#090d0b] border border-[#1c3523] flex flex-col justify-between">
                  <div>
                    <div className="flex items-center gap-2 mb-1.5">
                      <span className="w-5 h-5 rounded-full bg-[#00e540]/20 text-[#00e540] flex items-center justify-center font-mono-code text-xs font-bold shrink-0">
                        {idx + 1}
                      </span>
                      <h4 className="font-bold font-display text-sm text-white">
                        {pt.title}
                      </h4>
                    </div>
                    <p className="text-xs text-gray-300 leading-relaxed pl-7">
                      {pt.desc}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* COMPARISON TABLE: WHY THIS WINS ON UNSEEN GENERATORS */}
        <div className="bg-[#0c130f] rounded-3xl border border-[#1b3623] p-6 sm:p-8">
          <div className="flex items-center gap-2 text-xs font-mono-code text-[#00e540] uppercase tracking-wider mb-2">
            <Sparkles className="w-4 h-4" />
            <span>Key Innovation • Problem Statement 2 Advantage</span>
          </div>
          <h3 className="text-2xl font-black font-syne text-white mb-6">
            WHY THIS ARCHITECTURE WINS ON UNSEEN GENERATORS
          </h3>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-[#1b3623] text-gray-400 font-mono-code">
                  <th className="py-3 px-4 uppercase">Component</th>
                  <th className="py-3 px-4 uppercase">What It Captures</th>
                  <th className="py-3 px-4 uppercase">Why It Generalises (The Winning Edge)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1b3623]/60 text-gray-300">
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white font-mono-code">DINOv2 (Frozen)</td>
                  <td className="py-3.5 px-4">Edges, textures, lighting physics, geometry</td>
                  <td className="py-3.5 px-4 text-[#00e540]">Self-supervised on 142M images; no class bias; zero generator shortcut traps.</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white font-mono-code">Multi-Layer CLS</td>
                  <td className="py-3.5 px-4">Layers 8 (low), 16 (mid), 20 & 24 (high)</td>
                  <td className="py-3.5 px-4 text-[#00e540]">Artifacts exist at all scales; single-layer extraction misses shallow noise.</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white font-mono-code">Patch Statistics</td>
                  <td className="py-3.5 px-4">Spatial variance across 1,369 patches</td>
                  <td className="py-3.5 px-4 text-[#00e540]">Synthetic images are unnaturally uniform; real photographs possess rich local chaos.</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white font-mono-code">SRM Multi-Colorspace</td>
                  <td className="py-3.5 px-4">Noise residuals across RGB + YCbCr + HSV</td>
                  <td className="py-3.5 px-4 text-[#00e540]">Noise fingerprints persist across all generators; color-space diversity catches channel anomalies.</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white font-mono-code">Bayer Autocorrelation</td>
                  <td className="py-3.5 px-4">Camera sensor CFA demosaicing lattice</td>
                  <td className="py-3.5 px-4 text-[#00e540]">Every real camera hardware chip leaves 2-pixel periodic traces; AI renders never have them.</td>
                </tr>
                <tr className="hover:bg-white/5 transition-colors">
                  <td className="py-3.5 px-4 font-bold text-white font-mono-code">LightGBM Stacking</td>
                  <td className="py-3.5 px-4">Non-linear feature interactions</td>
                  <td className="py-3.5 px-4 text-[#00e540]">Trains in 30 seconds on CPU; catches subtle decision-tree thresholds missed by neural MLPs.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
};
