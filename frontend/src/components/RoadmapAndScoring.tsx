import React, { useState } from 'react';
import { SparkleStar } from './SparkleStar';
import { 
  Trophy, 
  CheckCircle2, 
  Calendar, 
  Terminal, 
  Award, 
  FileText, 
  Clock, 
  AlertCircle,
  Code2,
  Copy,
  Check
} from 'lucide-react';

export const RoadmapAndScoring: React.FC = () => {
  const [copiedCode, setCopiedCode] = useState<boolean>(false);
  const [activeDay, setActiveDay] = useState<number>(1);

  const scoringAxes = [
    {
      axis: 'AI/ML Implementation',
      points: 25,
      target: '23–25',
      summary: 'DINOv2 + SRM dual-stream; multi-layer features; LightGBM stacking; calibrated confidence; unseen-gen AUC ≥ 0.88'
    },
    {
      axis: 'Technical Implementation',
      points: 20,
      target: '18–20',
      summary: 'Docker reproducibility; one-command predict.py; clean code; comprehensive README'
    },
    {
      axis: 'Innovation & Creativity',
      points: 15,
      target: '13–15',
      summary: 'Multi-colorspace SRM; multi-layer DINOv2; JPEG ghost analysis; Bayer autocorrelation; patch token statistics'
    },
    {
      axis: 'Explanation & Trust Impact',
      points: 15,
      target: '13–15',
      summary: 'Attention Rollout + Grad-CAM heatmaps; grounded forensic cue descriptors; responsible likely framing'
    },
    {
      axis: 'User Experience',
      points: 10,
      target: '9–10',
      summary: 'Web app with drag-and-drop, batch scan, heatmap slider, CSV export, smart abstention'
    },
    {
      axis: 'Problem Understanding',
      points: 10,
      target: '9–10',
      summary: 'Honest limitations; degradation-vs-accuracy curves; unseen-generator analysis; threshold optimization'
    },
    {
      axis: 'Presentation & Demo',
      points: 5,
      target: '5',
      summary: '3–5 min video showing full pipeline on novel images'
    },
  ];

  const scheduleDays = [
    {
      day: 1,
      date: 'September 10',
      title: 'Foundation & Data Pipeline',
      status: 'Completed',
      focus: 'Data pipeline, all frozen feature extractors (DINOv2, SRM 9ch, FFT, JPEG ghost, Bayer). Prepares 7,575-dim output pipeline.',
      deliverable: 'Feature extraction pipeline ready. Given any image → outputs 7,575-dim vector.'
    },
    {
      day: 2,
      date: 'September 11',
      title: 'DINOv2 Backbone + Training',
      status: 'Completed',
      focus: 'Pre-cache DINOv2 features for training images (~1hr on T4). Train SpectralCNN, SpectralMLP, and Fusion MLP with CosineAnnealing + FP16 mixed precision.',
      deliverable: 'Trained model with baseline metrics on validation set.'
    },
    {
      day: 3,
      date: 'September 12',
      title: 'Calibration, XAI & Predict Interface',
      status: 'Completed',
      focus: 'Temperature scaling calibration (ECE < 0.04), LightGBM meta-stacking, Attention Rollout + Grad-CAM++ heatmap fusion, model/predict.py CLI tool.',
      deliverable: 'python model/predict.py --image test.jpg --explain runs end-to-end.'
    },
    {
      day: 4,
      date: 'September 13',
      title: 'Bonus Modules + Interactive Web App',
      status: 'On Track',
      focus: 'Module C degradation battery suite (15+ transforms), Module D EXIF/C2PA metadata checkers, Module F interactive web application and batch scanner.',
      deliverable: 'Complete working system with all bonus modules and responsive UI.'
    },
    {
      day: 5,
      date: 'September 14–15',
      title: 'Report, Demo Video & Submission',
      status: 'On Track',
      focus: 'One-page model_report.md, comprehensive README.md (<10 min reproduction), Dockerfile, 3–5 min demo video, GitHub release weights upload.',
      deliverable: 'Final verified submission ready for SIH evaluation.'
    },
  ];

  const copyPredictSnippet = () => {
    navigator.clipboard.writeText('python model/predict.py --image sample.jpg --explain');
    setCopiedCode(true);
    setTimeout(() => setCopiedCode(false), 2000);
  };

  return (
    <section id="roadmap" className="py-16 bg-[#090d0b] text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Section Header */}
        <div className="mb-10 text-center max-w-3xl mx-auto">
          <div className="inline-flex items-center gap-2 text-xs font-mono-code text-[#00e540] uppercase tracking-wider mb-2">
            <Trophy className="w-4 h-4" />
            <span>Sections 2, 8, 9 & 10 • Evaluation & Execution</span>
          </div>
          <h2 className="text-3xl sm:text-5xl font-black font-syne tracking-tight text-white mb-3">
            HACKATHON SCORING & ROADMAP
          </h2>
          <p className="text-sm sm:text-base text-gray-400">
            Targeting 90–100 points out of 100 points. Built to decisively win on the #1 tie-breaker metric: Unseen-Generator Split AUC.
          </p>
        </div>

        {/* TIE-BREAKER SPOTLIGHT CARD */}
        <div className="bg-[#101913] rounded-3xl border-2 border-[#00e540]/60 p-6 sm:p-8 mb-10 shadow-[0_0_30px_rgba(0,229,64,0.15)]">
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4 border-b border-[#1c3623] pb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-[#00e540] flex items-center justify-center text-black font-black font-syne">
                #1
              </div>
              <div>
                <span className="text-xs font-mono-code text-[#00e540] font-bold uppercase">
                  Official SIH Tie-Break Order
                </span>
                <h3 className="text-xl sm:text-2xl font-black font-syne text-white">
                  HOW WINNERS ARE DECIDED
                </h3>
              </div>
            </div>
            <span className="text-xs font-mono-code px-3 py-1 rounded-full bg-[#00e540]/20 text-[#00e540] border border-[#00e540]/40 font-bold self-start md:self-auto">
              Our Core Architecture Advantage
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-[#090d0b] border border-[#00e540]/40">
              <span className="text-base font-black font-syne text-[#00e540] block mb-1">
                1. Unseen-Gen Split AUC
              </span>
              <p className="text-gray-300">
                Highest wins. DINOv2 self-supervision + SRM noise filters specifically prevent overfitting to known models.
              </p>
            </div>
            <div className="p-4 rounded-xl bg-[#090d0b] border border-[#1c3623]">
              <span className="text-base font-black font-syne text-white block mb-1">
                2. Overall Held-Out AUC
              </span>
              <p className="text-gray-400">
                Full benchmark performance with temperature-calibrated confidence (target &ge; 0.94).
              </p>
            </div>
            <div className="p-4 rounded-xl bg-[#090d0b] border border-[#1c3623]">
              <span className="text-base font-black font-syne text-white block mb-1">
                3. Reproducibility
              </span>
              <p className="text-gray-400">
                One-command execution via Docker or standard pip virtualenv with deterministic seeds.
              </p>
            </div>
            <div className="p-4 rounded-xl bg-[#090d0b] border border-[#1c3623]">
              <span className="text-base font-black font-syne text-white block mb-1">
                4. XAI Faithfulness Score
              </span>
              <p className="text-gray-400">
                37×37 attention rollouts and grounded forensic cues that directly correspond to anomalous pixel activations.
              </p>
            </div>
          </div>
        </div>

        {/* 6 EVALUATION AXES TABLE */}
        <div className="bg-[#0c130f] rounded-3xl border border-[#1b3623] p-6 sm:p-8 mb-10">
          <div className="flex items-center justify-between mb-6">
            <div>
              <span className="text-xs font-mono-code text-[#00e540] uppercase tracking-wider">
                Full Evaluation Rubric
              </span>
              <h3 className="text-2xl font-black font-syne text-white mt-0.5">
                SCORING STRATEGY (100 TOTAL POINTS)
              </h3>
            </div>
            <div className="text-right">
              <span className="text-xs font-mono-code text-gray-400 block">Target Total</span>
              <span className="text-2xl font-black font-syne text-[#00e540]">90–100 / 100</span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-[#1b3623] text-gray-400 font-mono-code bg-[#101913]">
                  <th className="py-3 px-4 uppercase">Evaluation Axis</th>
                  <th className="py-3 px-4 uppercase text-center">Max Weight</th>
                  <th className="py-3 px-4 uppercase text-center">Target</th>
                  <th className="py-3 px-4 uppercase">How We Win (Technical Execution)</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1b3623]/60 text-gray-300">
                {scoringAxes.map((axis) => (
                  <tr key={axis.axis} className="hover:bg-white/5 transition-colors">
                    <td className="py-3 px-4 font-bold text-white font-display">
                      {axis.axis}
                    </td>
                    <td className="py-3 px-4 font-mono-code text-center font-bold text-white">
                      {axis.points} pts
                    </td>
                    <td className="py-3 px-4 font-mono-code text-center font-bold text-[#00e540]">
                      {axis.target}
                    </td>
                    <td className="py-3 px-4 text-gray-300">
                      {axis.summary}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 5-DAY TIMELINE & ONE-COMMAND PREDICT CLI */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* 5-Day Schedule (7 Cols) */}
          <div className="lg:col-span-7 bg-[#0c130f] rounded-3xl border border-[#1b3623] p-6">
            <div className="flex items-center justify-between mb-4 border-b border-[#1b3623] pb-3">
              <h3 className="text-lg font-black font-syne text-white flex items-center gap-2">
                <Calendar className="w-4 h-4 text-[#00e540]" />
                <span>5-Day Execution Schedule</span>
              </h3>
              <span className="text-xs font-mono-code text-[#00e540]">
                Sep 10–15, 2026
              </span>
            </div>

            <div className="space-y-3">
              {scheduleDays.map((item) => (
                <div
                  key={item.day}
                  className="p-3.5 rounded-xl bg-[#101913] border border-[#1b3623] hover:border-[#00e540]/40 transition-all"
                >
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono-code text-xs font-bold px-2 py-0.5 rounded bg-[#00e540]/20 text-[#00e540]">
                        Day {item.day}
                      </span>
                      <span className="font-display font-bold text-white text-xs sm:text-sm">
                        {item.title}
                      </span>
                    </div>
                    <span className="text-[11px] font-mono-code text-gray-400">
                      {item.date}
                    </span>
                  </div>
                  <p className="text-xs text-gray-300 mb-2 leading-relaxed">
                    {item.focus}
                  </p>
                  <div className="text-[11px] font-mono-code text-[#00e540] bg-black/40 px-2.5 py-1 rounded flex items-center justify-between">
                    <span className="truncate">Key Milestone: {item.deliverable}</span>
                    <span className="text-xs ml-2">✓</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* ONE-COMMAND PREDICT CLI TERMINAL (5 Cols) */}
          <div className="lg:col-span-5 bg-[#0c130f] rounded-3xl border border-[#1b3623] p-6 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4 border-b border-[#1b3623] pb-3">
                <h3 className="text-lg font-black font-syne text-white flex items-center gap-2">
                  <Terminal className="w-4 h-4 text-[#00e540]" />
                  <span>Section 8: Predict Interface</span>
                </h3>
                <span className="text-[10px] font-mono-code px-2 py-0.5 rounded bg-white/10 text-gray-300">
                  Required by Judges
                </span>
              </div>

              <p className="text-xs text-gray-400 mb-4 leading-relaxed">
                Standard one-command interface compliant with Section 4.1 for external automated evaluation:
              </p>

              {/* Terminal code snippet */}
              <div className="bg-black rounded-xl p-3.5 border border-white/10 font-mono-code text-xs text-gray-300 relative mb-4">
                <div className="flex items-center justify-between pb-2 mb-2 border-b border-white/10 text-[10px] text-gray-400">
                  <span>bash terminal</span>
                  <button
                    onClick={copyPredictSnippet}
                    className="flex items-center gap-1 hover:text-white transition-colors"
                  >
                    {copiedCode ? <Check className="w-3 h-3 text-[#00e540]" /> : <Copy className="w-3 h-3" />}
                    <span>{copiedCode ? 'Copied' : 'Copy'}</span>
                  </button>
                </div>
                <div className="text-[#00e540] select-all">
                  $ python model/predict.py \<br />
                  &nbsp;&nbsp;--image sample.jpg \<br />
                  &nbsp;&nbsp;--explain
                </div>
              </div>

              {/* Sample output preview */}
              <div className="bg-[#050806] rounded-xl p-3 border border-[#18291c] font-mono-code text-[11px] text-gray-300 space-y-1">
                <div className="text-gray-400">// JSON Evaluation Output:</div>
                <div className="text-yellow-400">&#123;</div>
                <div className="pl-3 text-gray-300">"label": <span className="text-[#00e540]">"AI-generated"</span>,</div>
                <div className="pl-3 text-gray-300">"confidence": <span className="text-[#00e540]">0.884</span>,</div>
                <div className="pl-3 text-gray-300">"verdict": <span className="text-white">"Likely AI-generated"</span>,</div>
                <div className="pl-3 text-gray-300">"generator_family": <span className="text-cyan-300">"Diffusion-family"</span>,</div>
                <div className="pl-3 text-gray-300">"metadata": &#123; "has_exif": false, "has_c2pa": false &#125;,</div>
                <div className="pl-3 text-gray-300">"heatmap_path": <span className="text-white">"output/heatmap.png"</span></div>
                <div className="text-yellow-400">&#125;</div>
              </div>
            </div>

            {/* Docker execution box */}
            <div className="mt-6 pt-4 border-t border-[#1b3623] text-xs text-gray-400">
              <span className="text-white font-bold block mb-1 font-mono-code">Docker Reproducibility:</span>
              <code>docker build -t signalscope . && docker run -p 8000:8000 signalscope</code>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};
