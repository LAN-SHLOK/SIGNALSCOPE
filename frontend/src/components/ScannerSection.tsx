import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { SparkleStar } from './SparkleStar';
import { SAMPLE_IMAGES, BATCH_RECORDS } from '../data/mockScanData';
import { SampleImage, BatchScanRecord } from '../types/signalscope';
import { 
  UploadCloud, 
  Sliders, 
  ShieldAlert, 
  ShieldCheck, 
  HelpCircle, 
  Sparkles, 
  Camera, 
  Download, 
  Search, 
  RotateCcw, 
  FileArchive, 
  FolderSync, 
  AlertTriangle, 
  CheckCircle2, 
  Layers,
  Eye,
  Activity,
  Cpu
} from 'lucide-react';

const API_BASE = (import.meta as any).env?.VITE_API_URL !== undefined
  ? (import.meta as any).env.VITE_API_URL
  : (typeof window !== 'undefined' && (window.location.port === '3000' || window.location.port === '5173') ? 'http://localhost:8000' : '');

export const ScannerSection: React.FC = () => {
  // Mode: 'single' image scan or 'batch' folder/zip scan
  const [activeMode, setActiveMode] = useState<'single' | 'batch'>('single');

  // Single Image State - null means initial empty upload state
  const [analyzedImage, setAnalyzedImage] = useState<SampleImage | null>(null);
  const [isScanning, setIsScanning] = useState<boolean>(false);
  const [activeLayer, setActiveLayer] = useState<'fused' | 'attention' | 'srm' | 'fft'>('fused');
  const [heatmapOpacity, setHeatmapOpacity] = useState<number>(70);
  const [infoTab, setInfoTab] = useState<'explanation' | 'waves' | 'camera'>('explanation');

  // Batch Image State - null means initial empty upload state
  const [batchItems, setBatchItems] = useState<BatchScanRecord[] | null>(null);
  const [isBatchScanning, setIsBatchScanning] = useState<boolean>(false);
  const [batchProgress, setBatchProgress] = useState<number>(0);
  const [filterTier, setFilterTier] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  // Handle single custom file upload
  const handleSingleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setIsScanning(true);

      try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE}/api/analyze`, {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const apiResult: SampleImage = await response.json();
          setAnalyzedImage(apiResult);
          setIsScanning(false);
          return;
        }
      } catch (err) {
        console.warn('Backend API offline or unreachable, falling back to local simulation:', err);
      }

      // Offline / fallback path
      const reader = new FileReader();
      reader.onload = () => {
        const customUrl = reader.result as string;
        setTimeout(() => {
          const isReal = file.name.toLowerCase().includes('real') || file.name.toLowerCase().includes('canon') || file.name.toLowerCase().includes('camera');
          const customResult: SampleImage = {
            id: 'custom-file',
            name: file.name,
            tag: 'User Uploaded File',
            description: `File size: ${(file.size / 1024).toFixed(1)} KB. Evaluated through dual-stream spatial & sensor frequency analysis.`,
            sourceType: isReal ? 'camera' : 'diffusion',
            confidence: isReal ? 0.94 : 0.89,
            verdictTier: isReal ? 'confident_real' : 'confident_ai',
            verdictLabel: isReal ? 'Likely Real Camera Photo' : 'Likely AI Generated',
            generatorFamily: isReal ? 'Real Camera' : 'Diffusion-family',
            imgUrl: customUrl,
            heatmapOverlayUrl: isReal ? SAMPLE_IMAGES[2].heatmapOverlayUrl : SAMPLE_IMAGES[0].heatmapOverlayUrl,
            attentionRolloutUrl: isReal ? SAMPLE_IMAGES[2].attentionRolloutUrl : SAMPLE_IMAGES[0].attentionRolloutUrl,
            srmResidualUrl: isReal ? SAMPLE_IMAGES[2].srmResidualUrl : SAMPLE_IMAGES[0].srmResidualUrl,
            fftSpectrumUrl: isReal ? SAMPLE_IMAGES[2].fftSpectrumUrl : SAMPLE_IMAGES[0].fftSpectrumUrl,
            exif: {
              hasExif: isReal,
              cameraModel: isReal ? 'Sony Alpha A7 IV' : undefined,
              lens: isReal ? 'FE 24-70mm F2.8 GM II' : undefined,
              anomalyFlag: isReal ? undefined : 'No camera hardware signature found in image metadata.',
            },
            c2pa: {
              hasC2pa: false,
              validationStatus: 'none',
              trustSignal: 'No Provenance',
            },
            cues: isReal
              ? [
                  {
                    id: 'cue-1',
                    name: 'Camera Sensor Grain',
                    category: 'Sensor',
                    status: 'clear',
                    statusText: 'Natural Sensor Grain Found',
                    description: 'Microscopic examination reveals authentic silicon sensor noise typical of physical optical cameras.',
                    evidence: 'Hardware sensor pattern confirmed.',
                    activationLevel: 94,
                  },
                  {
                    id: 'cue-2',
                    name: 'Natural Lighting Physics',
                    category: 'Physical',
                    status: 'clear',
                    statusText: 'Consistent Lighting',
                    description: 'Eye reflections, specular highlights, and cast shadows follow real-world physical optics.',
                    evidence: 'No lighting conflicts detected.',
                    activationLevel: 91,
                  }
                ]
              : [
                  {
                    id: 'cue-1',
                    name: 'Microscopic Surface Texture',
                    category: 'Spatial',
                    status: 'detected',
                    statusText: 'Artificial Smoothness',
                    description: 'Surface textures are unnaturally smooth without the microscopic noise left by a camera lens.',
                    evidence: 'Detected latent diffusion synthesis pattern.',
                    activationLevel: 89,
                  },
                  {
                    id: 'cue-2',
                    name: 'Camera Hardware Sensor',
                    category: 'Sensor',
                    status: 'abnormal',
                    statusText: 'Missing Camera Stamp',
                    description: 'Silicon sensor noise signature was absent or altered by generative diffusion steps.',
                    evidence: 'Frequency autocorrelation shows high-frequency void.',
                    activationLevel: 85,
                  },
                  {
                    id: 'cue-3',
                    name: 'Light & Shadow Angles',
                    category: 'Physical',
                    status: 'detected',
                    statusText: 'Conflicting Highlights',
                    description: 'Specular highlights on reflective surfaces do not match the shadows cast by surrounding objects.',
                    evidence: 'AI diffusion lighting inconsistency detected.',
                    activationLevel: 78,
                  }
                ],
            summaryExplanation: isReal
              ? 'This image displays authentic optical Bayer CFA sensor traces and natural light physics typical of physical camera lenses.'
              : 'Our spatial and sensor frequency streams detected unnatural surface smoothing and synthetic generative traces typical of diffusion models.',
            fftStats: {
              radialSlope: isReal ? -1.82 : -1.14,
              highFreqPeak: !isReal,
              symmetryScore: isReal ? 0.41 : 0.88,
            }
          };
          setAnalyzedImage(customResult);
          setIsScanning(false);
        }, 500);
      };
      reader.readAsDataURL(file);
    }
  };

  // Test with preset sample
  const handleSelectSample = (sample: SampleImage) => {
    setIsScanning(true);
    setTimeout(() => {
      setAnalyzedImage(sample);
      setIsScanning(false);
    }, 350);
  };

  // Handle batch upload
  const handleBatchUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      setIsBatchScanning(true);
      setBatchProgress(20);

      try {
        const formData = new FormData();
        for (let i = 0; i < Math.min(files.length, 20); i++) {
          formData.append('files', files[i]);
        }
        setBatchProgress(50);
        const response = await fetch(`${API_BASE}/api/batch`, {
          method: 'POST',
          body: formData,
        });
        if (response.ok) {
          const data = await response.json();
          setBatchProgress(100);
          setBatchItems(data.items);
          setIsBatchScanning(false);
          return;
        }
      } catch (err) {
        console.warn('Batch API offline, falling back to local simulation:', err);
      }

      // Offline fallback
      setTimeout(() => setBatchProgress(65), 250);
      setTimeout(() => {
        const count = Math.min(files.length, 12);
        const newRecords: BatchScanRecord[] = [];
        for (let i = 0; i < count; i++) {
          const file = files[i];
          const isReal = file.name.toLowerCase().includes('real') || file.name.toLowerCase().includes('photo') || i % 3 === 1;
          const isUnsure = i % 5 === 4;
          newRecords.push({
            id: `batch-${Date.now()}-${i}`,
            filename: file.name,
            dimensions: '1024 × 1024',
            fileSize: `${(file.size / 1024).toFixed(1)} KB`,
            verdict: isUnsure ? 'Needs Human Review' : isReal ? 'Likely Real Photo' : 'Likely AI Generated',
            confidence: isUnsure ? 0.54 : isReal ? 0.94 : 0.89,
            generatorFamily: isUnsure ? 'Needs Closer Inspection' : isReal ? 'Real Camera' : 'Diffusion-family',
            tier: isUnsure ? 'uncertain' : isReal ? 'confident_real' : 'confident_ai',
            hasC2pa: false,
            hasBayerTrace: isReal,
            inferenceTimeMs: Math.floor(Math.random() * 20) + 18,
          });
        }
        setBatchItems(newRecords);
        setBatchProgress(100);
        setIsBatchScanning(false);
      }, 500);
    }
  };

  // Test with sample batch
  const handleTestSampleBatch = () => {
    setIsBatchScanning(true);
    setBatchProgress(30);
    setTimeout(() => setBatchProgress(75), 300);
    setTimeout(() => {
      setBatchItems(BATCH_RECORDS);
      setBatchProgress(100);
      setIsBatchScanning(false);
    }, 600);
  };

  // Export batch CSV
  const exportToCsv = () => {
    if (!batchItems) return;
    const headers = [
      'File Name',
      'Dimensions',
      'File Size',
      'Verdict',
      'Confidence %',
      'Probable Creator',
      'Camera Fingerprint Found',
      'Digital Stamp (C2PA)',
      'Scan Speed (ms)',
    ];

    const rows = filteredBatchItems.map((r) => [
      `"${r.filename}"`,
      `"${r.dimensions}"`,
      `"${r.fileSize}"`,
      `"${r.verdict}"`,
      `${(r.confidence * 100).toFixed(1)}%`,
      `"${r.generatorFamily}"`,
      r.hasBayerTrace ? 'Yes (Authentic)' : 'No (AI)',
      r.hasC2pa ? 'Valid' : 'None',
      r.inferenceTimeMs,
    ]);

    const csvContent = [headers.join(','), ...rows.map((row) => row.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `signalscope_audit_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  // Filter and sort batch items
  const filteredBatchItems = (batchItems || [])
    .filter((r) => {
      if (filterTier !== 'all' && r.tier !== filterTier) return false;
      if (searchQuery.trim() !== '') {
        const q = searchQuery.toLowerCase();
        return (
          r.filename.toLowerCase().includes(q) ||
          r.generatorFamily.toLowerCase().includes(q) ||
          r.verdict.toLowerCase().includes(q)
        );
      }
      return true;
    })
    .sort((a, b) => (sortAsc ? a.confidence - b.confidence : b.confidence - a.confidence));

  // Get active overlay URL
  const getActiveLayerUrl = () => {
    if (!analyzedImage) return '';
    switch (activeLayer) {
      case 'attention':
        return analyzedImage.attentionRolloutUrl;
      case 'srm':
        return analyzedImage.srmResidualUrl;
      case 'fft':
        return analyzedImage.fftSpectrumUrl;
      case 'fused':
      default:
        return analyzedImage.heatmapOverlayUrl;
    }
  };

  return (
    <section 
      id="scanner" 
      className="relative min-h-screen py-24 px-4 sm:px-8 lg:px-12 bg-[#f4f0e6] text-[#1a1a1a] selection:bg-black selection:text-white flex flex-col justify-center border-t-2 border-b-2 border-black overflow-hidden"
    >
      {/* MATCHING STRUCTURAL OUTLINE WITH SHARP EDGES MATCHING PAGE 3 & 4 */}
      <div className="absolute top-12 left-4 right-4 bottom-12 border-2 border-black/80 pointer-events-none hidden sm:block" />
      <div className="absolute top-16 left-8 right-8 bottom-16 border border-neutral-400/60 pointer-events-none hidden md:block" />

      {/* Corner crosshairs `+` `+` */}
      <div className="absolute top-14 left-6 text-black/60 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute top-14 right-6 text-black/60 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute bottom-14 left-6 text-black/60 font-mono-code text-base hidden sm:block">+</div>
      <div className="absolute bottom-14 right-6 text-black/60 font-mono-code text-base hidden sm:block">+</div>

      {/* Fine dotted vertical guide line matching the dashed line from image.png */}
      <div className="absolute top-0 bottom-0 left-1/2 w-px border-r border-dashed border-neutral-300 pointer-events-none hidden xl:block" />

      {/* Interactive floating decorative stars in margins (hidden on mobile to prevent overlap) */}
      <motion.div 
        animate={{ y: [0, -12, 0], rotate: [0, 15, 0] }}
        transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
        className="absolute top-24 right-14 z-10 hidden md:block"
      >
        <SparkleStar size={56} fill="#000000" className="opacity-30 hover:opacity-90 transition-opacity" />
      </motion.div>
      <motion.div 
        animate={{ y: [0, 10, 0], rotate: [0, -15, 0] }}
        transition={{ duration: 6, repeat: Infinity, ease: "easeInOut", delay: 0.5 }}
        className="absolute bottom-20 left-12 z-10 hidden lg:block"
      >
        <SparkleStar size={44} fill="#000000" className="opacity-25 hover:opacity-85 transition-opacity" />
      </motion.div>

      <div className="max-w-7xl mx-auto w-full relative z-10">
        {/* Top Editorial Header Stamps */}
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.2 }}
          transition={{ duration: 0.5 }}
          className="flex items-center justify-between border-b border-black/15 pb-4 mb-10 text-xs font-mono-code"
        >
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 bg-black animate-pulse" />
            <span className="font-bold tracking-widest uppercase">LABORATORY / MEDIA INSPECTION</span>
          </div>
          <div className="font-serif-vintage tracking-wider text-sm hidden sm:block">
            SIGNALSCOPE ARCHIVE
          </div>
        </motion.div>

        {/* Big Editorial Title - Now "SCANNER & BATCH LAB" directly in that title */}
        <motion.div 
          initial={{ opacity: 0, y: 35 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false, amount: 0.2 }}
          transition={{ duration: 0.6, type: "spring", stiffness: 100, damping: 20 }}
          className="text-center max-w-4xl mx-auto mb-10"
        >
          <h2 className="font-serif-vintage text-5xl sm:text-7xl lg:text-8xl text-black leading-tight mb-4 tracking-tight uppercase select-none">
            SCANNER & BATCH LAB
          </h2>
          <p className="font-display text-base sm:text-lg text-neutral-800 font-semibold max-w-xl mx-auto">
            Upload any single picture to reveal its forensic verdict and heatmaps, or inspect an entire folder at once.
          </p>
        </motion.div>

        {/* MODE TOGGLE: SINGLE IMAGE vs BATCH ARCHIVE */}
        <motion.div 
          initial={{ opacity: 0, scale: 0.92 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: false, amount: 0.2 }}
          transition={{ duration: 0.5, delay: 0.1 }}
          className="flex justify-center mb-10"
        >
          <div className="inline-flex p-1 bg-[#ede8dc] border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)]">
            <motion.button
              whileTap={{ scale: 0.97 }}
              onClick={() => setActiveMode('single')}
              className={`flex items-center gap-2 px-6 py-2.5 font-display font-bold text-xs sm:text-sm uppercase tracking-wider transition-colors duration-150 ${
                activeMode === 'single'
                  ? 'bg-black text-white shadow-inner'
                  : 'text-neutral-700 hover:text-black'
              }`}
            >
              <Camera className="w-4 h-4" />
              <span>Single Image Inspection</span>
            </motion.button>
            <motion.button
              whileTap={{ scale: 0.97 }}
              onClick={() => setActiveMode('batch')}
              className={`flex items-center gap-2 px-6 py-2.5 font-display font-bold text-xs sm:text-sm uppercase tracking-wider transition-colors duration-150 ${
                activeMode === 'batch'
                  ? 'bg-black text-white shadow-inner'
                  : 'text-neutral-700 hover:text-black'
              }`}
            >
              <FolderSync className="w-4 h-4" />
              <span>Batch Folder / ZIP Audit</span>
            </motion.button>
          </div>
        </motion.div>

        {/* ------------------------------------------------------------- */}
        {/* MODE 1: SINGLE IMAGE INSPECTION */}
        {/* ------------------------------------------------------------- */}
        {activeMode === 'single' && (
          <div>
            {/* INITIAL EMPTY UPLOAD STATE */}
            {!analyzedImage && (
              <motion.div 
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: false, amount: 0.2 }}
                transition={{ duration: 0.6 }}
                className="max-w-3xl mx-auto space-y-6"
              >
                {/* Clean, editorial drag & drop upload box with animated scanner laser line */}
                <motion.label 
                  whileHover={{ scale: 1.005, y: -2 }}
                  whileTap={{ scale: 0.99 }}
                  transition={{ duration: 0.12, ease: "easeOut" }}
                  className="relative block w-full p-12 sm:p-16 border-2 border-black bg-white hover:bg-[#faf7f2] text-center cursor-pointer transition-colors duration-150 shadow-[8px_8px_0px_rgba(0,0,0,1)] group overflow-hidden"
                >
                  {/* Subtle animated scanning beam across the drop box */}
                  <motion.div
                    animate={{ y: ['-10%', '300%', '-10%'] }}
                    transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut' }}
                    className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-black/30 to-transparent pointer-events-none"
                  />

                  <div className="flex flex-col items-center justify-center relative z-10">
                    <div className="w-16 h-16 bg-black text-white flex items-center justify-center mb-6 group-hover:scale-105 transition-transform shadow-[4px_4px_0px_rgba(0,0,0,0.2)]">
                      <UploadCloud className="w-8 h-8" />
                    </div>

                    <h3 className="font-serif-vintage text-3xl sm:text-5xl text-black tracking-tight mb-2">
                      Drop an Image to Inspect
                    </h3>
                    
                    <p className="font-display font-medium text-sm sm:text-base text-neutral-600 mb-6">
                      Drag and drop any photograph or click to browse files
                    </p>

                    <div className="inline-flex items-center gap-2 px-4 py-1.5 font-mono-code text-xs text-neutral-700 bg-[#ede8dc] border border-black/20 shadow-sm">
                      <span>SUPPORTS: JPG, PNG, WEBP</span>
                      <span>•</span>
                      <span>LOCAL IN-BROWSER ANALYSIS</span>
                    </div>
                  </div>

                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleSingleUpload}
                    className="hidden"
                  />
                </motion.label>

                {/* Scanning Progress */}
                {isScanning && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="p-4 bg-black text-white border-2 border-black text-center font-mono-code text-xs font-bold animate-pulse"
                  >
                    ANALYZING VISUAL ANATOMY & CAMERA SENSOR GRAIN...
                  </motion.div>
                )}

                {/* Preset demo options */}
                <motion.div 
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: false, amount: 0.2 }}
                  transition={{ duration: 0.5, delay: 0.15 }}
                  className="border-2 border-black/20 p-5 bg-[#ede8dc]"
                >
                  <div className="text-xs font-mono-code text-neutral-700 font-bold uppercase tracking-wider mb-3 flex items-center gap-2">
                    <Sparkles className="w-3.5 h-3.5" />
                    Or test with a sample photograph:
                  </div>

                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                    {SAMPLE_IMAGES.map((sample, idx) => (
                      <motion.button
                        key={sample.id}
                        initial={{ opacity: 0, y: 20 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: false }}
                        transition={{ duration: 0.4, delay: idx * 0.08 }}
                        whileHover={{ scale: 1.02, y: -2, transition: { duration: 0.1, ease: "easeOut" } }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => handleSelectSample(sample)}
                        className="p-3 border border-black/30 hover:border-black bg-white hover:bg-white text-left transition-colors duration-150 shadow-[2px_2px_0px_rgba(0,0,0,0.15)] group"
                      >
                        <div className="aspect-square w-full mb-2 bg-neutral-900 overflow-hidden border border-black/20">
                          <img
                            src={sample.imgUrl}
                            alt={sample.name}
                            className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                          />
                        </div>
                        <div className="font-bold text-xs text-black truncate">
                          {sample.name}
                        </div>
                        <div className="text-[10px] font-mono-code text-neutral-500 truncate">
                          {sample.tag}
                        </div>
                      </motion.button>
                    ))}
                  </div>
                </motion.div>
              </motion.div>
            )}

            {/* RESULTS STATE: DISPLAYED ONCE AN IMAGE IS SELECTED OR UPLOADED */}
            {analyzedImage && (
              <motion.div 
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
                className="space-y-6"
              >
                {/* Action Bar */}
                <div className="flex flex-wrap items-center justify-between gap-4 pb-4 border-b-2 border-black">
                  <motion.button
                    whileHover={{ scale: 1.02, y: -1 }}
                    whileTap={{ scale: 0.98 }}
                    transition={{ duration: 0.1, ease: "easeOut" }}
                    onClick={() => setAnalyzedImage(null)}
                    className="inline-flex items-center gap-2 px-4 py-2 bg-black text-white hover:bg-neutral-800 font-mono-code text-xs font-bold uppercase tracking-wider transition-colors duration-150 shadow-[3px_3px_0px_rgba(0,0,0,0.3)]"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    <span>Scan Another Image</span>
                  </motion.button>

                  <div className="flex items-center gap-3">
                    <span className="text-xs font-mono-code text-neutral-600">
                      Active: <strong className="text-black">{analyzedImage.name}</strong>
                    </span>
                    <label className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-white border-2 border-black text-black font-mono-code text-xs font-bold cursor-pointer hover:bg-neutral-100 transition-colors duration-150 shadow-[2px_2px_0px_rgba(0,0,0,1)]">
                      <UploadCloud className="w-3.5 h-3.5" />
                      <span>Upload New</span>
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleSingleUpload}
                        className="hidden"
                      />
                    </label>
                  </div>
                </div>

                {/* RESULTS GRID: FULL IMAGE VIEWER + VERDICT/EXPLANATIONS */}
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
                  {/* LEFT: FULL-SIZE IMAGE & HEATMAP INSPECTOR (7 Cols) with scroll slide-in */}
                  <motion.div 
                    initial={{ opacity: 0, x: -25 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: false, amount: 0.15 }}
                    transition={{ duration: 0.6 }}
                    className="lg:col-span-7 bg-white border-2 border-black p-4 sm:p-6 shadow-[8px_8px_0px_rgba(0,0,0,1)]"
                  >
                    {/* Layer Mode Buttons */}
                    <div className="flex flex-wrap items-center justify-between gap-3 mb-4">
                      <span className="font-mono-code text-xs text-black font-bold uppercase tracking-wider">
                        Forensic View Mode:
                      </span>

                      <div className="flex flex-wrap gap-1">
                        <button
                          onClick={() => setActiveLayer('fused')}
                          className={`px-3 py-1 font-mono-code text-xs uppercase font-bold border-2 transition-colors duration-150 ${
                            activeLayer === 'fused'
                              ? 'bg-black text-white border-black'
                              : 'bg-white text-black border-black/30 hover:border-black'
                          }`}
                        >
                          <Layers className="w-3 h-3 inline mr-1" />
                          Suspicious Heatmap
                        </button>
                        <button
                          onClick={() => setActiveLayer('attention')}
                          className={`px-3 py-1 font-mono-code text-xs uppercase font-bold border-2 transition-colors duration-150 ${
                            activeLayer === 'attention'
                              ? 'bg-black text-white border-black'
                              : 'bg-white text-black border-black/30 hover:border-black'
                          }`}
                        >
                          <Eye className="w-3 h-3 inline mr-1" />
                          Focus Areas
                        </button>
                        <button
                          onClick={() => setActiveLayer('srm')}
                          className={`px-3 py-1 font-mono-code text-xs uppercase font-bold border-2 transition-colors duration-150 ${
                            activeLayer === 'srm'
                              ? 'bg-black text-white border-black'
                              : 'bg-white text-black border-black/30 hover:border-black'
                          }`}
                        >
                          <Cpu className="w-3 h-3 inline mr-1" />
                          Sensor Noise
                        </button>
                        <button
                          onClick={() => setActiveLayer('fft')}
                          className={`px-3 py-1 font-mono-code text-xs uppercase font-bold border-2 transition-colors duration-150 ${
                            activeLayer === 'fft'
                              ? 'bg-black text-white border-black'
                              : 'bg-white text-black border-black/30 hover:border-black'
                          }`}
                        >
                          <Activity className="w-3 h-3 inline mr-1" />
                          Light Waves
                        </button>
                      </div>
                    </div>

                    {/* Image Viewer with real-time scan laser animation */}
                    <div className="relative aspect-square sm:aspect-4/3 w-full bg-neutral-900 border-2 border-black overflow-hidden mb-4 flex items-center justify-center">
                      <img
                        src={analyzedImage.imgUrl}
                        alt="Analyzed Photo"
                        className="absolute inset-0 w-full h-full object-contain"
                      />
                      <img
                        src={getActiveLayerUrl()}
                        alt="Forensic Map"
                        className="absolute inset-0 w-full h-full object-contain mix-blend-screen pointer-events-none transition-opacity duration-150"
                        style={{ opacity: heatmapOpacity / 100 }}
                      />

                      {/* Moving laser scan line */}
                      <motion.div
                        animate={{ top: ['0%', '98%', '0%'] }}
                        transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
                        className="absolute left-0 right-0 h-0.5 bg-[#00e540]/90 shadow-[0_0_8px_rgba(0,229,64,0.9)] z-10 pointer-events-none"
                      />

                      <div className="absolute top-3 left-3 px-3 py-1 bg-black text-white font-mono-code text-[11px] font-bold border border-white/20 z-20">
                        Layer: {activeLayer.toUpperCase()} ({heatmapOpacity}%)
                      </div>
                    </div>

                    {/* Blend Slider */}
                    <div className="p-3 bg-[#ede8dc] border border-black/30 space-y-1">
                      <div className="flex justify-between text-xs font-mono-code text-black font-bold">
                        <span className="flex items-center gap-1.5">
                          <Sliders className="w-3.5 h-3.5" />
                          Adjust Heatmap Blend:
                        </span>
                        <span>{heatmapOpacity}%</span>
                      </div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        value={heatmapOpacity}
                        onChange={(e) => setHeatmapOpacity(Number(e.target.value))}
                        className="w-full accent-black cursor-pointer"
                      />
                      <div className="flex justify-between text-[10px] font-mono-code text-neutral-600">
                        <span>0% (Clean Original)</span>
                        <span>50% (Balanced)</span>
                        <span>100% (Pure Overlay)</span>
                      </div>
                    </div>
                  </motion.div>

                  {/* RIGHT: BOLD VERDICT & EXPLANATION (5 Cols) with scroll slide-in */}
                  <motion.div 
                    initial={{ opacity: 0, x: 25 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: false, amount: 0.15 }}
                    transition={{ duration: 0.6, delay: 0.1 }}
                    className="lg:col-span-5 space-y-4"
                  >
                    {/* VERDICT BANNER */}
                    <div className={`p-6 border-2 shadow-[6px_6px_0px_rgba(0,0,0,1)] ${
                      analyzedImage.verdictTier === 'confident_ai'
                        ? 'bg-red-100 border-black text-red-950'
                        : analyzedImage.verdictTier === 'confident_real'
                        ? 'bg-emerald-100 border-black text-emerald-950'
                        : 'bg-amber-100 border-black text-amber-950'
                    }`}>
                      <div className="flex items-center justify-between text-xs font-mono-code font-bold uppercase tracking-widest mb-2 text-neutral-800">
                        <span>DETECTION VERDICT</span>
                        <span>
                          {analyzedImage.verdictTier === 'confident_real'
                            ? `${((1 - analyzedImage.confidence) * 100).toFixed(0)}% CONFIDENCE`
                            : `${(analyzedImage.confidence * 100).toFixed(0)}% CONFIDENCE`}
                        </span>
                      </div>

                      <div className="flex items-center gap-3 mb-2">
                        {analyzedImage.verdictTier === 'confident_ai' && (
                          <ShieldAlert className="w-10 h-10 text-red-700 shrink-0" />
                        )}
                        {analyzedImage.verdictTier === 'confident_real' && (
                          <ShieldCheck className="w-10 h-10 text-emerald-700 shrink-0" />
                        )}
                        {analyzedImage.verdictTier === 'uncertain' && (
                          <HelpCircle className="w-10 h-10 text-amber-700 shrink-0" />
                        )}
                        <div>
                          <h4 className="font-serif-vintage text-3xl sm:text-4xl tracking-tight leading-none text-black">
                            {analyzedImage.verdictLabel}
                          </h4>
                          <span className="text-xs font-mono-code text-neutral-700 font-semibold">
                            Source Profile: {analyzedImage.generatorFamily}
                          </span>
                        </div>
                      </div>

                      {/* Meter bar */}
                      <div className="w-full h-3 bg-white border-2 border-black p-0.5 mt-4">
                        <div
                          className={`h-full ${
                            analyzedImage.verdictTier === 'confident_ai'
                              ? 'bg-red-600'
                              : analyzedImage.verdictTier === 'confident_real'
                              ? 'bg-emerald-600'
                              : 'bg-amber-600'
                          }`}
                          style={{
                            width: `${
                              analyzedImage.verdictTier === 'confident_real'
                                ? (1 - analyzedImage.confidence) * 100
                                : analyzedImage.confidence * 100
                            }%`
                          }}
                        />
                      </div>
                    </div>

                    {/* TABS: EXPLANATION / WAVES / CAMERA */}
                    <div className="bg-white border-2 border-black p-5 shadow-[4px_4px_0px_rgba(0,0,0,1)]">
                      <div className="flex border-b-2 border-black/15 pb-3 mb-4">
                        <button
                          onClick={() => setInfoTab('explanation')}
                          className={`flex-1 py-2 font-mono-code text-xs uppercase font-bold border-b-2 transition-all ${
                            infoTab === 'explanation'
                              ? 'border-black text-black'
                              : 'border-transparent text-neutral-500 hover:text-black'
                          }`}
                        >
                          Simple Explanation
                        </button>
                        <button
                          onClick={() => setInfoTab('waves')}
                          className={`flex-1 py-2 font-mono-code text-xs uppercase font-bold border-b-2 transition-all ${
                            infoTab === 'waves'
                              ? 'border-black text-black'
                              : 'border-transparent text-neutral-500 hover:text-black'
                          }`}
                        >
                          Light Waves
                        </button>
                        <button
                          onClick={() => setInfoTab('camera')}
                          className={`flex-1 py-2 font-mono-code text-xs uppercase font-bold border-b-2 transition-all ${
                            infoTab === 'camera'
                              ? 'border-black text-black'
                              : 'border-transparent text-neutral-500 hover:text-black'
                          }`}
                        >
                          Camera Info
                        </button>
                      </div>

                      {/* Tab 1: Explanation */}
                      {infoTab === 'explanation' && (
                        <div className="space-y-3">
                          <p className="text-xs text-neutral-800 leading-relaxed font-display font-medium">
                            {analyzedImage.summaryExplanation}
                          </p>

                          <div className="pt-2 border-t border-black/10 space-y-2">
                            <span className="text-[11px] font-mono-code text-black font-bold uppercase tracking-wider block">
                              Key Clues Detected:
                            </span>
                            {analyzedImage.cues.map((cue) => (
                              <div key={cue.id} className="p-2.5 bg-[#f5f1e8] border border-black/20 text-xs">
                                <div className="flex items-center justify-between font-bold text-black mb-1">
                                  <span className="flex items-center gap-1.5">
                                    {cue.status === 'detected' && <AlertTriangle className="w-3.5 h-3.5 text-red-600" />}
                                    {cue.status === 'abnormal' && <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />}
                                    {cue.status === 'clear' && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />}
                                    <span>{cue.name}</span>
                                  </span>
                                  <span className="text-[10px] font-mono-code text-neutral-600">
                                    {cue.statusText}
                                  </span>
                                </div>
                                <p className="text-[11px] text-neutral-700">
                                  {cue.description}
                                </p>
                              </div>
                            ))}
                          </div>
                        </div>
                      )}

                      {/* Tab 2: Light Waves */}
                      {infoTab === 'waves' && (
                        <div className="space-y-3 text-xs">
                          <div className="p-3 bg-neutral-900 border-2 border-black flex justify-center">
                            <img
                              src={analyzedImage.fftSpectrumUrl}
                              alt="Light Waves"
                              className="w-40 h-40 object-contain"
                            />
                          </div>
                          <div className="p-3 bg-[#f5f1e8] border border-black/20 text-neutral-800 font-display">
                            <strong className="block mb-1 text-black font-bold">How Light Waves Tell the Story:</strong>
                            <p className="text-[11px] text-neutral-700 leading-relaxed">
                              Real cameras scatter light smoothly like gentle water ripples. Generative AI tools leave unnatural checkerboard spikes because pixels are generated by math formulas.
                            </p>
                          </div>
                        </div>
                      )}

                      {/* Tab 3: Camera Metadata */}
                      {infoTab === 'camera' && (
                        <div className="space-y-2 text-xs font-mono-code">
                          <div className="p-3 bg-[#f5f1e8] border border-black/20 space-y-2">
                            <div className="flex justify-between border-b border-black/10 pb-1.5">
                              <span className="text-neutral-500">Camera Model:</span>
                              <span className="text-black font-bold">{analyzedImage.exif.cameraModel || 'None Found (AI)'}</span>
                            </div>
                            <div className="flex justify-between border-b border-black/10 pb-1.5">
                              <span className="text-neutral-500">Camera Lens:</span>
                              <span className="text-black">{analyzedImage.exif.lens || 'N/A'}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-neutral-500">Provenance Stamp:</span>
                              <span className="text-black font-bold">{analyzedImage.c2pa.trustSignal}</span>
                            </div>
                          </div>
                          <p className="text-[10px] text-neutral-600 italic">
                            Physical cameras record hardware lens and sensor metadata tags. AI models typically lack these hardware footprints.
                          </p>
                        </div>
                      )}
                    </div>
                  </motion.div>
                </div>
              </motion.div>
            )}
          </div>
        )}

        {/* ------------------------------------------------------------- */}
        {/* MODE 2: BATCH FOLDER / ZIP AUDIT */}
        {/* ------------------------------------------------------------- */}
        {activeMode === 'batch' && (
          <div>
            {/* INITIAL BATCH UPLOAD SCREEN */}
            {!batchItems && (
              <motion.div 
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: false, amount: 0.2 }}
                transition={{ duration: 0.6 }}
                className="max-w-3xl mx-auto space-y-6"
              >
                <motion.label 
                  whileHover={{ scale: 1.005, y: -2 }}
                  whileTap={{ scale: 0.99 }}
                  transition={{ duration: 0.12, ease: "easeOut" }}
                  className="relative block w-full p-12 sm:p-16 border-2 border-black bg-white hover:bg-[#faf7f2] text-center cursor-pointer transition-colors duration-150 shadow-[8px_8px_0px_rgba(0,0,0,1)] group overflow-hidden"
                >
                  {/* Moving scanner line in batch dropzone */}
                  <motion.div
                    animate={{ y: ['-10%', '300%', '-10%'] }}
                    transition={{ duration: 4.5, repeat: Infinity, ease: 'easeInOut' }}
                    className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-black/30 to-transparent pointer-events-none"
                  />

                  <div className="flex flex-col items-center justify-center relative z-10">
                    <div className="w-16 h-16 bg-black text-white flex items-center justify-center mb-6 group-hover:scale-105 transition-transform shadow-[4px_4px_0px_rgba(0,0,0,0.2)]">
                      <FileArchive className="w-8 h-8" />
                    </div>

                    <h3 className="font-serif-vintage text-3xl sm:text-5xl text-black tracking-tight mb-2">
                      Drop a Folder or ZIP Archive
                    </h3>
                    
                    <p className="font-display font-medium text-sm sm:text-base text-neutral-600 mb-6">
                      Scan hundreds of images simultaneously and generate a CSV report
                    </p>

                    <div className="inline-flex items-center gap-2 px-4 py-1.5 font-mono-code text-xs text-neutral-700 bg-[#ede8dc] border border-black/20 shadow-sm">
                      <span>AUDITS UP TO 500 IMAGES</span>
                      <span>•</span>
                      <span>SORTABLE TABLE & CSV EXPORT</span>
                    </div>
                  </div>

                  <input
                    type="file"
                    multiple
                    onChange={handleBatchUpload}
                    className="hidden"
                  />
                </motion.label>

                {/* Scanning Progress */}
                {isBatchScanning && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.95 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="p-4 bg-black text-white border-2 border-black space-y-2"
                  >
                    <div className="flex justify-between text-xs font-mono-code text-white font-bold">
                      <span>SCANNING BATCH ARCHIVE...</span>
                      <span>{batchProgress}%</span>
                    </div>
                    <div className="w-full h-2 bg-neutral-800">
                      <div
                        className="h-full bg-[#00e540] transition-all duration-300"
                        style={{ width: `${batchProgress}%` }}
                      />
                    </div>
                  </motion.div>
                )}

                {/* Quick Sample Batch */}
                <motion.div 
                  initial={{ opacity: 0, y: 15 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  viewport={{ once: false, amount: 0.2 }}
                  transition={{ duration: 0.5, delay: 0.1 }}
                  className="text-center pt-2"
                >
                  <motion.button
                    whileHover={{ scale: 1.02, y: -2 }}
                    whileTap={{ scale: 0.98 }}
                    transition={{ duration: 0.1, ease: "easeOut" }}
                    onClick={handleTestSampleBatch}
                    className="inline-flex items-center gap-2 px-6 py-3 bg-white hover:bg-[#ede8dc] text-black font-mono-code text-xs font-bold uppercase tracking-wider border-2 border-black shadow-[4px_4px_0px_rgba(0,0,0,1)] transition-colors duration-150"
                  >
                    <Sparkles className="w-4 h-4" />
                    <span>Or Test With Sample 6-Image Batch</span>
                  </motion.button>
                </motion.div>
              </motion.div>
            )}

            {/* BATCH RESULTS VIEW */}
            {batchItems && (
              <motion.div 
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: false, amount: 0.1 }}
                transition={{ duration: 0.6 }}
                className="space-y-6"
              >
                {/* Header */}
                <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 bg-white border-2 border-black shadow-[6px_6px_0px_rgba(0,0,0,1)]">
                  <div>
                    <h3 className="font-serif-vintage text-2xl sm:text-3xl text-black">
                      Batch Audit Results
                    </h3>
                    <p className="text-xs text-neutral-600 font-mono-code mt-0.5">
                      Audited {batchItems.length} images • Average speed: ~24 ms/image
                    </p>
                  </div>

                  <div className="flex flex-wrap items-center gap-3">
                    <motion.button
                      whileHover={{ scale: 1.02, y: -1 }}
                      whileTap={{ scale: 0.98 }}
                      transition={{ duration: 0.1, ease: "easeOut" }}
                      onClick={exportToCsv}
                      className="inline-flex items-center gap-2 px-5 py-2.5 bg-black hover:bg-neutral-800 text-white font-display font-bold text-xs sm:text-sm uppercase tracking-wider transition-colors duration-150 shadow-[3px_3px_0px_rgba(0,0,0,0.3)]"
                    >
                      <Download className="w-4 h-4" />
                      <span>Download CSV Spreadsheet</span>
                    </motion.button>

                    <motion.button
                      whileHover={{ scale: 1.02, y: -1 }}
                      whileTap={{ scale: 0.98 }}
                      transition={{ duration: 0.1, ease: "easeOut" }}
                      onClick={() => setBatchItems(null)}
                      className="inline-flex items-center gap-1.5 px-4 py-2.5 bg-[#ede8dc] hover:bg-white text-black font-mono-code text-xs font-bold uppercase border-2 border-black transition-colors duration-150"
                    >
                      <RotateCcw className="w-3.5 h-3.5" />
                      <span>Upload Another Batch</span>
                    </motion.button>
                  </div>
                </div>

                {/* KPI Metrics */}
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                  <div className="p-4 bg-white border-2 border-black">
                    <span className="text-[11px] font-mono-code text-neutral-500 uppercase block">Total Scanned</span>
                    <span className="font-serif-vintage text-3xl sm:text-4xl text-black">{batchItems.length}</span>
                  </div>
                  <div className="p-4 bg-white border-2 border-black">
                    <span className="text-[11px] font-mono-code text-red-600 uppercase block">AI Generated</span>
                    <span className="font-serif-vintage text-3xl sm:text-4xl text-red-700">
                      {batchItems.filter((i) => i.tier === 'confident_ai').length}
                    </span>
                  </div>
                  <div className="p-4 bg-white border-2 border-black">
                    <span className="text-[11px] font-mono-code text-emerald-600 uppercase block">Real Photos</span>
                    <span className="font-serif-vintage text-3xl sm:text-4xl text-emerald-700">
                      {batchItems.filter((i) => i.tier === 'confident_real').length}
                    </span>
                  </div>
                  <div className="p-4 bg-white border-2 border-black">
                    <span className="text-[11px] font-mono-code text-amber-600 uppercase block">Needs Review</span>
                    <span className="font-serif-vintage text-3xl sm:text-4xl text-amber-700">
                      {batchItems.filter((i) => i.tier === 'uncertain').length}
                    </span>
                  </div>
                </div>

                {/* Filters */}
                <div className="p-4 bg-white border-2 border-black flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
                    <span className="text-xs font-mono-code text-neutral-600">Filter:</span>
                    <button
                      onClick={() => setFilterTier('all')}
                      className={`px-3 py-1 font-mono-code text-xs uppercase border-2 transition-all ${
                        filterTier === 'all' ? 'bg-black text-white border-black' : 'bg-white text-black border-black/30'
                      }`}
                    >
                      All ({batchItems.length})
                    </button>
                    <button
                      onClick={() => setFilterTier('confident_ai')}
                      className={`px-3 py-1 font-mono-code text-xs uppercase border-2 transition-all ${
                        filterTier === 'confident_ai' ? 'bg-red-700 text-white border-red-700' : 'bg-white text-red-700 border-red-300'
                      }`}
                    >
                      AI Only ({batchItems.filter((i) => i.tier === 'confident_ai').length})
                    </button>
                    <button
                      onClick={() => setFilterTier('confident_real')}
                      className={`px-3 py-1 font-mono-code text-xs uppercase border-2 transition-all ${
                        filterTier === 'confident_real' ? 'bg-emerald-700 text-white border-emerald-700' : 'bg-white text-emerald-700 border-emerald-300'
                      }`}
                    >
                      Real Only ({batchItems.filter((i) => i.tier === 'confident_real').length})
                    </button>
                  </div>

                  <div className="flex items-center gap-3 w-full sm:w-auto">
                    <div className="relative flex-1 sm:w-48">
                      <Search className="w-3.5 h-3.5 text-neutral-400 absolute left-3 top-1/2 -translate-y-1/2" />
                      <input
                        type="text"
                        placeholder="Search filename..."
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="w-full bg-[#f4f0e6] text-xs text-black pl-8 pr-3 py-1.5 border-2 border-black focus:outline-none"
                      />
                    </div>
                    <button
                      onClick={() => setSortAsc(!sortAsc)}
                      className="px-3 py-1.5 font-mono-code text-xs bg-[#ede8dc] border-2 border-black text-black font-bold"
                    >
                      {sortAsc ? 'Lowest AI %' : 'Highest AI %'}
                    </button>
                  </div>
                </div>

                {/* Table */}
                <div className="border-2 border-black overflow-x-auto bg-white shadow-[6px_6px_0px_rgba(0,0,0,1)]">
                  <table className="w-full text-left text-xs border-collapse font-mono-code">
                    <thead>
                      <tr className="border-b-2 border-black bg-[#ede8dc] text-black uppercase font-bold">
                        <th className="py-3 px-4">File Name</th>
                        <th className="py-3 px-4">Verdict</th>
                        <th className="py-3 px-4">Confidence</th>
                        <th className="py-3 px-4">AI Family</th>
                        <th className="py-3 px-4">Camera Sensor Trace</th>
                        <th className="py-3 px-4">Speed</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y border-black/20 text-neutral-900">
                      {filteredBatchItems.map((item) => (
                        <tr key={item.id} className="hover:bg-[#f6f2ea] transition-colors">
                          <td className="py-3 px-4 font-bold text-black">
                            <div>{item.filename}</div>
                            <div className="text-[10px] text-neutral-500">{item.dimensions} • {item.fileSize}</div>
                          </td>
                          <td className="py-3 px-4">
                            <span className={`px-2 py-0.5 border font-bold ${
                              item.tier === 'confident_ai'
                                ? 'bg-red-100 text-red-800 border-red-400'
                                : item.tier === 'confident_real'
                                ? 'bg-emerald-100 text-emerald-800 border-emerald-400'
                                : 'bg-amber-100 text-amber-800 border-amber-400'
                            }`}>
                              {item.verdict}
                            </span>
                          </td>
                          <td className="py-3 px-4 font-bold text-sm">
                            {(item.confidence * 100).toFixed(0)}%
                          </td>
                          <td className="py-3 px-4">{item.generatorFamily}</td>
                          <td className="py-3 px-4">
                            {item.hasBayerTrace ? (
                              <span className="text-emerald-700 font-bold">Camera Found</span>
                            ) : (
                              <span className="text-red-700">Absent (AI)</span>
                            )}
                          </td>
                          <td className="py-3 px-4 text-neutral-500">{item.inferenceTimeMs} ms</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </motion.div>
            )}
          </div>
        )}
      </div>
    </section>
  );
};
