import React from 'react';
import { SparkleStar } from './SparkleStar';
import { ShieldCheck, Heart, Github, ExternalLink, ArrowUp } from 'lucide-react';

export const Footer: React.FC = () => {
  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  return (
    <footer className="bg-[#050806] border-t border-[#14281a] text-white pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Top footer row */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-8 border-b border-[#14281a]">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-[#00e540] flex items-center justify-center text-black font-black shadow-md shadow-[#00e540]/30">
              <SparkleStar size={24} fill="#000000" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-syne text-xl font-black tracking-tight text-white">
                  SIGNALSCOPE
                </span>
                <span className="text-[10px] font-mono-code font-bold px-2 py-0.5 rounded bg-[#00e540]/20 text-[#00e540] border border-[#00e540]/40">
                  FINAL IMPLEMENTATION (v3)
                </span>
              </div>
              <p className="text-xs text-gray-400 font-mono-code mt-0.5">
                SIH 2026 Internal Hackathon • Problem Statement 2 • L.J. Institute [C-433]
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <button
              onClick={scrollToTop}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#0e1611] hover:bg-[#142319] border border-[#1d3824] text-xs font-mono-code text-gray-300 hover:text-white transition-all"
            >
              <span>Back to Top</span>
              <ArrowUp className="w-3.5 h-3.5 text-[#00e540]" />
            </button>
          </div>
        </div>

        {/* Responsible AI Disclaimer */}
        <div className="py-6 border-b border-[#14281a] text-xs text-gray-400 leading-relaxed">
          <div className="flex items-start gap-2.5">
            <ShieldCheck className="w-4 h-4 text-[#00e540] shrink-0 mt-0.5" />
            <div>
              <strong className="text-gray-200">Ethical & Responsible Media Forensics:</strong>
              <p className="mt-0.5 text-[11px] text-gray-400">
                SignalScope outputs calibrated probabilistic likelihoods, not infallible binary judgments. Degradation from multi-generational compression, social media transcoding, or low-resolution crops can obscure sensor fingerprints. Automated scores should always be complemented by provenance metadata (C2PA / EXIF) and human editorial verification.
              </p>
            </div>
          </div>
        </div>

        {/* Bottom copyright & attribution */}
        <div className="pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-gray-500 font-mono-code gap-3">
          <div>
            © 2026 SignalScope Team • MIT License • Built for SIH 2026
          </div>
          <div className="flex items-center gap-4">
            <span>DINOv2 ViT-L/14</span>
            <span>•</span>
            <span>Multi-Colorspace SRM</span>
            <span>•</span>
            <span>LightGBM Stacking</span>
          </div>
        </div>
      </div>
    </footer>
  );
};
