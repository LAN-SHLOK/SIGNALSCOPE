import { SampleImage, BatchScanRecord } from '../types/signalscope';

// SVG canvas generators for realistic visual samples & forensic maps
const createSvgDataUrl = (svgContent: string): string => {
  return `data:image/svg+xml;utf8,${encodeURIComponent(svgContent.trim())}`;
};

export const SAMPLE_IMAGES: SampleImage[] = [
  {
    id: 'sample-diffusion',
    name: 'Cyberpunk Portrait (Midjourney v6)',
    tag: 'AI Diffusion Generated',
    description: 'High-detail synthetic portrait with latent diffusion upsampling and prompt lighting physics.',
    sourceType: 'diffusion',
    confidence: 0.884,
    verdictTier: 'confident_ai',
    verdictLabel: 'Likely AI-generated',
    generatorFamily: 'Diffusion-family',
    // Original synthetic image illustration
    imgUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="cyberGlow" cx="50%" cy="40%" r="60%">
            <stop offset="0%" stop-color="#0ff" stop-opacity="0.9"/>
            <stop offset="50%" stop-color="#8a2be2" stop-opacity="0.8"/>
            <stop offset="100%" stop-color="#0a051b" stop-opacity="1"/>
          </radialGradient>
          <linearGradient id="skin" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#ffb6c1"/>
            <stop offset="100%" stop-color="#e68a9f"/>
          </linearGradient>
        </defs>
        <rect width="600" height="600" fill="url(#cyberGlow)"/>
        <!-- Face silhouette -->
        <ellipse cx="300" cy="290" rx="140" ry="190" fill="url(#skin)"/>
        <!-- Cybernetic eyes with glassy AI specular shine -->
        <ellipse cx="240" cy="270" rx="30" ry="18" fill="#111"/>
        <ellipse cx="360" cy="270" rx="30" ry="18" fill="#111"/>
        <circle cx="240" cy="270" r="12" fill="#00ffff"/>
        <circle cx="360" cy="270" r="12" fill="#00ffff"/>
        <circle cx="243" cy="267" r="4" fill="#fff"/>
        <circle cx="363" cy="267" r="4" fill="#fff"/>
        <!-- Nose and mouth with ultra-smooth synthetic shading -->
        <path d="M 296 280 Q 300 325 285 335 L 315 335" stroke="#c0607a" stroke-width="4" fill="none"/>
        <path d="M 255 385 Q 300 415 345 385 Q 300 400 255 385 Z" fill="#b03050"/>
        <!-- Cyber hairline / glowing strands -->
        <path d="M 160 250 Q 220 120 300 130 Q 380 120 440 250 Q 400 160 300 165 Q 200 160 160 250 Z" fill="#0ff" opacity="0.85"/>
        <!-- Watermark / grid text -->
        <text x="30" y="560" fill="#00ffff" font-family="monospace" font-size="14" opacity="0.6">SYNTHETIC ARTIFACTS: DINOv2-L14 / LATENT DIFFUSION NOISE DETECTED</text>
      </svg>
    `),
    // Fused Heatmap (Attention Rollout + GradCAM on SRM)
    heatmapOverlayUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="heat1" cx="40%" cy="45%" r="35%">
            <stop offset="0%" stop-color="#ff0000" stop-opacity="0.9"/>
            <stop offset="40%" stop-color="#ff8800" stop-opacity="0.75"/>
            <stop offset="70%" stop-color="#ffee00" stop-opacity="0.5"/>
            <stop offset="100%" stop-color="#0000ff" stop-opacity="0"/>
          </radialGradient>
          <radialGradient id="heat2" cx="60%" cy="45%" r="30%">
            <stop offset="0%" stop-color="#ff0000" stop-opacity="0.85"/>
            <stop offset="50%" stop-color="#ffaa00" stop-opacity="0.6"/>
            <stop offset="100%" stop-color="#0000ff" stop-opacity="0"/>
          </radialGradient>
          <radialGradient id="heatHair" cx="50%" cy="25%" r="45%">
            <stop offset="0%" stop-color="#ff0055" stop-opacity="0.8"/>
            <stop offset="60%" stop-color="#ffcc00" stop-opacity="0.4"/>
            <stop offset="100%" stop-color="#00ffff" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <rect width="600" height="600" fill="url(#heatHair)"/>
        <circle cx="240" cy="270" r="120" fill="url(#heat1)"/>
        <circle cx="360" cy="270" r="110" fill="url(#heat2)"/>
      </svg>
    `),
    // Attention Rollout (DINOv2 ViT 37x37 grid)
    attentionRolloutUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="attnGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#003366"/>
            <stop offset="50%" stop-color="#ff3300"/>
            <stop offset="100%" stop-color="#ffff00"/>
          </linearGradient>
        </defs>
        <rect width="600" height="600" fill="#051020"/>
        <!-- 37x37 patch grid preview -->
        <g opacity="0.3" stroke="#0ff" stroke-width="0.5">
          <line x1="0" y1="150" x2="600" y2="150"/><line x1="0" y1="300" x2="600" y2="300"/><line x1="0" y1="450" x2="600" y2="450"/>
          <line x1="150" y1="0" x2="150" y2="600"/><line x1="300" y1="0" x2="300" y2="600"/><line x1="450" y1="0" x2="450" y2="600"/>
        </g>
        <circle cx="300" cy="270" r="160" fill="url(#attnGrad)" opacity="0.85"/>
        <circle cx="300" cy="270" r="80" fill="#ffffff" opacity="0.9"/>
      </svg>
    `),
    // SRM Multi-Colorspace Residual Map
    srmResidualUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#222"/>
        <!-- Noise filter texture -->
        <filter id="noiseFilter">
          <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/>
          <feColorMatrix type="matrix" values="0 1 0 0 0  1 0 0 0 0  0 0 1 0 0  0 0 0 1 0"/>
        </filter>
        <rect width="600" height="600" filter="url(#noiseFilter)" opacity="0.75"/>
        <!-- Edge outlines where high-pass triggers -->
        <ellipse cx="300" cy="290" rx="140" ry="190" stroke="#00e540" stroke-width="4" fill="none" opacity="0.8"/>
        <ellipse cx="240" cy="270" rx="30" ry="18" stroke="#ff0055" stroke-width="3" fill="none"/>
        <ellipse cx="360" cy="270" rx="30" ry="18" stroke="#ff0055" stroke-width="3" fill="none"/>
      </svg>
    `),
    // FFT Spectrum
    fftSpectrumUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#05080c"/>
        <circle cx="300" cy="300" r="280" fill="none" stroke="#10e346" stroke-width="1" stroke-dasharray="4 8" opacity="0.3"/>
        <circle cx="300" cy="300" r="180" fill="none" stroke="#10e346" stroke-width="1" stroke-dasharray="4 8" opacity="0.4"/>
        <circle cx="300" cy="300" r="90" fill="none" stroke="#10e346" stroke-width="1" opacity="0.6"/>
        <!-- Synthetic frequency cross and periodic peaks -->
        <line x1="0" y1="300" x2="600" y2="300" stroke="#00ffff" stroke-width="2" opacity="0.6"/>
        <line x1="300" y1="0" x2="300" y2="600" stroke="#00ffff" stroke-width="2" opacity="0.6"/>
        <!-- Central DC peak -->
        <circle cx="300" cy="300" r="25" fill="#ffffff"/>
        <!-- Periodic upsampling spikes (characteristic of diffusion/GAN) -->
        <circle cx="420" cy="300" r="6" fill="#ff0055"/>
        <circle cx="180" cy="300" r="6" fill="#ff0055"/>
        <circle cx="300" cy="420" r="6" fill="#ff0055"/>
        <circle cx="300" cy="180" r="6" fill="#ff0055"/>
      </svg>
    `),
    exif: {
      hasExif: false,
      anomalyFlag: 'Missing all EXIF hardware headers (common in direct AI generation)',
    },
    c2pa: {
      hasC2pa: false,
      validationStatus: 'none',
      trustSignal: 'No Provenance',
    },
    cues: [
      {
        id: 'cue-1',
        name: 'Unnatural High-Freq Energy',
        category: 'Spectral',
        status: 'abnormal',
        statusText: 'Spike Detected',
        description: 'Frequency power distribution exhibits unnatural decay rate at object contours, typical of latent deconvolution.',
        evidence: 'Azimuthal spectrum slope = -0.42 (Real camera reference: -1.02 ± 0.08).',
        activationLevel: 92,
      },
      {
        id: 'cue-2',
        name: 'Structured Noise Residual',
        category: 'Spatial',
        status: 'detected',
        statusText: 'Synthetic Pattern',
        description: 'Multi-colorspace SRM residual maps reveal non-Poissonian noise across RGB, YCbCr, and HSV planes.',
        evidence: 'SRM-CNN 256-dim embedding clusters squarely inside Diffusion manifold.',
        activationLevel: 88,
      },
      {
        id: 'cue-3',
        name: 'Bayer CFA Demodulation',
        category: 'Sensor',
        status: 'missing',
        statusText: 'Zero Sensor Trace',
        description: 'Physical camera sensors use Bayer color filter arrays leaving periodic 2-pixel autocorrelation. Completely absent.',
        evidence: 'Autocorrelation ratio = 0.992 (Authentic threshold > 1.050).',
        activationLevel: 95,
      },
      {
        id: 'cue-4',
        name: 'DINOv2 Patch Uniformity',
        category: 'Physical',
        status: 'abnormal',
        statusText: 'Excessive Uniformity',
        description: 'Average pairwise cosine similarity across 1,369 patch tokens is significantly higher than natural photographic diversity.',
        evidence: 'Patch similarity score = 0.814 (Natural scene baseline: 0.45 - 0.62).',
        activationLevel: 84,
      },
      {
        id: 'cue-5',
        name: 'JPEG Ghost Signature',
        category: 'Spectral',
        status: 'detected',
        statusText: 'Uncompressed Latent',
        description: 'Ghost curve shows zero minimum dip across 10 quality steps, proving the image has never experienced camera-native compression.',
        evidence: 'Recompression std deviation is flat across Q=50 to 95.',
        activationLevel: 79,
      },
      {
        id: 'cue-6',
        name: 'Cryptographic Provenance',
        category: 'Metadata',
        status: 'missing',
        statusText: 'No C2PA Manifest',
        description: 'No Content Credentials signature or device root-of-trust found in image metadata container.',
        evidence: 'Zero metadata segments found in JFIF/Exif header blocks.',
        activationLevel: 70,
      },
    ],
    summaryExplanation: 'High-confidence AI generation verdict driven by combined DINOv2 patch uniformity, high-pass SRM residual anomalies in chrominance channels, and complete absence of camera sensor Bayer CFA autocorrelation.',
    fftStats: {
      radialSlope: -0.42,
      highFreqPeak: true,
      symmetryScore: 0.91,
    },
  },

  {
    id: 'sample-gan',
    name: 'Studio Fashion Face (StyleGAN3)',
    tag: 'GAN-Family Synthesis',
    description: 'Generative Adversarial Network output exhibiting symmetric eye reflections and transductive grid artifacts.',
    sourceType: 'gan',
    confidence: 0.941,
    verdictTier: 'confident_ai',
    verdictLabel: 'Likely AI-generated',
    generatorFamily: 'GAN-family',
    imgUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#1c2024"/>
        <ellipse cx="300" cy="300" rx="150" ry="200" fill="#e8c4b8"/>
        <!-- Eyeballs with identical uncanny reflections -->
        <ellipse cx="240" cy="275" rx="25" ry="15" fill="#fff"/>
        <ellipse cx="360" cy="275" rx="25" ry="15" fill="#fff"/>
        <circle cx="240" cy="275" r="11" fill="#3a2416"/>
        <circle cx="360" cy="275" r="11" fill="#3a2416"/>
        <!-- Identical pinpoint catchlights -->
        <circle cx="243" cy="272" r="3" fill="#fff"/>
        <circle cx="363" cy="272" r="3" fill="#fff"/>
        <path d="M 300 290 L 290 350 L 310 350 Z" fill="#d9aa9c"/>
        <ellipse cx="300" cy="400" rx="40" ry="14" fill="#c64756"/>
        <!-- GAN hair artifact: melting strands on left side -->
        <path d="M 150 250 C 130 380 180 480 200 520 C 170 420 180 320 220 200 Z" fill="#36221a"/>
        <!-- Normal hair right -->
        <path d="M 450 250 C 470 380 420 480 400 520 C 430 420 420 320 380 200 Z" fill="#36221a"/>
      </svg>
    `),
    heatmapOverlayUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <radialGradient id="ganEyesHeat" cx="50%" cy="45%" r="40%">
            <stop offset="0%" stop-color="#ff0000" stop-opacity="0.95"/>
            <stop offset="40%" stop-color="#ff7700" stop-opacity="0.7"/>
            <stop offset="80%" stop-color="#ffff00" stop-opacity="0.3"/>
            <stop offset="100%" stop-color="#000" stop-opacity="0"/>
          </radialGradient>
        </defs>
        <circle cx="300" cy="275" r="180" fill="url(#ganEyesHeat)"/>
      </svg>
    `),
    attentionRolloutUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#0a0515"/>
        <ellipse cx="300" cy="280" rx="140" ry="90" fill="#ff0055" opacity="0.85"/>
        <ellipse cx="300" cy="280" rx="60" ry="40" fill="#ffff00" opacity="0.9"/>
      </svg>
    `),
    srmResidualUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#111"/>
        <!-- Checkerboard GAN artifact pattern -->
        <g stroke="#00e540" stroke-width="1" opacity="0.6">
          <line x1="0" y1="100" x2="600" y2="100"/><line x1="0" y1="200" x2="600" y2="200"/>
          <line x1="0" y1="300" x2="600" y2="300"/><line x1="0" y1="400" x2="600" y2="400"/>
          <line x1="100" y1="0" x2="100" y2="600"/><line x1="200" y1="0" x2="200" y2="600"/>
          <line x1="300" y1="0" x2="300" y2="600"/><line x1="400" y1="0" x2="400" y2="600"/>
        </g>
      </svg>
    `),
    fftSpectrumUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#000"/>
        <circle cx="300" cy="300" r="20" fill="#fff"/>
        <!-- 4-star checkerboard peaks from transposed convolution -->
        <circle cx="380" cy="220" r="10" fill="#ff0000"/>
        <circle cx="220" cy="220" r="10" fill="#ff0000"/>
        <circle cx="380" cy="380" r="10" fill="#ff0000"/>
        <circle cx="220" cy="380" r="10" fill="#ff0000"/>
      </svg>
    `),
    exif: {
      hasExif: false,
      software: 'None detected',
      anomalyFlag: 'Missing camera serial, lens profile, and sensor geometry tags.',
    },
    c2pa: {
      hasC2pa: false,
      validationStatus: 'none',
      trustSignal: 'No Provenance',
    },
    cues: [
      {
        id: 'cue-gan-1',
        name: 'Transposed Conv Grid',
        category: 'Spectral',
        status: 'detected',
        statusText: 'Strong Peak Array',
        description: 'Harmonic peaks in the 2D FFT spectrum caused by upsampling strided convolutions in generator architecture.',
        evidence: '4-quadrant symmetric peak ratio = 4.88x above natural photo background.',
        activationLevel: 98,
      },
      {
        id: 'cue-gan-2',
        name: 'Pupil Geometry Disparity',
        category: 'Spatial',
        status: 'abnormal',
        statusText: 'Geometric Glitch',
        description: 'Irregular contour eccentricity in pupils and mismatched specular reflections across left/right corneas.',
        evidence: 'Eye symmetry index = 0.54 (Normal human symmetry > 0.88).',
        activationLevel: 91,
      },
      {
        id: 'cue-gan-3',
        name: 'Bayer Demosaicing Absence',
        category: 'Sensor',
        status: 'missing',
        statusText: 'No CFA Trace',
        description: 'Physical sensor CFA pattern is absent in residual autocorrelation.',
        evidence: 'Autocorrelation ratio = 0.988.',
        activationLevel: 94,
      },
    ],
    summaryExplanation: 'Unambiguous GAN generation fingerprint flagged by symmetric 4-quadrant FFT peaks (transposed conv artifacts) and optical inconsistencies around facial symmetry.',
    fftStats: {
      radialSlope: -0.38,
      highFreqPeak: true,
      symmetryScore: 0.98,
    },
  },

  {
    id: 'sample-authentic',
    name: 'Alpine Sunrise (Sony A7 IV DSLR)',
    tag: 'Authentic Photographic Capture',
    description: 'Hardware camera RAW export with full optical depth of field, real sensor noise, and intact EXIF provenance.',
    sourceType: 'camera',
    confidence: 0.062,
    verdictTier: 'confident_real',
    verdictLabel: 'Likely authentic',
    generatorFamily: 'Real Camera',
    imgUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="skyGrad" x1="0%" y1="0%" x2="0%" y2="100%">
            <stop offset="0%" stop-color="#192841"/>
            <stop offset="40%" stop-color="#c96038"/>
            <stop offset="70%" stop-color="#f5a65b"/>
            <stop offset="100%" stop-color="#ffdc99"/>
          </linearGradient>
        </defs>
        <rect width="600" height="600" fill="url(#skyGrad)"/>
        <!-- Sun rising behind mountain -->
        <circle cx="340" cy="310" r="50" fill="#fff5d9" opacity="0.9"/>
        <!-- Mountain peaks with organic jagged rock facets -->
        <polygon points="40,550 220,240 380,550" fill="#1b222d"/>
        <polygon points="180,550 320,180 480,550" fill="#242e3d"/>
        <polygon points="350,550 490,290 600,550" fill="#161c24"/>
        <!-- Snow highlights -->
        <polygon points="320,180 295,240 315,225 330,250 345,220" fill="#ffffff" opacity="0.9"/>
        <!-- Foreground natural pine silhouettes -->
        <polygon points="80,600 100,500 120,600" fill="#0d141d"/>
        <polygon points="140,600 160,480 180,600" fill="#0d141d"/>
        <polygon points="480,600 500,510 520,600" fill="#0d141d"/>
      </svg>
    `),
    heatmapOverlayUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <!-- Minimal cold activation everywhere -->
        <rect width="600" height="600" fill="#0000ff" opacity="0.15"/>
      </svg>
    `),
    attentionRolloutUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#081020"/>
        <!-- Natural diffuse attention following horizon -->
        <ellipse cx="320" cy="300" rx="200" ry="60" fill="#0088ff" opacity="0.4"/>
      </svg>
    `),
    srmResidualUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#111"/>
        <filter id="authenticNoise">
          <feTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves="4" stitchTiles="stitch"/>
          <feColorMatrix type="matrix" values="0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0.33 0.33 0.33 0 0  0 0 0 0.8 0"/>
        </filter>
        <rect width="600" height="600" filter="url(#authenticNoise)"/>
      </svg>
    `),
    fftSpectrumUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#05080c"/>
        <circle cx="300" cy="300" r="280" fill="none" stroke="#10e346" stroke-width="1" opacity="0.2"/>
        <circle cx="300" cy="300" r="180" fill="none" stroke="#10e346" stroke-width="1" opacity="0.3"/>
        <circle cx="300" cy="300" r="90" fill="none" stroke="#10e346" stroke-width="1" opacity="0.5"/>
        <circle cx="300" cy="300" r="25" fill="#ffffff"/>
        <!-- Classic natural 1/f falloff without periodic spikes -->
      </svg>
    `),
    exif: {
      hasExif: true,
      cameraModel: 'Sony ILCE-7M4 (Alpha 7 IV)',
      lens: 'FE 24-70mm F2.8 GM II',
      exposure: '1/320s @ f/8.0, ISO 100',
      software: 'Sony Imaging Engine v2.01',
      iso: 100,
    },
    c2pa: {
      hasC2pa: true,
      issuer: 'Sony Digital Signature Authority',
      claimGenerator: 'Sony Alpha In-Camera Cryptographic Module',
      signingTime: '2026-09-08T06:14:22Z',
      validationStatus: 'valid',
      trustSignal: 'Strong Provenance',
    },
    cues: [
      {
        id: 'cue-auth-1',
        name: 'Natural 1/f Spectrum',
        category: 'Spectral',
        status: 'clear',
        statusText: 'Passes Physics Law',
        description: 'Radial power spectrum strictly obeys natural optical 1/f law with smooth decay into sensor noise floor.',
        evidence: 'Power law slope = -1.04 ± 0.03 (Standard natural range: -0.95 to -1.10).',
        activationLevel: 8,
      },
      {
        id: 'cue-auth-2',
        name: 'Bayer CFA Demodulation',
        category: 'Sensor',
        status: 'clear',
        statusText: 'Hardware Trace Confirmed',
        description: 'High-pass residual autocorrelation detects the 2-pixel periodic lattice created by the hardware Bayer mosaic filter.',
        evidence: 'Autocorrelation ratio = 1.184 (Exceeds 1.050 camera hardware threshold).',
        activationLevel: 96,
      },
      {
        id: 'cue-auth-3',
        name: 'Cryptographic C2PA Manifest',
        category: 'Metadata',
        status: 'clear',
        statusText: 'Valid In-Camera Signature',
        description: 'Hardware-level Content Credentials certificate chain verified without tamper.',
        evidence: 'SHA-256 manifest hash matches original sensor bitstream.',
        activationLevel: 99,
      },
    ],
    summaryExplanation: 'Image exhibits authentic photographic properties: positive Bayer CFA autocorrelation trace, continuous natural 1/f power law distribution, and valid C2PA hardware cryptographic signature.',
    fftStats: {
      radialSlope: -1.04,
      highFreqPeak: false,
      symmetryScore: 0.12,
    },
  },

  {
    id: 'sample-screenshot',
    name: 'Social Media Compressed Screenshot',
    tag: 'Degraded / Multi-Compressed',
    description: 'Image re-saved across messaging apps and screenshotted, introducing conflicting noise patterns.',
    sourceType: 'screenshot',
    confidence: 0.518,
    verdictTier: 'uncertain',
    verdictLabel: 'Uncertain — human review recommended',
    generatorFamily: 'Unknown',
    imgUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#2d3748"/>
        <!-- Heavy 8x8 blocky JPEG artifacts -->
        <g stroke="#3a485e" stroke-width="1">
          <line x1="0" y1="150" x2="600" y2="150"/><line x1="0" y1="300" x2="600" y2="300"/><line x1="0" y1="450" x2="600" y2="450"/>
          <line x1="150" y1="0" x2="150" y2="600"/><line x1="300" y1="0" x2="300" y2="600"/><line x1="450" y1="0" x2="450" y2="600"/>
        </g>
        <circle cx="300" cy="300" r="120" fill="#63b3ed" opacity="0.6"/>
        <text x="50" y="550" fill="#cbd5e0" font-family="sans-serif" font-size="16">RE-COMPRESSED MESSAGING APP EXPORT</text>
      </svg>
    `),
    heatmapOverlayUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#ffaa00" opacity="0.4"/>
      </svg>
    `),
    attentionRolloutUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#1a202c"/>
        <rect x="150" y="150" width="300" height="300" fill="#dd6b20" opacity="0.5"/>
      </svg>
    `),
    srmResidualUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#111"/>
        <!-- Block boundary artifacts -->
        <g stroke="#e2e8f0" stroke-width="2" opacity="0.4">
          <line x1="0" y1="150" x2="600" y2="150"/><line x1="0" y1="300" x2="600" y2="300"/><line x1="0" y1="450" x2="600" y2="450"/>
        </g>
      </svg>
    `),
    fftSpectrumUrl: createSvgDataUrl(`
      <svg width="600" height="600" viewBox="0 0 600 600" xmlns="http://www.w3.org/2000/svg">
        <rect width="600" height="600" fill="#000"/>
        <circle cx="300" cy="300" r="30" fill="#aaa"/>
        <!-- 8x8 block frequency grid -->
        <circle cx="360" cy="300" r="4" fill="#ffaa00"/>
        <circle cx="240" cy="300" r="4" fill="#ffaa00"/>
      </svg>
    `),
    exif: {
      hasExif: true,
      software: 'WhatsApp / WebKit Screenshot Handler',
      anomalyFlag: 'EXIF camera data stripped; replaced by screenshot utility headers.',
    },
    c2pa: {
      hasC2pa: false,
      validationStatus: 'none',
      trustSignal: 'Conflicting Signals',
    },
    cues: [
      {
        id: 'cue-scr-1',
        name: 'Double Compression Ghost',
        category: 'Spectral',
        status: 'detected',
        statusText: 'Multi-Generation JPEG',
        description: 'Re-compression ghost profile shows multiple non-aligned minima, indicating multiple lossy transcode cycles.',
        evidence: 'Ghost minima observed at Q=72 and Q=85.',
        activationLevel: 82,
      },
      {
        id: 'cue-scr-2',
        name: 'Smart Abstention Trigger',
        category: 'Physical',
        status: 'abnormal',
        statusText: 'Low Confidence Zone',
        description: 'Post-temperature calibrated confidence sits in the [0.25, 0.75] uncertainty band. Refusing binary classification to avoid false accusation.',
        evidence: 'Raw prob = 0.531, Calibrated prob = 0.518.',
        activationLevel: 52,
      },
    ],
    summaryExplanation: 'Smart Abstention Activated: Heavy lossy re-compression mask subtle high-frequency fingerprints. Rather than outputting a brittle guess, SignalScope flags this media for human review.',
    fftStats: {
      radialSlope: -0.74,
      highFreqPeak: false,
      symmetryScore: 0.44,
    },
  },
];

export const BATCH_RECORDS: BatchScanRecord[] = [
  { id: 'b-01', filename: 'IMG_8492_portrait.png', fileSize: '2.8 MB', dimensions: '1024×1024', verdict: 'Likely AI-generated', confidence: 0.962, generatorFamily: 'Diffusion-family', tier: 'confident_ai', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 412 },
  { id: 'b-02', filename: 'DSC_0034_raw_export.jpg', fileSize: '4.1 MB', dimensions: '2048×1365', verdict: 'Likely authentic', confidence: 0.041, generatorFamily: 'Real Camera', tier: 'confident_real', hasC2pa: true, hasBayerTrace: true, inferenceTimeMs: 388 },
  { id: 'b-03', filename: 'sdxl_cyber_render_v2.png', fileSize: '3.4 MB', dimensions: '1024×1024', verdict: 'Likely AI-generated', confidence: 0.895, generatorFamily: 'Diffusion-family', tier: 'confident_ai', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 425 },
  { id: 'b-04', filename: 'whatsapp_image_2026.jpg', fileSize: '480 KB', dimensions: '1280×720', verdict: 'Uncertain — human review', confidence: 0.512, generatorFamily: 'Unknown', tier: 'uncertain', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 360 },
  { id: 'b-05', filename: 'face_fashion_gan3.png', fileSize: '1.9 MB', dimensions: '1024×1024', verdict: 'Likely AI-generated', confidence: 0.944, generatorFamily: 'GAN-family', tier: 'confident_ai', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 395 },
  { id: 'b-06', filename: 'canon_eos_r5_landscape.jpg', fileSize: '5.2 MB', dimensions: '3000×2000', verdict: 'Likely authentic', confidence: 0.082, generatorFamily: 'Real Camera', tier: 'confident_real', hasC2pa: true, hasBayerTrace: true, inferenceTimeMs: 430 },
  { id: 'b-07', filename: 'midjourney_architectural.png', fileSize: '3.1 MB', dimensions: '1024×1024', verdict: 'Likely AI-generated', confidence: 0.918, generatorFamily: 'Diffusion-family', tier: 'confident_ai', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 410 },
  { id: 'b-08', filename: 'twitter_meme_clip.jpg', fileSize: '310 KB', dimensions: '800×600', verdict: 'Uncertain — human review', confidence: 0.485, generatorFamily: 'Unknown', tier: 'uncertain', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 345 },
  { id: 'b-09', filename: 'nikon_z8_wildlife.jpg', fileSize: '6.4 MB', dimensions: '2400×1600', verdict: 'Likely authentic', confidence: 0.038, generatorFamily: 'Real Camera', tier: 'confident_real', hasC2pa: true, hasBayerTrace: true, inferenceTimeMs: 442 },
  { id: 'b-10', filename: 'flux_hyperreal_concept.png', fileSize: '3.7 MB', dimensions: '1024×1024', verdict: 'Likely AI-generated', confidence: 0.931, generatorFamily: 'Diffusion-family', tier: 'confident_ai', hasC2pa: false, hasBayerTrace: false, inferenceTimeMs: 405 },
];
