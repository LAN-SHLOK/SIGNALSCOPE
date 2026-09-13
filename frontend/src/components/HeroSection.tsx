import React from 'react';
import { motion, useScroll, useTransform } from 'motion/react';
import { SparkleStar } from './SparkleStar';
import { ArrowDown, Camera, FolderSync, ShieldCheck } from 'lucide-react';

export const HeroSection: React.FC = () => {
  const { scrollY } = useScroll();
  // Parallax transformations triggered upon scrolling
  const wireframeRotate = useTransform(scrollY, [0, 800], [12, 35]);
  const heroContentY = useTransform(scrollY, [0, 800], [0, 50]);

  return (
    <section
      id="hero"
      className="relative min-h-screen w-full flex flex-col justify-between px-4 sm:px-8 lg:px-12 pt-24 pb-12 overflow-hidden bg-[#00e540] text-black selection:bg-white selection:text-black"
    >
      {/* FULL-BLEED BACKGROUND GRAPHICS & STRUCTURAL WIREFRAMES */}

      {/* Outer structural framing border with sharp edges matching Page 3 & 4 */}
      <div className="absolute top-20 left-4 right-4 bottom-6 border-2 border-black/80 pointer-events-none hidden sm:block" />
      <div className="absolute top-24 left-8 right-8 bottom-10 border border-white/60 pointer-events-none hidden md:block" />

      {/* Corner crosshairs `+` `+` */}
      <div className="absolute top-22 left-6 text-black/70 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute top-22 right-6 text-black/70 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute bottom-8 left-6 text-black/70 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute bottom-8 right-6 text-black/70 font-mono-code text-base hidden sm:block">+</div>

      {/* Diagonal geometric wireframes that rotate on scroll */}
      <motion.div
        style={{ rotate: wireframeRotate }}
        className="absolute -top-16 -right-16 w-80 h-80 border-2 border-black/40 pointer-events-none hidden lg:block"
      />
      <motion.div
        style={{ rotate: wireframeRotate }}
        className="absolute -top-12 -right-12 w-80 h-80 border-2 border-white/60 pointer-events-none hidden lg:block"
      />

      {/* Interactive floating decorative stars matching other pages */}
      <motion.div
        animate={{ y: [0, -14, 0], rotate: [0, 12, 0] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-28 sm:top-24 right-4 sm:right-16 lg:right-24 z-10 pointer-events-auto"
      >
        <SparkleStar size={75} fill="#000000" className="opacity-85 hover:opacity-100 transition-opacity cursor-pointer drop-shadow-md sm:hidden" />
        <SparkleStar size={145} fill="#000000" className="opacity-90 hover:opacity-100 transition-opacity cursor-pointer drop-shadow-md hidden sm:inline-block" />
      </motion.div>

      <motion.div
        animate={{ y: [0, 12, 0], rotate: [0, -15, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 0.6 }}
        className="absolute top-1/2 -translate-y-1/2 right-6 sm:right-12 lg:right-20 z-10 pointer-events-auto hidden md:block"
      >
        <SparkleStar size={95} fill="#000000" className="opacity-80 hover:opacity-100 transition-opacity cursor-pointer" />
      </motion.div>

      <motion.div
        animate={{ y: [0, -10, 0], rotate: [0, 10, 0] }}
        transition={{ duration: 4.5, repeat: Infinity, ease: "easeInOut", delay: 1 }}
        className="absolute bottom-20 sm:bottom-24 right-8 sm:right-28 lg:right-40 z-10 pointer-events-auto hidden sm:block"
      >
        <SparkleStar size={55} fill="#000000" className="opacity-75 hover:opacity-100 transition-opacity cursor-pointer" />
      </motion.div>

      {/* Top Banner Tag */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 pt-4">
        <motion.div
          initial={{ opacity: 0, y: -15 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-none bg-black text-[#00e540] font-mono-code text-xs font-black uppercase tracking-widest border border-black shadow-[3px_3px_0px_rgba(0,0,0,0.3)]"
        >
          <span className="w-2 h-2 rounded-full bg-[#00e540] animate-ping" />
          <span>REAL CAMERA PHOTO OR AI GENERATED?</span>
        </motion.div>
      </div>

      {/* MAIN HERO CONTENT - Proportionally balanced bold poster typography */}
      <motion.div style={{ y: heroContentY }} className="relative z-20 max-w-5xl my-auto py-8">
        <div className="overflow-hidden mb-6">
          <motion.h1
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
            className="font-poster text-6xl sm:text-7xl md:text-8xl lg:text-[7rem] xl:text-[8rem] leading-[0.88] tracking-tight uppercase text-black"
          >
            SIGNAL<br />
            SCOPE
          </motion.h1>
        </div>

        {/* What it does: Small one-line description in simple words */}
        <motion.p
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.15, ease: [0.16, 1, 0.3, 1] }}
          className="font-display font-bold text-xl sm:text-2xl lg:text-3xl text-black leading-tight max-w-2xl mb-8 border-l-4 border-black pl-4"
        >
          Drop any picture to instantly see if it was taken by a real camera or generated by AI — with clear heatmaps and honest explanations.
        </motion.p>

        {/* 3 Simple Badges with hover micro-physics */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.25, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-wrap gap-3 mb-10 max-w-xl"
        >
          <motion.div
            whileHover={{ y: -2 }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            className="bg-black text-white px-3.5 py-2 font-mono-code font-bold text-xs uppercase flex items-center gap-2 border border-black shadow-[2px_2px_0px_rgba(0,0,0,0.3)] transition-colors duration-150 cursor-default"
          >
            <Camera className="w-3.5 h-3.5 text-[#00e540]" />
            <span>Checks Physical Camera Lenses</span>
          </motion.div>
          <motion.div
            whileHover={{ y: -2 }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            className="bg-black text-white px-3.5 py-2 font-mono-code font-bold text-xs uppercase flex items-center gap-2 border border-black shadow-[2px_2px_0px_rgba(0,0,0,0.3)] transition-colors duration-150 cursor-default"
          >
            <ShieldCheck className="w-3.5 h-3.5 text-[#00e540]" />
            <span>Highlights Fake AI Regions</span>
          </motion.div>
          <motion.div
            whileHover={{ y: -2 }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            className="bg-white text-black px-3.5 py-2 font-mono-code font-bold text-xs uppercase flex items-center gap-2 border-2 border-black shadow-[2px_2px_0px_rgba(0,0,0,1)] transition-colors duration-150 cursor-default"
          >
            <FolderSync className="w-3.5 h-3.5" />
            <span>Single & Batch ZIP Scanning</span>
          </motion.div>
        </motion.div>

        {/* Launch CTAs with hover physics */}
        <motion.div
          initial={{ opacity: 0, y: 25 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 0.35, ease: [0.16, 1, 0.3, 1] }}
          className="flex flex-wrap items-center gap-4"
        >
          <motion.a
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            href="#scanner"
            className="inline-flex items-center gap-3 px-8 py-4 bg-black text-[#00e540] hover:bg-neutral-900 font-poster text-xl tracking-wider uppercase transition-colors duration-150 shadow-[6px_6px_0px_rgba(255,255,255,0.9)] cursor-pointer"
          >
            <span>Scan An Image Now</span>
            <ArrowDown className="w-5 h-5 text-[#00e540]" />
          </motion.a>

          <motion.a
            whileHover={{ scale: 1.02, y: -2 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.1, ease: "easeOut" }}
            href="#pipeline"
            className="inline-flex items-center gap-2 px-6 py-4 bg-white/70 hover:bg-white text-black font-display font-bold text-sm sm:text-base uppercase tracking-wider transition-colors duration-150 border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)] cursor-pointer"
          >
            <span>How It Works (In Simple Words)</span>
          </motion.a>
        </motion.div>
      </motion.div>

      {/* Bottom Ticker Bar */}
      <div className="relative z-10 border-t-2 border-black/80 pt-3 flex flex-col sm:flex-row items-start sm:items-center justify-between text-xs font-mono-code text-black font-bold gap-2">
        <div className="flex items-center gap-4">
          <span>NO CODING OR EXPERIENCE REQUIRED</span>
          <span className="hidden md:inline">•</span>
          <span className="hidden md:inline">100% PRIVATE IN-BROWSER PREVIEW</span>
        </div>
        <div>
          <span>SCROLL DOWN TO INSPECT MEDIA</span>
        </div>
      </div>
    </section>
  );
};
