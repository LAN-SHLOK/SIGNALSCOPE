/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { motion, useScroll, useSpring } from 'motion/react';
import { Navbar } from './components/Navbar';
import { HeroSection } from './components/HeroSection';
import { ScannerSection } from './components/ScannerSection';
import { PipelineSection } from './components/PipelineSection';
import { TrustAndFaqSection } from './components/TrustAndFaqSection';

export default function App() {
  const [activeSection, setActiveSection] = useState<string>('hero');
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, {
    stiffness: 120,
    damping: 24,
    restDelta: 0.001
  });

  useEffect(() => {
    const handleScroll = () => {
      const sectionIds = ['hero', 'scanner', 'pipeline', 'trust'];
      const scrollPosition = window.scrollY + 200;

      for (const id of sectionIds) {
        const el = document.getElementById(id);
        if (el) {
          const top = el.offsetTop;
          const height = el.offsetHeight;
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveSection(id);
            break;
          }
        }
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const getProgressColor = () => {
    switch (activeSection) {
      case 'scanner':
        return 'bg-black';
      case 'pipeline':
        return 'bg-white';
      case 'trust':
        return 'bg-black';
      case 'hero':
      default:
        return 'bg-black';
    }
  };

  return (
    <div className="min-h-screen bg-[#060a08] text-white flex flex-col selection:bg-[#00e540] selection:text-black relative">
      {/* Dynamic Scroll Progress Bar visible throughout the app */}
      <motion.div
        style={{ scaleX }}
        className={`fixed top-0 left-0 right-0 h-1 z-[70] origin-left transition-colors duration-300 ${getProgressColor()}`}
      />

      {/* Sticky top navigation bar with dynamic theme color reflecting active section */}
      <Navbar activeSection={activeSection} />

      {/* Main Single Page Content - 4 Main Sections */}
      <main className="flex-1">
        {/* SECTION 1: Title & What It Does with small 1-line description (Electric Green Star World) */}
        <HeroSection />

        {/* SECTION 2: Live Analysis (Single Image + Batch Folder/ZIP in SAME section) (Editorial Cream Lab World) */}
        <ScannerSection />

        {/* SECTION 3: About & How the Pipeline Works in Simple Words (Japanese Brutalist Crimson Red World) */}
        <PipelineSection />

        {/* SECTION 4: Why You Can Trust It, Stress-Testing, FAQ & Attribution (Poster Orange World) */}
        <TrustAndFaqSection />
      </main>
    </div>
  );
}
