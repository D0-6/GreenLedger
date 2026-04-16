"use client";

import React, { useState } from 'react';

interface ForensicModuleProps {
  onAnalyze: (claim: string) => void;
  logs: Array<{ icon: string; text: string; status?: string }>;
}

const ForensicModule: React.FC<ForensicModuleProps> = ({ onAnalyze, logs }) => {
  const [input, setInput] = useState('');

  return (
    <div className="grid grid-cols-1 md:grid-cols-12 border border-[#a9b4b9] bg-white">
      <div className="md:col-span-8 p-8 border-b md:border-b-0 md:border-r border-[#a9b4b9]">
        <h3 className="text-xl font-bold text-[#565e74] mb-2">Step 1: Enter ESG Claim</h3>
        <label className="block text-[10px] font-bold uppercase tracking-[0.1em] text-[#566166] mb-4">
          Verification Input Terminal
        </label>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          className="w-full bg-[#f7f9fb] border border-[#a9b4b9] focus:ring-0 focus:border-[#565e74] p-4 font-mono text-sm resize-none"
          placeholder="Paste corporate sustainability claim string here (e.g. 'We will be net zero by 2040')"
          rows={8}
        />
        <div className="mt-6 flex justify-between items-center">
          <div className="flex gap-4">
            <span className="text-[10px] text-[#566166] font-medium uppercase tracking-widest">Verification Engine: Active</span>
          </div>
          <button
            onClick={() => onAnalyze(input)}
            className="bg-[#565e74] text-white px-6 py-3 rounded-sm font-bold text-xs uppercase tracking-widest hover:bg-[#4a5268] transition-colors shadow-sm"
          >
            Analyze a Claim Now
          </button>
        </div>
      </div>
      <div className="md:col-span-4 p-8 flex flex-col justify-between bg-[#f0f4f7]">
        <div>
          <h4 className="text-[10px] font-bold uppercase tracking-[0.1em] text-[#566166] mb-6 underline decoration-[#a9b4b9] underline-offset-4">Analysis Pipeline</h4>
          <ul className="space-y-4">
            {logs.map((log, index) => (
              <li key={index} className="flex gap-3 items-start">
                <span className="text-sm text-[#565e74]">{log.icon}</span>
                <span className="text-[11px] font-mono leading-tight">
                  {log.text} {log.status && <span className="text-[#565e74] font-bold">{log.status}</span>}
                </span>
              </li>
            ))}
          </ul>
        </div>
        <div className="pt-8 border-t border-[#a9b4b9] mt-8">
          <p className="text-[10px] text-[#566166] italic leading-normal">
            *All analyses are timestamped and committed to the GreenLedger immutable store.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ForensicModule;
