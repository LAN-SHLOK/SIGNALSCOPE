import React, { useState, useEffect } from 'react';
import { SparkleStar } from './SparkleStar';
import { ArrowRight } from 'lucide-react';

interface NavbarProps {
  activeSection: string;
}

export const Navbar: React.FC<NavbarProps> = ({ activeSection }) => {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 30);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const getThemeAccent = () => {
    switch (activeSection) {
      case 'scanner':
        return {
          dot: 'bg-[#ede8dc]',
          text: 'text-[#ede8dc]',
          border: 'border-[#ede8dc]',
          btnBg: 'bg-[#ede8dc] hover:bg-white text-black',
        };
      case 'pipeline':
        return {
          dot: 'bg-[#ff4d5a]',
          text: 'text-[#ff4d5a]',
          border: 'border-[#ff4d5a]',
          btnBg: 'bg-white hover:bg-gray-200 text-black',
        };
      case 'trust':
        return {
          dot: 'bg-[#ff5200]',
          text: 'text-[#ff5200]',
          border: 'border-[#ff5200]',
          btnBg: 'bg-[#ff5200] hover:bg-[#ff6c24] text-white',
        };
      case 'hero':
      default:
        return {
          dot: 'bg-[#00e540]',
          text: 'text-[#00e540]',
          border: 'border-black',
          btnBg: 'bg-black hover:bg-neutral-900 text-[#00e540]',
        };
    }
  };

  const theme = getThemeAccent();

  const navItems = [
    { id: 'hero', label: 'INTRO', href: '#hero' },
    { id: 'scanner', label: 'SCAN & BATCH LAB', href: '#scanner' },
    { id: 'pipeline', label: 'HOW IT WORKS', href: '#pipeline' },
    { id: 'trust', label: 'WHY TRUST IT', href: '#trust' },
  ];

  return (
    <header
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? 'bg-black/95 backdrop-blur-md border-b-2 border-white/20 shadow-2xl py-2'
          : 'bg-transparent py-4'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-8 flex items-center justify-between">
        {/* Brand logo & title */}
        <a href="#hero" className="flex items-center gap-3 group">
          <div className="w-9 h-9 bg-black border-2 border-white flex items-center justify-center text-[#00e540] group-hover:scale-105 transition-transform">
            <SparkleStar size={22} fill="#00e540" />
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="font-poster text-xl tracking-wider text-white group-hover:text-[#00e540] transition-colors">
                SIGNALSCOPE
              </span>
              <span className="text-[10px] font-mono-code font-bold px-1.5 py-0.5 bg-white text-black border border-white">
                VERIFY
              </span>
            </div>
          </div>
        </a>

        {/* 4 Main Navigation Links */}
        <nav className="hidden md:flex items-center bg-black border-2 border-white/40 p-1">
          {navItems.map((item) => {
            const isActive = activeSection === item.id;
            return (
              <a
                key={item.id}
                href={item.href}
                className={`text-xs font-mono-code font-bold px-4 py-1.5 transition-colors duration-150 flex items-center gap-2 ${
                  isActive
                    ? 'bg-white text-black shadow-sm'
                    : 'text-gray-300 hover:text-white hover:bg-white/10'
                }`}
              >
                {isActive && (
                  <span className={`w-1.5 h-1.5 ${theme.dot}`} />
                )}
                <span>{item.label}</span>
              </a>
            );
          })}
        </nav>

        {/* Quick Launch CTA Button */}
        <div className="flex items-center gap-3">
          <a
            href="#scanner"
            className={`inline-flex items-center gap-2 px-5 py-2 font-poster uppercase text-sm tracking-wider border-2 border-white shadow-[3px_3px_0px_rgba(255,255,255,0.8)] hover:-translate-y-0.5 hover:shadow-[4px_4px_0px_rgba(255,255,255,1)] active:translate-y-0 active:shadow-[2px_2px_0px_rgba(255,255,255,0.8)] transition-[background-color,color,transform,box-shadow] duration-150 ease-out ${theme.btnBg}`}
          >
            <span>Scan Image</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </a>
        </div>
      </div>
    </header>
  );
};
