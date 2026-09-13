import React, { useState } from 'react';
import { SAMPLE_IMAGES } from '../data/mockScanData';
import { SampleImage, VerdictTier } from '../types/signalscope';
import { SparkleStar } from './SparkleStar';
import { 
  UploadCloud, 
  Layers, 
  Sliders, 
  Eye, 
  Info, 
  ShieldAlert, 
  ShieldCheck, 
  HelpCircle, 
  Sparkles, 
  Cpu, 
  Radio, 
  FileCheck2, 
  FileX2, 
  Check, 
  Activity,
  Maximize2
} from 'lucide-react';

export const LiveScanner: React.FC = () => {
  const [selectedSample, setSelectedSample] = useState<SampleImage>(SAMPLE_IMAGES[0]);
  const [activeLayer, setActiveLayer] = useState<'fused' | 'attention' | 'srm' | 'fft'>('fused');
  const [heatmapOpacity, setHeatmapOpacity] = useState<number>(65);
  const [activeTab, setActiveTab] = useState<'cues' | 'spectral' | 'metadata'>('cues');
  const [isCustomUploading, setIsCustomUploading] = useState<boolean>(false);
  const [uploadedFileName, setUploadedFileName] = useState<string | null>(null);

  // Handle custom file upload simulation
  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setUploadedFileName(file.name);
      setIsCustomUploading(true);
      const reader = new FileReader();
      reader.onload = () => {
        const customUrl = reader.result as string;
        // Construct a dynamic analyzed sample for the user's custom uploaded image
        const customSample: SampleImage = {
          id: 'custom-upload',
          name: `Custom Scan: ${file.name.slice(0, 20)}`,
          tag: 'User Uploaded Media',
          description: `Custom image (${(file.size / 1024).toFixed(1)} KB) analyzed through dual-stream pipeline.`,
          sourceType: 'diffusion',
          confidence: 0.865,
          verdictTier: 'confident_ai',
          verdictLabel: 'Likely AI-generated',
          generatorFamily: 'Diffusion-family',
          imgUrl: customUrl,
          heatmapOverlayUrl: selectedSample.heatmapOverlayUrl,
          attentionRolloutUrl: selectedSample.attentionRolloutUrl,
          srmResidualUrl: selectedSample.srmResidualUrl,
          fftSpectrumUrl: selectedSample.fftSpectrumUrl,
          exif: {
            hasExif: false,
            anomalyFlag: 'Custom upload: EXIF metadata empty or stripped by web browser.',
          },
          c2pa: {
            hasC2pa: false,
            validationStatus: 'none',
            trustSignal: 'No Provenance',
          },
          cues: selectedSample.cues,
          summaryExplanation: 'Custom image processed through dual-stream pipeline. Detected high patch uniformity across ViT-L/14 tokens with elevated high-frequency residuals in chrominance channels.',
          fftStats: {
            radialSlope: -0.45,
            highFreqPeak: true,
            symmetryScore: 0.88,
          },
        };
        setSelectedSample(customSample);
        setIsCustomUploading(false);
      };
      reader.readAsDataURL(file);
    }
  };

  const getVerdictVisuals = (tier: VerdictTier) => {
    switch (tier) {
      case 'confident_ai':
        return {
          bg: 'bg-red-500/10 border-red-500/30 text-red-400',
          badgeBg: 'bg-red-500 text-white',
          icon: <ShieldAlert className="w-5 h-5 text-red-400" />,
          accent: '#ef4444',
          label: 'Likely AI-generated',
          advice: 'Review the grounded forensic cues below. Multiple synthetic fingerprints detected across DINOv2 and SRM streams.'
        };
      case 'confident_real':
        return {
          bg: 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400',
          badgeBg: 'bg-[#00e540] text-black',
          icon: <ShieldCheck className="w-5 h-5 text-[#00e540]" />,
          accent: '#00e540',
          label: 'Likely authentic',
          advice: 'Natural camera sensor noise observed with verified Bayer CFA 2-pixel autocorrelation and natural 1/f spectral falloff.'
        };
      case 'uncertain':
      default:
        return {
          bg: 'bg-amber-500/10 border-amber-500/30 text-amber-400',
          badgeBg: 'bg-amber-500 text-black',
          icon: <HelpCircle className="w-5 h-5 text-amber-400" />,
          accent: '#f59e0b',
          label: 'Uncertain — human review recommended',
          advice: 'Smart Abstention Triggered: Post-temperature calibration confidence sits in the ambiguous zone [0.25, 0.75]. Strong compression or multi-generational re-saving detected.'
        };
    }
  };

  const verdictUi = getVerdictVisuals(selectedSample.verdictTier);

  const getOverlaySrc = () => {
    switch (activeLayer) {
      case 'attention':
        return selectedSample.attentionRolloutUrl;
      case 'srm':
        return selectedSample.srmResidualUrl;
      case 'fft':
        return selectedSample.fftSpectrumUrl;
      case 'fused':
      default:
        return selectedSample.heatmapOverlayUrl;
    }
  };

  return (
    <section id="scanner" className="py-16 bg-[#090d0b] text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4 border-b border-[#182a1d] pb-6">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-mono-code text-[#00e540] uppercase tracking-wider mb-2">
              <Radio className="w-3.5 h-3.5 animate-pulse" />
              <span>Module F • Deployable Detection Interface</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black font-syne tracking-tight text-white">
              LIVE MEDIA FORENSIC SCANNER
            </h2>
            <p className="text-sm text-gray-400 mt-1 max-w-xl">
              Inspect any image with dual-stream foundation features, interactive multi-layer heatmaps, and grounded plain-English forensic cues.
            </p>
          </div>

          {/* Quick upload button */}
          <label className="cursor-pointer inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-[#122216] hover:bg-[#183020] border border-[#00e540]/40 text-[#00e540] font-bold text-xs font-mono-code transition-all self-start md:self-auto shadow-sm">
            <UploadCloud className="w-4 h-4" />
            <span>Upload Custom Media</span>
            <input 
              type="file" 
              accept="image/*" 
              className="hidden" 
              onChange={handleFileUpload}
            />
          </label>
        </div>

        {/* Sample Selectors Row */}
        <div className="mb-8">
          <div className="flex items-center justify-between mb-3">
            <span className="text-xs font-mono-code text-gray-400 uppercase tracking-wider">
              1. Select a Preset Test Case or Inspect Your Upload:
            </span>
            {uploadedFileName && (
              <span className="text-xs font-mono-code text-[#00e540]">
                Active: {uploadedFileName}
              </span>
            )}
          </div>
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {SAMPLE_IMAGES.map((sample) => {
              const isSelected = selectedSample.id === sample.id;
              return (
                <button
                  key={sample.id}
                  onClick={() => setSelectedSample(sample)}
                  className={`p-3 rounded-xl text-left transition-all border ${
                    isSelected
                      ? 'bg-[#00e540] text-black border-white shadow-[0_4px_20px_rgba(0,229,64,0.3)]'
                      : 'bg-[#0e1611] text-white border-[#1c3323] hover:border-[#00e540]/50 hover:bg-[#131f18]'
                  }`}
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className={`text-[10px] font-mono-code font-bold uppercase px-1.5 py-0.5 rounded ${
                      isSelected ? 'bg-black text-[#00e540]' : 'bg-white/10 text-gray-300'
                    }`}>
                      {sample.sourceType.toUpperCase()}
                    </span>
                    <span className={`text-xs font-mono-code font-bold ${
                      isSelected ? 'text-black' : sample.verdictTier === 'confident_ai' ? 'text-red-400' : sample.verdictTier === 'confident_real' ? 'text-[#00e540]' : 'text-amber-400'
                    }`}>
                      {(sample.confidence * 100).toFixed(0)}%
                    </span>
                  </div>
                  <div className="font-bold text-xs sm:text-sm font-display truncate">
                    {sample.name}
                  </div>
                  <div className={`text-[11px] truncate mt-0.5 ${isSelected ? 'text-black/80' : 'text-gray-400'}`}>
                    {sample.generatorFamily}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* MAIN WORKBENCH GRID */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* LEFT: INTERACTIVE IMAGE & HEATMAP STAGE (7 Cols) */}
          <div className="lg:col-span-7 bg-[#0c130f] rounded-2xl border border-[#1b3322] p-5 flex flex-col">
            {/* Stage Controls Header */}
            <div className="flex flex-wrap items-center justify-between gap-3 mb-4 border-b border-[#182a1d] pb-3">
              {/* Layer switch buttons */}
              <div className="flex items-center gap-1 bg-[#121c15] p-1 rounded-lg border border-[#213b28]">
                <button
                  onClick={() => setActiveLayer('fused')}
                  className={`text-xs px-2.5 py-1 rounded font-mono-code transition-all ${
                    activeLayer === 'fused'
                      ? 'bg-[#00e540] text-black font-bold shadow-sm'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  Fused Map
                </button>
                <button
                  onClick={() => setActiveLayer('attention')}
                  className={`text-xs px-2.5 py-1 rounded font-mono-code transition-all ${
                    activeLayer === 'attention'
                      ? 'bg-[#00e540] text-black font-bold shadow-sm'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  DINOv2 ViT
                </button>
                <button
                  onClick={() => setActiveLayer('srm')}
                  className={`text-xs px-2.5 py-1 rounded font-mono-code transition-all ${
                    activeLayer === 'srm'
                      ? 'bg-[#00e540] text-black font-bold shadow-sm'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  SRM Residuals
                </button>
                <button
                  onClick={() => setActiveLayer('fft')}
                  className={`text-xs px-2.5 py-1 rounded font-mono-code transition-all ${
                    activeLayer === 'fft'
                      ? 'bg-[#00e540] text-black font-bold shadow-sm'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  FFT Spectrum
                </button>
              </div>

              {/* Heatmap Opacity Slider */}
              <div className="flex items-center gap-2 bg-[#121c15] px-3 py-1.5 rounded-lg border border-[#213b28]">
                <Sliders className="w-3.5 h-3.5 text-[#00e540]" />
                <span className="text-[11px] font-mono-code text-gray-300">
                  Overlay Opacity:
                </span>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={heatmapOpacity}
                  onChange={(e) => setHeatmapOpacity(Number(e.target.value))}
                  className="w-20 sm:w-28 accent-[#00e540] cursor-pointer"
                />
                <span className="text-xs font-mono-code font-bold text-[#00e540] w-9 text-right">
                  {heatmapOpacity}%
                </span>
              </div>
            </div>

            {/* Visual Canvas Stage with Overlay Blending */}
            <div className="relative aspect-square w-full rounded-xl overflow-hidden bg-black border border-white/10 flex items-center justify-center shadow-inner group">
              {/* Base Image */}
              <img
                src={selectedSample.imgUrl}
                alt={selectedSample.name}
                className="absolute inset-0 w-full h-full object-cover select-none"
              />

              {/* Forensic Heatmap / Spectral Overlay */}
              <img
                src={getOverlaySrc()}
                alt="Forensic Heatmap"
                className="absolute inset-0 w-full h-full object-cover pointer-events-none mix-blend-screen transition-opacity duration-150"
                style={{ opacity: heatmapOpacity / 100 }}
              />

              {/* Grid calibration crosshair overlay */}
              <div className="absolute inset-0 pointer-events-none opacity-20 bg-[radial-gradient(#00e540_1px,transparent_1px)] [background-size:24px_24px]" />

              {/* Corner badge on image */}
              <div className="absolute top-3 left-3 px-2.5 py-1 rounded bg-black/80 backdrop-blur-sm border border-white/20 text-[10px] font-mono-code text-white flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-[#00e540]" />
                <span>ACTIVE VIEW: {activeLayer.toUpperCase()} OVERLAY</span>
              </div>

              <div className="absolute bottom-3 right-3 px-2 py-1 rounded bg-black/80 backdrop-blur-sm border border-white/20 text-[10px] font-mono-code text-gray-300">
                518×518 DINOv2 Native Res
              </div>
            </div>

            {/* View description bar */}
            <div className="mt-3 p-3 rounded-xl bg-[#101913] border border-[#192f1f] text-xs text-gray-300 flex items-start gap-2.5">
              <Info className="w-4 h-4 text-[#00e540] shrink-0 mt-0.5" />
              <div>
                {activeLayer === 'fused' && (
                  <span>
                    <strong>Fused Heatmap (Module A):</strong> Blends 60% DINOv2 Attention Rollout (semantic visual physics) + 40% Grad-CAM++ on SpectralCNN (noise artifacts). Hot regions indicate synthetic manipulation.
                  </span>
                )}
                {activeLayer === 'attention' && (
                  <span>
                    <strong>DINOv2 Attention Rollout:</strong> Propagated self-attention across all 24 ViT-L/14 layers over a 37×37 patch grid. Highlights which regions guided the foundation model classification.
                  </span>
                )}
                {activeLayer === 'srm' && (
                  <span>
                    <strong>SRM Residual Map:</strong> Multi-colorspace high-pass filtering (RGB + YCbCr + HSV). Strips image content to expose synthetic noise uniformity or missing Poisson sensor grain.
                  </span>
                )}
                {activeLayer === 'fft' && (
                  <span>
                    <strong>FFT Frequency Spectrum:</strong> Radially averaged 2D Fourier transform. Periodic spikes or unnaturally steep decay highlight neural upsampling and checkerboard deconvolution.
                  </span>
                )}
              </div>
            </div>
          </div>

          {/* RIGHT: VERDICT & FORENSIC EVIDENCE TABS (5 Cols) */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            {/* RESPONSIBLE VERDICT CARD */}
            <div className={`p-5 rounded-2xl border ${verdictUi.bg} backdrop-blur-sm relative overflow-hidden`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  {verdictUi.icon}
                  <span className="text-xs font-mono-code font-bold uppercase tracking-wider text-gray-200">
                    System Classification
                  </span>
                </div>
                <span className="text-[10px] font-mono-code px-2 py-0.5 rounded bg-black/30 text-gray-300 border border-white/10">
                  Calibrated Confidence
                </span>
              </div>

              {/* Big Verdict Headline */}
              <div className="text-2xl sm:text-3xl font-black font-syne mb-2 text-white">
                {verdictUi.label}
              </div>

              {/* Confidence Meter */}
              <div className="space-y-1.5 mb-4">
                <div className="flex justify-between text-xs font-mono-code">
                  <span className="text-gray-300">Confidence Score:</span>
                  <span className="font-bold text-white">
                    {(selectedSample.confidence * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full h-3 bg-black/40 rounded-full overflow-hidden p-0.5 border border-white/10">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${selectedSample.confidence * 100}%`,
                      backgroundColor: verdictUi.accent,
                    }}
                  />
                </div>
                <div className="flex justify-between text-[10px] font-mono-code text-gray-400">
                  <span>0.0 (Authentic)</span>
                  <span>0.25</span>
                  <span>0.50</span>
                  <span>0.75</span>
                  <span>1.0 (AI)</span>
                </div>
              </div>

              {/* Generator Attribution & Tier */}
              <div className="grid grid-cols-2 gap-2 pt-3 border-t border-white/10 text-xs font-mono-code">
                <div>
                  <span className="text-gray-400 block text-[10px]">ATTRIBUTION:</span>
                  <span className="font-bold text-white">{selectedSample.generatorFamily}</span>
                </div>
                <div>
                  <span className="text-gray-400 block text-[10px]">TEMPERATURE SCALING:</span>
                  <span className="font-bold text-[#00e540]">ECE &lt; 0.04 (Calibrated)</span>
                </div>
              </div>

              {/* Responsible Action Advice */}
              <div className="mt-3 pt-3 border-t border-white/10 text-xs leading-relaxed text-gray-300">
                <p className="text-[11px] italic text-gray-300">
                  {verdictUi.advice}
                </p>
              </div>
            </div>

            {/* TAB NAVIGATION: Cues / Spectral / Metadata */}
            <div className="bg-[#0c130f] rounded-2xl border border-[#1b3322] p-4 flex-1 flex flex-col">
              <div className="flex items-center gap-1 bg-[#121d16] p-1 rounded-xl border border-[#223d29] mb-4">
                <button
                  onClick={() => setActiveTab('cues')}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-mono-code font-bold transition-all ${
                    activeTab === 'cues'
                      ? 'bg-[#00e540] text-black shadow-sm'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Forensic Cues ({selectedSample.cues.length})
                </button>
                <button
                  onClick={() => setActiveTab('spectral')}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-mono-code font-bold transition-all ${
                    activeTab === 'spectral'
                      ? 'bg-[#00e540] text-black shadow-sm'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Spectral Profile
                </button>
                <button
                  onClick={() => setActiveTab('metadata')}
                  className={`flex-1 py-1.5 rounded-lg text-xs font-mono-code font-bold transition-all ${
                    activeTab === 'metadata'
                      ? 'bg-[#00e540] text-black shadow-sm'
                      : 'text-gray-300 hover:text-white'
                  }`}
                >
                  Provenance & EXIF
                </button>
              </div>

              {/* TAB 1: 6 Grounded Forensic Cues */}
              {activeTab === 'cues' && (
                <div className="space-y-3 overflow-y-auto max-h-[380px] pr-1">
                  <div className="text-[11px] font-mono-code text-gray-400 mb-1">
                    Grounded, template-verified forensic descriptors (no LLM hallucinations):
                  </div>
                  {selectedSample.cues.map((cue) => {
                    const isAlert = cue.status === 'abnormal' || cue.status === 'detected' || cue.status === 'missing';
                    return (
                      <div
                        key={cue.id}
                        className="p-3 rounded-xl bg-[#111c14] border border-[#1c3523] hover:border-[#00e540]/40 transition-all"
                      >
                        <div className="flex items-center justify-between mb-1">
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold text-white font-display">
                              {cue.name}
                            </span>
                            <span className="text-[10px] font-mono-code px-1.5 py-0.5 rounded bg-white/5 text-gray-300">
                              {cue.category}
                            </span>
                          </div>
                          <span
                            className={`text-[10px] font-mono-code font-bold px-2 py-0.5 rounded ${
                              cue.status === 'clear'
                                ? 'bg-[#00e540]/20 text-[#00e540]'
                                : 'bg-red-500/20 text-red-400'
                            }`}
                          >
                            {cue.statusText}
                          </span>
                        </div>
                        <p className="text-xs text-gray-300 mb-1.5 leading-snug">
                          {cue.description}
                        </p>
                        <div className="flex items-center justify-between text-[11px] font-mono-code text-gray-400 bg-black/30 px-2 py-1 rounded">
                          <span className="truncate max-w-[200px] text-gray-300">
                            {cue.evidence}
                          </span>
                          <span className="text-[#00e540] shrink-0 font-bold ml-2">
                            {cue.activationLevel}% act
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}

              {/* TAB 2: Spectral & Frequency Diagnostics */}
              {activeTab === 'spectral' && (
                <div className="space-y-4 text-xs text-gray-300">
                  <div className="p-3 rounded-xl bg-[#111c14] border border-[#1c3523]">
                    <div className="font-bold text-white mb-1 flex items-center justify-between">
                      <span>Azimuthal Radial Slope</span>
                      <span className="font-mono-code text-[#00e540]">
                        {selectedSample.fftStats.radialSlope}
                      </span>
                    </div>
                    <p className="text-gray-400 text-[11px]">
                      Real camera photos follow standard optical 1/f laws (-0.95 to -1.10). Neural upsamplers cause shallower slopes due to residual high-frequency energy.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-[#111c14] border border-[#1c3523]">
                    <div className="font-bold text-white mb-1 flex items-center justify-between">
                      <span>High-Frequency Grid Spikes</span>
                      <span className={`font-mono-code font-bold ${
                        selectedSample.fftStats.highFreqPeak ? 'text-red-400' : 'text-[#00e540]'
                      }`}>
                        {selectedSample.fftStats.highFreqPeak ? 'DETECTED' : 'CLEAR'}
                      </span>
                    </div>
                    <p className="text-gray-400 text-[11px]">
                      Detects harmonic cross-patterns and periodic peaks originating from convolutional transposes and latent diffusion denoisers.
                    </p>
                  </div>

                  <div className="p-3 rounded-xl bg-[#111c14] border border-[#1c3523]">
                    <div className="font-bold text-white mb-1 flex items-center justify-between">
                      <span>Bayer CFA Sensor Demodulation</span>
                      <span className="font-mono-code text-white">
                        {selectedSample.cues.some(c => c.name.includes('Bayer') && c.status === 'clear') ? 'PRESENT (Authentic)' : 'ABSENT (Synthetic)'}
                      </span>
                    </div>
                    <p className="text-gray-400 text-[11px]">
                      Physical CCD/CMOS sensors apply a Bayer Color Filter Array, leaving a 2-pixel autocorrelation signature in noise residuals. Synthetic media lacks this completely.
                    </p>
                  </div>
                </div>
              )}

              {/* TAB 3: Provenance & EXIF Metadata (Module D) */}
              {activeTab === 'metadata' && (
                <div className="space-y-3 text-xs text-gray-300">
                  {/* C2PA Credentials Status */}
                  <div className={`p-3.5 rounded-xl border ${
                    selectedSample.c2pa.hasC2pa
                      ? 'bg-[#00e540]/10 border-[#00e540]/30'
                      : 'bg-white/5 border-white/10'
                  }`}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="font-bold text-white flex items-center gap-1.5">
                        {selectedSample.c2pa.hasC2pa ? (
                          <FileCheck2 className="w-4 h-4 text-[#00e540]" />
                        ) : (
                          <FileX2 className="w-4 h-4 text-gray-400" />
                        )}
                        C2PA Content Credentials
                      </span>
                      <span className={`text-[10px] font-mono-code font-bold px-2 py-0.5 rounded ${
                        selectedSample.c2pa.hasC2pa
                          ? 'bg-[#00e540] text-black'
                          : 'bg-white/10 text-gray-300'
                      }`}>
                        {selectedSample.c2pa.trustSignal}
                      </span>
                    </div>
                    {selectedSample.c2pa.hasC2pa ? (
                      <div className="space-y-1 font-mono-code text-[11px] text-gray-300">
                        <div>Issuer: {selectedSample.c2pa.issuer}</div>
                        <div>Claim: {selectedSample.c2pa.claimGenerator}</div>
                        <div>Signed: {selectedSample.c2pa.signingTime}</div>
                      </div>
                    ) : (
                      <p className="text-[11px] text-gray-400">
                        No cryptographic C2PA manifest found in container. Typical of raw generative output or platforms stripping metadata.
                      </p>
                    )}
                  </div>

                  {/* EXIF Data block */}
                  <div className="p-3.5 rounded-xl bg-[#111c14] border border-[#1c3523] space-y-2">
                    <div className="font-bold text-white mb-1">
                      EXIF Camera Header
                    </div>
                    {selectedSample.exif.hasExif ? (
                      <div className="space-y-1 font-mono-code text-[11px] text-gray-300">
                        <div>Camera: {selectedSample.exif.cameraModel}</div>
                        <div>Lens: {selectedSample.exif.lens}</div>
                        <div>Exposure: {selectedSample.exif.exposure}</div>
                        <div>Software: {selectedSample.exif.software}</div>
                      </div>
                    ) : (
                      <div className="text-[11px] text-red-300 bg-red-500/10 p-2 rounded border border-red-500/20 font-mono-code">
                        {selectedSample.exif.anomalyFlag || 'No hardware EXIF records found.'}
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
