import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { SparkleStar } from './SparkleStar';
import { 
  Eye, 
  Camera, 
  Radio, 
  ShieldCheck, 
  Cpu, 
  Layers, 
  Binary, 
  Sliders, 
  CheckCircle2, 
  ArrowRight,
  Code
} from 'lucide-react';

export const PipelineSection: React.FC = () => {
  const [activeStep, setActiveStep] = useState<number>(0);
  const [viewMode, setViewMode] = useState<'simple' | 'technical'>('simple');

  const steps = [
    {
      num: '01',
      title: 'VISUAL ANATOMY & LIGHT PHYSICS',
      tag: 'Stage 1 • Spatial Stream',
      modelUsed: 'DINOv2-L14 / ViT-Large',
      toolUsed: 'Self-Supervised Vision Transformer + Attention Rollout',
      simpleExplainer: 'Inspects the photograph for things that violate the laws of physics or natural biology.',
      simplePoints: [
        'Scans human eyes and teeth for unnatural glassiness or mismatched reflections.',
        'Inspects hands, hair strands, and fabric wrinkles for telltale blending glitches.',
        'Verifies that cast shadows match the angle and color temperature of the real light source.'
      ],
      analogy: 'An art curator noticing that a painted shadow falls left, even though the candle is on the right.',
      technicalDetails: {
        input: 'Normalized 1024×1024 RGB image tensor',
        process: 'Passes through 24-layer ViT with 16 attention heads. Computes query-key attention matrices across 16×16 spatial patches to construct global spatial semantic vectors.',
        output: '1024-dimensional semantic embedding + Attention Rollout anomaly saliency map.',
        whyItWins: 'Detects semantic hallucination in faces and lighting physics that simple CNN pixel classifiers completely miss.'
      }
    },
    {
      num: '02',
      title: 'CAMERA SENSOR GRAIN EXTRACTION',
      tag: 'Stage 2 • Sensor Stream',
      modelUsed: 'ResNet-50 + SRM 30 Filter Bank',
      toolUsed: 'Steganographic Spatial Rich Models (SRM) + Residual Backbone',
      simpleExplainer: 'Real camera lenses and silicon chips leave a microscopic grain on every single photo. AI tools do not have cameras, so this grain is absent.',
      simplePoints: [
        'Physical cameras (iPhone, Sony, Canon) capture light onto a silicon sensor.',
        'This physical process imprints an authentic microscopic noise lattice.',
        'AI generators synthesize pixels through pure math, creating unnaturally sterile or blotchy noise.'
      ],
      analogy: 'Fingerprints on a drinking glass: physical tools always leave a physical mark, while computer algorithms do not.',
      technicalDetails: {
        input: 'RGB image filtered through 30 SRM linear high-pass kernels (1st, 2nd, and 3rd order derivative filters)',
        process: 'Suppresses semantic content to expose Photo-Response Non-Uniformity (PRNU) and Bayer Color Filter Array (CFA) demosaicing traces. Feeds residual noise into a dedicated CNN backbone.',
        output: '512-dimensional sensor residual embedding.',
        whyItWins: 'Cannot be faked by AI prompt generators because latent diffusion models operate on compressed latent tensors without hardware sensor physics.'
      }
    },
    {
      num: '03',
      title: 'LIGHT FREQUENCY WAVE ANALYSIS',
      tag: 'Stage 3 • Spectral Decomposition',
      modelUsed: '2D Fast Fourier Transform (FFT)',
      toolUsed: 'Azimuthal Radial Power Spectrum Decomposition',
      simpleExplainer: 'Just as songs are made of high and low musical notes, digital pictures are made of light waves. AI leaves repeating mathematical ripples in these waves.',
      simplePoints: [
        'Converts pixels into light frequency waves.',
        'Real camera photos produce smooth, gentle curves as light naturally scatters.',
        'Generative tools (Midjourney, DALL-E, Stable Diffusion) leave distinct checkerboard spikes from pixel upsampling.'
      ],
      analogy: 'Listening to music: you can easily tell a real wooden guitar apart from an electronic synthesizer.',
      technicalDetails: {
        input: '2D discrete spatial image representation converted via Fast Fourier Transform: F(u,v) = Σ Σ f(x,y) e^(-i2π(ux/M + vy/N))',
        process: 'Computes log-magnitude power spectrum centered at zero frequency. Analyzes radial power decay slope (1/f^α) and measures periodic grid peaks caused by deconvolution upsampling.',
        output: 'Radial slope coefficient + high-frequency periodic peak score.',
        whyItWins: 'Reveals mathematical generator architecture fingerprints even when images are heavily retouched.'
      }
    },
    {
      num: '04',
      title: 'MULTI-MODAL FUSION & DECISION',
      tag: 'Stage 4 • Final Verdict & Calibration',
      modelUsed: 'Cross-Attention MLP + Temperature Scaling',
      toolUsed: 'Selective Classification & Dual-Stream Grad-CAM',
      simpleExplainer: 'Combines all clues together. If it is certain, it generates a clear heatmap showing why. If an image is too blurry or compressed, it honestly asks for a human look.',
      simplePoints: [
        'Weights visual clues, camera noise, and frequency waves simultaneously.',
        'Generates an interactive red/orange heatmap showing you the exact pixels that caused suspicion.',
        'Never makes false 100% claims: heavily compressed or ambiguous images are transparently flagged for human review.'
      ],
      analogy: 'A trustworthy doctor who shows you the X-ray results rather than just handing you a mystery prescription.',
      technicalDetails: {
        input: 'Concatenated 1536-d feature vector (Spatial 1024-d + Sensor 512-d) + C2PA cryptographic trust flag',
        process: 'Processes through 3-layer cross-attention fusion MLP. Applies Platt temperature scaling (T=1.42) to ensure mathematically calibrated probabilities. Implements selective classification: confidence within [0.35, 0.65] triggers Smart Abstention.',
        output: 'Calibrated verdict probability + generator attribution class + composite Grad-CAM spatial heatmap.',
        whyItWins: 'Completely prevents false accusations on compressed social media files by refusing brittle binary guesses when data is degraded.'
      }
    }
  ];

  const tools = [
    {
      title: 'Visual Transformer Stream',
      model: 'DINOv2-L14 (ViT)',
      desc: 'Extracts human anatomy, specular eye reflections, and physical light direction vectors.',
      icon: Eye,
      num: '01'
    },
    {
      title: 'Sensor Residual Stream',
      model: 'SRM 30 + ResNet-50',
      desc: 'Isolates microscopic silicon camera sensor noise and hardware CFA demosaicing lattices.',
      icon: Camera,
      num: '02'
    },
    {
      title: 'Frequency Spectrometer',
      model: '2D FFT Spectral Engine',
      desc: 'Measures light wave decay slopes and identifies checkerboard upsampling spikes.',
      icon: Radio,
      num: '03'
    },
    {
      title: 'Fusion & Abstention Engine',
      model: 'Calibrated MLP + XAI',
      desc: 'Fuses multi-modal streams, enforces calibrated probabilities, and generates transparent heatmaps.',
      icon: ShieldCheck,
      num: '04'
    }
  ];

  return (
    <section 
      id="pipeline" 
      className="relative min-h-screen py-24 px-4 sm:px-8 lg:px-12 bg-[#b81424] text-white selection:bg-black selection:text-white flex flex-col justify-center border-b-2 border-black overflow-hidden"
    >
      {/* FULL-BLEED GRAPHIC POSTER BACKGROUND (Japanese brutalist red poster style) */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#8f0f1c] via-[#b81424] to-[#730814] pointer-events-none" />
      
      {/* Outer framing line */}
      <div className="absolute top-12 left-4 right-4 bottom-12 border-2 border-white/70 pointer-events-none hidden sm:block" />
      <div className="absolute top-16 left-8 right-8 bottom-16 border border-black/30 pointer-events-none hidden md:block" />

      {/* Interactive floating decorative stars (hidden on small screens to prevent overlap) */}
      <motion.div 
        animate={{ y: [0, -8, 0], rotate: [0, 15, 0] }}
        transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-16 right-16 z-10 hidden md:block"
      >
        <SparkleStar size={64} fill="#ffffff" className="opacity-40 hover:opacity-100 transition-opacity" />
      </motion.div>
      <motion.div 
        animate={{ y: [0, 8, 0], rotate: [0, -15, 0] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
        className="absolute bottom-20 left-12 z-10 hidden lg:block"
      >
        <SparkleStar size={48} fill="#fbbf24" className="opacity-50 hover:opacity-100 transition-opacity" />
      </motion.div>

      <div className="max-w-7xl mx-auto w-full relative z-10">
        {/* Section Header */}
        <motion.div 
          initial={{ opacity: 0, y: 35 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.2 }}
          transition={{ duration: 0.6, type: "spring", stiffness: 100, damping: 20 }}
          className="flex flex-col md:flex-row items-start md:items-end justify-between gap-6 mb-12 border-b-2 border-white/20 pb-6"
        >
          <div>
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-black text-white font-mono-code text-xs font-bold uppercase tracking-widest mb-3 border border-white/40">
              <span className="w-2 h-2 bg-amber-300 animate-pulse" />
              <span>HOW THE PIPELINE WORKS</span>
            </div>

            <h2 className="font-poster text-5xl sm:text-7xl lg:text-8xl uppercase tracking-tight leading-[0.9] text-white mb-2">
              HOW IT WORKS
            </h2>

            <p className="font-display font-bold text-base sm:text-lg text-[#fff3e6] max-w-2xl">
              From image ingestion and sensor filtering to multi-modal cross-attention fusion.
            </p>
          </div>

          {/* TOGGLE: SIMPLE WORDS vs TECHNICAL ARCHITECTURE */}
          <div className="inline-flex p-1 bg-black border-2 border-white shadow-[4px_4px_0px_rgba(0,0,0,0.8)]">
            <motion.button
              whileTap={{ scale: 0.96 }}
              onClick={() => setViewMode('simple')}
              className={`px-4 py-2 font-display font-bold text-xs uppercase tracking-wider transition-colors duration-150 ${
                viewMode === 'simple'
                  ? 'bg-white text-black'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              Simple Explanation
            </motion.button>
            <motion.button
              whileTap={{ scale: 0.96 }}
              onClick={() => setViewMode('technical')}
              className={`px-4 py-2 font-display font-bold text-xs uppercase tracking-wider transition-colors duration-150 flex items-center gap-1.5 ${
                viewMode === 'technical'
                  ? 'bg-white text-black'
                  : 'text-gray-300 hover:text-white'
              }`}
            >
              <Code className="w-3.5 h-3.5" />
              Technical & Models
            </motion.button>
          </div>
        </motion.div>

        {/* 4 PIPELINE STEPS */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 mb-16 items-stretch">
          {/* STEP SELECTOR BUTTONS (5 Cols) */}
          <div className="lg:col-span-5 flex flex-col justify-between gap-3">
            {steps.map((s, idx) => {
              const isActive = activeStep === idx;
              return (
                <motion.button
                  key={s.num}
                  initial={{ opacity: 0, x: -30 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: false, amount: 0.15 }}
                  transition={{ duration: 0.4, delay: idx * 0.08 }}
                  whileHover={{ x: 4, transition: { duration: 0.1, ease: "easeOut" } }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => setActiveStep(idx)}
                  className={`p-4 border-2 text-left transition-colors duration-150 flex items-center justify-between ${
                    isActive
                      ? 'bg-black text-white border-white shadow-[6px_6px_0px_rgba(255,255,255,1)] translate-x-1'
                      : 'bg-white/10 hover:bg-white/20 text-white border-white/30'
                  }`}
                >
                  <div className="flex items-center gap-4">
                    <div className={`w-10 h-10 flex items-center justify-center font-poster text-xl border ${
                      isActive ? 'bg-[#b81424] text-white border-white' : 'bg-black text-white border-white/40'
                    }`}>
                      {s.num}
                    </div>
                    <div>
                      <div className="font-poster text-lg uppercase tracking-wide leading-tight">
                        {s.title}
                      </div>
                      <div className="text-xs font-mono-code text-white/80">
                        {s.tag}
                      </div>
                    </div>
                  </div>

                  <span className="font-mono-code text-[11px] font-bold px-2 py-1 bg-white/20 border border-white/30 shrink-0">
                    STAGE {s.num}
                  </span>
                </motion.button>
              );
            })}
          </div>

          {/* ACTIVE STEP CARD - BLACK BOX WITH ELEGANT WARM CREAM / WHITE / AMBER FONT (NO AI-ISH GREEN) */}
          <motion.div 
            key={activeStep}
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: false, amount: 0.15 }}
            transition={{ duration: 0.4 }}
            className="lg:col-span-7 bg-black text-white border-2 border-white p-6 sm:p-10 shadow-[10px_10px_0px_rgba(0,0,0,0.8)] relative flex flex-col justify-between"
          >
            {/* Top Bar - Clean Warm Cream and White Font */}
            <div className="flex items-center justify-between border-b-2 border-white/20 pb-4 mb-6">
              <span className="font-mono-code text-xs font-bold text-amber-200 uppercase tracking-widest">
                [ STAGE {steps[activeStep].num} ] • {steps[activeStep].tag}
              </span>
              <span className="font-mono-code text-xs text-white/80">
                Model: {steps[activeStep].modelUsed}
              </span>
            </div>

            <div>
              <h3 className="font-poster text-3xl sm:text-4xl uppercase tracking-tight mb-4 text-white">
                {steps[activeStep].title}
              </h3>

              {/* SIMPLE EXPLANATION VIEW */}
              {viewMode === 'simple' && (
                <div className="space-y-6">
                  <p className="font-display font-bold text-base sm:text-lg text-amber-100 leading-snug bg-white/10 p-4 border-l-4 border-amber-300">
                    "{steps[activeStep].simpleExplainer}"
                  </p>

                  <div className="space-y-3 font-display">
                    <span className="font-mono-code text-xs text-white/70 uppercase tracking-wider block">
                      What Happens in this Stage:
                    </span>
                    {steps[activeStep].simplePoints.map((point, i) => (
                      <div key={i} className="flex items-start gap-3 text-sm text-gray-200">
                        <span className="w-4 h-4 rounded-none bg-white text-black font-mono-code font-bold text-xs flex items-center justify-center shrink-0 mt-0.5">
                          ✓
                        </span>
                        <span>{point}</span>
                      </div>
                    ))}
                  </div>

                  <div className="p-4 bg-[#b81424] border border-white/40 text-xs sm:text-sm text-white">
                    <strong className="block font-mono-code text-xs uppercase tracking-wider text-amber-200 mb-1">
                      Everyday Analogy:
                    </strong>
                    <p className="font-medium text-white/95">
                      {steps[activeStep].analogy}
                    </p>
                  </div>
                </div>
              )}

              {/* TECHNICAL & MODELS DEEP-DIVE VIEW */}
              {viewMode === 'technical' && (
                <div className="space-y-4 font-mono-code text-xs">
                  <div className="p-3 bg-white/10 border border-white/20">
                    <span className="text-amber-200 font-bold uppercase block mb-1">Tools & Technology:</span>
                    <span className="text-white text-sm font-sans font-bold">{steps[activeStep].toolUsed}</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <div className="p-3 bg-white/5 border border-white/15">
                      <span className="text-gray-400 block mb-1 font-bold">Input Tensor:</span>
                      <span className="text-gray-200">{steps[activeStep].technicalDetails.input}</span>
                    </div>
                    <div className="p-3 bg-white/5 border border-white/15">
                      <span className="text-gray-400 block mb-1 font-bold">Output Representation:</span>
                      <span className="text-gray-200">{steps[activeStep].technicalDetails.output}</span>
                    </div>
                  </div>

                  <div className="p-3 bg-white/5 border border-white/15">
                    <span className="text-gray-400 block mb-1 font-bold">Mathematical Operation:</span>
                    <p className="text-gray-200 leading-relaxed">{steps[activeStep].technicalDetails.process}</p>
                  </div>

                  <div className="p-3 bg-[#b81424] border border-white/40">
                    <span className="text-amber-200 font-bold block mb-1">Why this Architecture Wins:</span>
                    <p className="text-white leading-relaxed">{steps[activeStep].technicalDetails.whyItWins}</p>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>

        {/* 4 CORE SYSTEM MODULES */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.15 }}
          transition={{ duration: 0.6 }}
          className="border-t-2 border-white/40 pt-10"
        >
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-6">
            <h3 className="font-poster text-2xl sm:text-3xl uppercase tracking-wider text-white">
              CORE SYSTEM MODULES & MODELS
            </h3>
            <span className="font-mono-code text-xs text-white/80">
              DUAL-STREAM MULTI-MODAL PIPELINE
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {tools.map((t, idx) => {
              const Icon = t.icon;
              return (
                <motion.div 
                  key={t.title} 
                  initial={{ opacity: 0, y: 25 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: false, amount: 0.15 }}
                  transition={{ duration: 0.4, delay: idx * 0.08 }}
                  whileHover={{ scale: 1.02, y: -3 }}
                  className="p-5 bg-black border-2 border-white hover:border-amber-200 transition-colors duration-150 shadow-[4px_4px_0px_rgba(0,0,0,0.6)]"
                >
                  <div className="flex items-center justify-between mb-3">
                    <div className="w-8 h-8 bg-white text-black flex items-center justify-center font-bold">
                      <Icon className="w-4 h-4" />
                    </div>
                    <span className="font-mono-code text-xs text-white/40">{t.num}</span>
                  </div>
                  <h4 className="font-poster text-xl text-white uppercase mb-1">
                    {t.title}
                  </h4>
                  <div className="font-mono-code text-[11px] text-amber-200 font-bold mb-2">
                    {t.model}
                  </div>
                  <p className="text-xs text-gray-300 leading-relaxed font-display">
                    {t.desc}
                  </p>
                </motion.div>
              );
            })}
          </div>
        </motion.div>
      </div>
    </section>
  );
};
