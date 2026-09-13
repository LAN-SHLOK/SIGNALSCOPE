# SignalScope REST API Reference

The SignalScope backend exposes a high-performance REST API powered by FastAPI.

### Base URL
```
http://localhost:8000
```

---

### Endpoints

#### 1. `GET /api/health`
Health check and device readiness status.
- **Response**: `200 OK`
```json
{
  "status": "healthy",
  "service": "SignalScope Authenticity API",
  "version": "1.0.0",
  "device": "CPU / DirectML"
}
```

#### 2. `POST /api/analyze`
Inspect a single image file for AI generation artifacts and camera provenance.
- **Content-Type**: `multipart/form-data`
- **Body**: `file` (binary image data: JPEG, PNG, WebP)
- **Response**: `200 OK`
```json
{
  "id": "scan-1726214500000",
  "name": "sample.jpg",
  "tag": "Live Forensics",
  "sourceType": "camera",
  "confidence": 0.94,
  "verdictTier": "confident_real",
  "verdictLabel": "Likely Real Camera Photo",
  "generatorFamily": "Real Camera",
  "imgUrl": "data:image/jpeg;base64,...",
  "heatmapOverlayUrl": "data:image/jpeg;base64,...",
  "attentionRolloutUrl": "data:image/jpeg;base64,...",
  "srmResidualUrl": "data:image/jpeg;base64,...",
  "fftSpectrumUrl": "data:image/jpeg;base64,...",
  "exif": {
    "hasExif": true,
    "cameraModel": "Sony Alpha A7 IV",
    "lens": "FE 24-70mm F2.8 GM II",
    "exposure": "1/250s",
    "software": null,
    "iso": 100,
    "anomalyFlag": null
  },
  "c2pa": {
    "hasC2pa": false,
    "validationStatus": "none",
    "trustSignal": "No Provenance"
  },
  "cues": [...],
  "fftStats": {
    "radialSlope": -1.82,
    "highFreqPeak": false,
    "symmetryScore": 0.41
  }
}
```

#### 3. `POST /api/batch`
Inspect multiple image files in parallel.
- **Content-Type**: `multipart/form-data`
- **Body**: `files` (array of image files)
- **Response**: `200 OK` with array of batch summary rows.
