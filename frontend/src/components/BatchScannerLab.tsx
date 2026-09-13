import React, { useState } from 'react';
import { BATCH_RECORDS } from '../data/mockScanData';
import { BatchScanRecord, VerdictTier } from '../types/signalscope';
import { SparkleStar } from './SparkleStar';
import { 
  Download, 
  Filter, 
  ArrowUpDown, 
  FileSpreadsheet, 
  CheckCircle, 
  ShieldAlert, 
  HelpCircle,
  FolderSync,
  Clock,
  Search
} from 'lucide-react';

export const BatchScannerLab: React.FC = () => {
  const [records, setRecords] = useState<BatchScanRecord[]>(BATCH_RECORDS);
  const [filterTier, setFilterTier] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortAsc, setSortAsc] = useState<boolean>(false);

  // Filter & Search
  const filtered = records
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

  // Export CSV generator
  const exportToCsv = () => {
    const headers = [
      'id',
      'filename',
      'dimensions',
      'file_size',
      'verdict',
      'confidence',
      'generator_family',
      'tier',
      'has_c2pa',
      'has_bayer_trace',
      'inference_time_ms'
    ];

    const rows = filtered.map((r) => [
      r.id,
      r.filename,
      r.dimensions,
      r.fileSize,
      `"${r.verdict}"`,
      r.confidence,
      `"${r.generatorFamily}"`,
      r.tier,
      r.hasC2pa,
      r.hasBayerTrace,
      r.inferenceTimeMs
    ]);

    const csvContent = [headers.join(','), ...rows.map((row) => row.join(','))].join('\n');
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', `signalscope_batch_scan_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <section id="batch" className="py-16 bg-[#060a08] text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 gap-4 border-b border-[#182a1d] pb-6">
          <div>
            <div className="inline-flex items-center gap-2 text-xs font-mono-code text-[#00e540] uppercase tracking-wider mb-2">
              <FolderSync className="w-4 h-4" />
              <span>Module F • Batch Processing Pipeline</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black font-syne tracking-tight text-white">
              BATCH FORENSIC AUDIT LAB
            </h2>
            <p className="text-sm text-gray-400 mt-1 max-w-xl">
              Simulate high-throughput folder auditing. Supports rapid multi-threaded inference with instant CSV export for enterprise compliance and media moderation.
            </p>
          </div>

          <button
            onClick={exportToCsv}
            className="inline-flex items-center gap-2 px-5 py-3 rounded-xl bg-[#00e540] hover:bg-[#10f04e] text-black font-bold text-xs sm:text-sm font-mono-code uppercase tracking-wider transition-all shadow-md shadow-[#00e540]/20 active:scale-95 self-start md:self-auto"
          >
            <Download className="w-4 h-4" />
            <span>Export CSV Report</span>
          </button>
        </div>

        {/* Filter and Search Bar */}
        <div className="bg-[#0c130f] rounded-2xl border border-[#1b3623] p-4 mb-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-2 w-full sm:w-auto">
            <span className="text-xs font-mono-code text-gray-400 mr-1 flex items-center gap-1">
              <Filter className="w-3.5 h-3.5" /> Filter:
            </span>
            <button
              onClick={() => setFilterTier('all')}
              className={`text-xs px-3 py-1.5 rounded-lg font-mono-code transition-all ${
                filterTier === 'all'
                  ? 'bg-[#00e540] text-black font-bold'
                  : 'bg-white/5 text-gray-300 hover:text-white'
              }`}
            >
              All ({records.length})
            </button>
            <button
              onClick={() => setFilterTier('confident_ai')}
              className={`text-xs px-3 py-1.5 rounded-lg font-mono-code transition-all ${
                filterTier === 'confident_ai'
                  ? 'bg-red-500 text-white font-bold'
                  : 'bg-white/5 text-red-300 hover:text-white'
              }`}
            >
              Likely AI ({records.filter((r) => r.tier === 'confident_ai').length})
            </button>
            <button
              onClick={() => setFilterTier('confident_real')}
              className={`text-xs px-3 py-1.5 rounded-lg font-mono-code transition-all ${
                filterTier === 'confident_real'
                  ? 'bg-[#00e540] text-black font-bold'
                  : 'bg-white/5 text-emerald-300 hover:text-white'
              }`}
            >
              Authentic ({records.filter((r) => r.tier === 'confident_real').length})
            </button>
            <button
              onClick={() => setFilterTier('uncertain')}
              className={`text-xs px-3 py-1.5 rounded-lg font-mono-code transition-all ${
                filterTier === 'uncertain'
                  ? 'bg-amber-500 text-black font-bold'
                  : 'bg-white/5 text-amber-300 hover:text-white'
              }`}
            >
              Uncertain ({records.filter((r) => r.tier === 'uncertain').length})
            </button>
          </div>

          <div className="flex items-center gap-3 w-full sm:w-auto">
            {/* Search */}
            <div className="relative flex-1 sm:w-48">
              <Search className="w-3.5 h-3.5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search file name..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full bg-[#121c15] text-xs text-white pl-8 pr-3 py-1.5 rounded-lg border border-[#223d29] focus:outline-none focus:border-[#00e540]"
              />
            </div>

            {/* Sort Toggle */}
            <button
              onClick={() => setSortAsc(!sortAsc)}
              className="flex items-center gap-1.5 text-xs font-mono-code px-3 py-1.5 rounded-lg bg-[#121c15] border border-[#223d29] text-gray-300 hover:text-white shrink-0"
            >
              <ArrowUpDown className="w-3.5 h-3.5 text-[#00e540]" />
              <span>{sortAsc ? 'Lowest AI %' : 'Highest AI %'}</span>
            </button>
          </div>
        </div>

        {/* BATCH RESULTS TABLE */}
        <div className="bg-[#0c130f] rounded-2xl border border-[#1b3623] overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs border-collapse">
              <thead>
                <tr className="border-b border-[#1b3623] text-gray-400 font-mono-code bg-[#101913]">
                  <th className="py-3 px-4 uppercase">Filename</th>
                  <th className="py-3 px-4 uppercase">Verdict</th>
                  <th className="py-3 px-4 uppercase">Confidence</th>
                  <th className="py-3 px-4 uppercase">Generator Attribution</th>
                  <th className="py-3 px-4 uppercase">C2PA Trust</th>
                  <th className="py-3 px-4 uppercase">Bayer CFA Trace</th>
                  <th className="py-3 px-4 uppercase">Latency</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-[#1b3623]/60 text-gray-300">
                {filtered.map((item) => {
                  return (
                    <tr key={item.id} className="hover:bg-white/5 transition-colors">
                      <td className="py-3.5 px-4 font-bold text-white font-mono-code">
                        <div className="flex flex-col">
                          <span>{item.filename}</span>
                          <span className="text-[10px] text-gray-500 font-normal">
                            {item.dimensions} • {item.fileSize}
                          </span>
                        </div>
                      </td>

                      <td className="py-3.5 px-4">
                        <span
                          className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full font-mono-code font-bold text-[11px] ${
                            item.tier === 'confident_ai'
                              ? 'bg-red-500/15 text-red-400 border border-red-500/30'
                              : item.tier === 'confident_real'
                              ? 'bg-[#00e540]/15 text-[#00e540] border border-[#00e540]/30'
                              : 'bg-amber-500/15 text-amber-400 border border-amber-500/30'
                          }`}
                        >
                          <span
                            className={`w-1.5 h-1.5 rounded-full ${
                              item.tier === 'confident_ai'
                                ? 'bg-red-500'
                                : item.tier === 'confident_real'
                                ? 'bg-[#00e540]'
                                : 'bg-amber-500'
                            }`}
                          />
                          {item.verdict}
                        </span>
                      </td>

                      <td className="py-3.5 px-4 font-mono-code font-bold text-sm">
                        <span
                          className={
                            item.tier === 'confident_ai'
                              ? 'text-red-400'
                              : item.tier === 'confident_real'
                              ? 'text-[#00e540]'
                              : 'text-amber-400'
                          }
                        >
                          {(item.confidence * 100).toFixed(1)}%
                        </span>
                      </td>

                      <td className="py-3.5 px-4 font-display font-medium text-white">
                        {item.generatorFamily}
                      </td>

                      <td className="py-3.5 px-4 font-mono-code text-[11px]">
                        {item.hasC2pa ? (
                          <span className="text-[#00e540] font-bold">Valid Manifest</span>
                        ) : (
                          <span className="text-gray-500">None</span>
                        )}
                      </td>

                      <td className="py-3.5 px-4 font-mono-code text-[11px]">
                        {item.hasBayerTrace ? (
                          <span className="text-[#00e540] font-bold">Hardware Trace (Confirmed)</span>
                        ) : (
                          <span className="text-red-400">Absent (Synthetic)</span>
                        )}
                      </td>

                      <td className="py-3.5 px-4 font-mono-code text-gray-400 text-[11px]">
                        {item.inferenceTimeMs} ms
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </section>
  );
};
