export type VerdictTier = 'confident_ai' | 'confident_real' | 'uncertain';

export interface ForensicCue {
  id: string;
  name: string;
  category: 'Spectral' | 'Spatial' | 'Metadata' | 'Physical' | 'Sensor';
  status: 'detected' | 'clear' | 'abnormal' | 'missing';
  statusText: string;
  description: string;
  evidence: string;
  activationLevel: number; // 0-100%
}

export interface ExifData {
  hasExif: boolean;
  cameraModel?: string;
  lens?: string;
  exposure?: string;
  software?: string;
  iso?: number;
  anomalyFlag?: string;
}

export interface C2paData {
  hasC2pa: boolean;
  issuer?: string;
  claimGenerator?: string;
  signingTime?: string;
  validationStatus: 'valid' | 'invalid' | 'none';
  trustSignal: 'Strong Provenance' | 'No Provenance' | 'Conflicting Signals' | 'AI Manifest Detected';
}

export interface SampleImage {
  id: string;
  name: string;
  tag: string;
  description: string;
  sourceType: 'diffusion' | 'gan' | 'camera' | 'screenshot';
  confidence: number;
  verdictTier: VerdictTier;
  verdictLabel: string;
  generatorFamily: 'Diffusion-family' | 'GAN-family' | 'Real Camera' | 'Unknown';
  imgUrl: string;
  heatmapOverlayUrl: string;
  attentionRolloutUrl: string;
  srmResidualUrl: string;
  fftSpectrumUrl: string;
  exif: ExifData;
  c2pa: C2paData;
  cues: ForensicCue[];
  summaryExplanation: string;
  fftStats: {
    radialSlope: number;
    highFreqPeak: boolean;
    symmetryScore: number;
  };
}

export interface BatchScanRecord {
  id: string;
  filename: string;
  fileSize: string;
  dimensions: string;
  verdict: string;
  confidence: number;
  generatorFamily: string;
  tier: VerdictTier;
  hasC2pa: boolean;
  hasBayerTrace: boolean;
  inferenceTimeMs: number;
}

export interface ArchitectureNode {
  id: string;
  stream: 'stream1' | 'stream2' | 'fusion' | 'inference' | 'xai';
  title: string;
  badge: string;
  dim?: string;
  frozen?: boolean;
  description: string;
  whyItWins: string;
}
