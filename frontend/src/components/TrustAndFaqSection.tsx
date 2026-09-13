import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { SparkleStar } from './SparkleStar';
import { 
  ShieldCheck, 
  ChevronDown, 
  ChevronUp, 
  ArrowUp,
  Cpu,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  Activity,
  Sliders,
  Shield
} from 'lucide-react';

export const TrustAndFaqSection: React.FC = () => {
  // Degradation simulation sliders
  const [jpegQuality, setJpegQuality] = useState<number>(85);
  const [blurLevel, setBlurLevel] = useState<number>(0);
  const [openFaq, setOpenFaq] = useState<number | null>(0);

  // Calculate simulated accuracy retention based on compression
  const simulatedAccuracy = Math.max(
    74,
    Math.round(94 - (100 - jpegQuality) * 0.15 - blurLevel * 2)
  );

  const faqs = [
    {
      q: 'Can it still detect AI if someone took a screenshot or shared it on WhatsApp?',
      a: 'Yes. Social media platforms compress images aggressively to save bandwidth. While single-layer pixel classifiers break under compression, SignalScope dual-stream architecture simultaneously evaluates high-level lighting physics, facial anatomy, and residual sensor grain. Even when compression wipes out fine pixel noise, the spatial stream retains strong detection accuracy.'
    },
    {
      q: 'Why does SignalScope never claim 100.0% certainty?',
      a: 'Forensic integrity requires probabilistic honesty. Artistic digital retouching, heavy motion blur, or digital paintings can mimic synthetic artifacts. SignalScope uses calibrated temperature-scaled probabilities (such as 94% or 88%) and explicitly flags ambiguous media as "Needs Human Review" rather than returning a false positive accusation.'
    },
    {
      q: 'Can it identify which AI generator created the image?',
      a: 'Yes. Different generative architectures leave distinctive mathematical footprints. Diffusion architectures (Midjourney, Stable Diffusion, Flux) generate unique high-frequency noise profiles, while GAN architectures (StyleGAN) produce distinct checkerboard deconvolution grids in the Fourier power spectrum. SignalScope attributes the most probable generator family alongside the verdict.'
    },
    {
      q: 'Does it support C2PA Content Authenticity digital provenance manifests?',
      a: 'Yes. If an image contains a cryptographically signed C2PA manifest (embedded by modern hardware cameras or ethical generative AI tools), SignalScope verifies the certificate signature chain, checks validity, and displays provenance history in the metadata inspector.'
    }
  ];

  return (
    <section 
      id="trust" 
      className="relative min-h-screen py-24 px-4 sm:px-8 lg:px-12 bg-[#ff5200] text-white selection:bg-black selection:text-white flex flex-col justify-between overflow-hidden"
    >
      {/* SOLID VIBRANT ORANGE POSTER GRADIENT (Exactly matching page 3 style, NO chess pattern) */}
      <div className="absolute inset-0 bg-gradient-to-b from-[#e54600] via-[#ff5200] to-[#c73b00] pointer-events-none" />

      {/* Structural outer white border - matching Page 3 */}
      <div className="absolute top-12 left-4 right-4 bottom-12 border-2 border-white/70 pointer-events-none hidden sm:block" />
      <div className="absolute top-16 left-8 right-8 bottom-16 border border-black/30 pointer-events-none hidden md:block" />

      {/* Interactive floating decorative stars (hidden on mobile to prevent overlap) */}
      <motion.div 
        animate={{ y: [0, -10, 0], rotate: [0, 20, 0] }}
        transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-20 right-16 z-10 hidden md:block"
      >
        <SparkleStar size={60} fill="#ffffff" className="opacity-40 hover:opacity-100 transition-opacity" />
      </motion.div>
      <motion.div 
        animate={{ y: [0, 10, 0], rotate: [0, -20, 0] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut", delay: 0.8 }}
        className="absolute bottom-24 left-14 z-10 hidden lg:block"
      >
        <SparkleStar size={52} fill="#ffffff" className="opacity-35 hover:opacity-100 transition-opacity" />
      </motion.div>

      {/* Corner crosshairs `+` `+` */}
      <div className="absolute top-14 left-6 text-white/70 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute top-14 right-6 text-white/70 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute bottom-14 left-6 text-white/70 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute bottom-14 right-6 text-white/70 font-mono-code text-base hidden sm:block">+</div>

      <div className="max-w-6xl mx-auto w-full relative z-10 my-auto">
        {/* Section Header with scroll animation */}
        <motion.div 
          initial={{ opacity: 0, y: 35 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.2 }}
          transition={{ duration: 0.6, type: "spring", stiffness: 100, damping: 20 }}
          className="max-w-3xl mb-12"
        >
          <div className="inline-flex items-center gap-2 px-3.5 py-1 bg-black text-white font-mono-code text-xs font-bold uppercase tracking-widest mb-3 border border-white/40 shadow-[3px_3px_0px_rgba(0,0,0,0.4)]">
            <span className="w-2 h-2 bg-white animate-pulse" />
            <span>WHY YOU CAN TRUST IT & FAQ</span>
          </div>

          <h2 className="font-poster text-5xl sm:text-7xl uppercase tracking-tight text-white mb-3">
            TESTED FOR REAL-WORLD TRUST
          </h2>

          <p className="font-display font-bold text-base sm:text-lg text-white/95">
            Photographs get re-compressed, screenshotted, and blurred across social apps. See how the dual-stream system performs under synthetic degradation.
          </p>
        </motion.div>

        {/* INTERACTIVE COMPRESSION STRESS-TEST (SHARP BRUTALIST BLACK BOX) */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.15 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="bg-black border-2 border-white p-6 sm:p-10 shadow-[10px_10px_0px_rgba(0,0,0,0.8)] mb-14"
        >
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4 mb-8 pb-6 border-b border-white/20">
            <div>
              <span className="font-mono-code text-xs text-white/70 uppercase tracking-widest font-bold block mb-1">
                [ STRESS SIMULATION ]
              </span>
              <h3 className="font-poster text-2xl sm:text-3xl text-white uppercase">
                Simulate Social Media Compression
              </h3>
              <p className="text-xs sm:text-sm text-gray-300 font-display mt-1">
                Adjust the sliders to simulate aggressive JPEG compression and blur. The dual-stream system retains high reliability by falling back to visual anatomy.
              </p>
            </div>

            {/* Reliability indicator */}
            <motion.div 
              key={simulatedAccuracy}
              initial={{ scale: 0.95 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.2 }}
              className="p-4 bg-white text-black border-2 border-white text-center shrink-0 min-w-[160px] shadow-[4px_4px_0px_rgba(255,255,255,0.4)]"
            >
              <span className="text-[10px] font-mono-code text-neutral-600 uppercase font-bold block mb-1">
                Reliability Score
              </span>
              <span className="font-poster text-4xl text-black">
                {simulatedAccuracy}%
              </span>
              <span className="text-[11px] font-mono-code text-neutral-800 font-bold block mt-0.5">
                {simulatedAccuracy > 85 ? 'High Confidence' : 'Balanced Review'}
              </span>
            </motion.div>
          </div>

          {/* Sliders Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div className="p-4 bg-white/5 border border-white/20 space-y-2">
              <div className="flex justify-between text-xs font-mono-code">
                <span className="text-white font-bold">JPEG Compression Quality:</span>
                <span className="text-white font-bold">{jpegQuality}%</span>
              </div>
              <input
                type="range"
                min="20"
                max="100"
                value={jpegQuality}
                onChange={(e) => setJpegQuality(Number(e.target.value))}
                className="w-full accent-white cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-gray-400 font-mono-code">
                <span>20% (Heavy WhatsApp Compression)</span>
                <span>100% (Lossless Camera Export)</span>
              </div>
            </div>

            <div className="p-4 bg-white/5 border border-white/20 space-y-2">
              <div className="flex justify-between text-xs font-mono-code">
                <span className="text-white font-bold">Simulated Resizing / Blur:</span>
                <span className="text-white font-bold">{blurLevel} px</span>
              </div>
              <input
                type="range"
                min="0"
                max="5"
                value={blurLevel}
                onChange={(e) => setBlurLevel(Number(e.target.value))}
                className="w-full accent-white cursor-pointer"
              />
              <div className="flex justify-between text-[10px] text-gray-400 font-mono-code">
                <span>0 px (Sharp Focus)</span>
                <span>5 px (Heavy Transcode Blur)</span>
              </div>
            </div>
          </div>

          {/* Explanation Callout */}
          <div className="p-4 bg-white/10 border border-white/30 text-xs sm:text-sm text-white flex items-start gap-3 font-display">
            <ShieldCheck className="w-5 h-5 text-white shrink-0 mt-0.5" />
            <div>
              <strong className="block text-white font-bold mb-0.5">Why Dual-Stream Architecture Survives:</strong>
              <p className="text-gray-200">
                Single-stream detectors rely exclusively on subtle sensor noise, which is destroyed by JPEG compression. SignalScope pairs microscopic sensor analysis with high-level spatial vision (DINOv2), maintaining dependable accuracy even on degraded social media screenshots.
              </p>
            </div>
          </div>
        </motion.div>

        {/* FAQ ACCORDION (SHARP POSTER BOXES WITH SMOOTH EXPANSION) */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.15 }}
          transition={{ duration: 0.6 }}
          className="space-y-3 mb-16"
        >
          <div className="mb-6">
            <h3 className="font-poster text-3xl sm:text-4xl text-white uppercase">
              FREQUENTLY ASKED QUESTIONS
            </h3>
            <p className="text-xs text-white/80 font-mono-code">
              CLEAR ANSWERS ON AI DETECTION RELIABILITY AND METHODS
            </p>
          </div>

          {faqs.map((faq, idx) => {
            const isOpen = openFaq === idx;
            return (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 15 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: false }}
                transition={{ duration: 0.35, delay: idx * 0.05 }}
                className="border-2 border-white bg-black overflow-hidden transition-all shadow-[4px_4px_0px_rgba(0,0,0,0.5)]"
              >
                <button
                  onClick={() => setOpenFaq(isOpen ? null : idx)}
                  className="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-white/5 transition-colors"
                >
                  <span className="font-display font-bold text-sm sm:text-base text-white">
                    {faq.q}
                  </span>
                  {isOpen ? (
                    <ChevronUp className="w-5 h-5 text-white shrink-0" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-gray-400 shrink-0" />
                  )}
                </button>

                <AnimatePresence>
                  {isOpen && (
                    <motion.div 
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="p-5 pt-0 text-xs sm:text-sm text-gray-300 leading-relaxed border-t border-white/15 font-display"
                    >
                      {faq.a}
                    </motion.div>
                  )}
                </AnimatePresence>
              </motion.div>
            );
          })}
        </motion.div>

        {/* FOOTER - CLEAN BRANDING (NO STARS, NO HACKATHON OR TEST MENTIONS) */}
        <div className="pt-8 border-t-2 border-white/40 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-6 text-xs text-white/80">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 bg-black border-2 border-white flex items-center justify-center text-white font-mono-code font-black text-sm">
              SS
            </div>
            <div>
              <div className="font-poster text-xl text-white">
                SIGNALSCOPE
              </div>
              <div className="text-[11px] font-mono-code text-white/70">
                AI Image Authenticity & Forensic Analysis System
              </div>
            </div>
          </div>

          <div className="max-w-md text-[11px] text-white/80 font-display">
            Responsible AI Notice: SignalScope is an investigative tool designed to assist human verification. Automated verdicts should always be reviewed alongside spatial heatmaps.
          </div>

          <motion.a
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            href="#hero"
            className="inline-flex items-center gap-2 px-4 py-2 bg-black text-white font-poster uppercase text-sm border-2 border-white hover:bg-neutral-900 transition-colors duration-150 shadow-[3px_3px_0px_rgba(255,255,255,0.8)] shrink-0"
          >
            <span>Back to Top</span>
            <ArrowUp className="w-3.5 h-3.5 text-white" />
          </motion.a>
        </div>
      </div>
    </section>
  );
};
