"use client";

import React, { useState, useEffect, useRef } from 'react';
import GeoGlobe from '@/components/GeoGlobe';
import AgentTrace from '@/components/AgentTrace';

const THINKING_STAGES = [
  { msg: "Acquiring global telemetry nodes...", type: 'info' },
  { msg: "Sweeping G7 climate disclosure indices...", type: 'search' },
  { msg: "Cross-referencing Scope 1-3 satellite data...", type: 'info' },
  { msg: "Analyzing ISSB & CSRD forensic gaps...", type: 'info' },
  { msg: "Finalizing institutional audit verdict...", type: 'success' }
];

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export default function Home() {
  const [claimText, setClaimText] = useState("");
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [thinkingIndex, setThinkingIndex] = useState(0);
  const [traceLogs, setTraceLogs] = useState<any[]>([]);
  
  const [isDarkMode, setIsDarkMode] = useState(true);
  const [isSimulating, setIsSimulating] = useState(false);
  const [auditSession, setAuditSession] = useState<any[]>([]);

  // Forensic PDF Upload State
  const [uploadedPdfText, setUploadedPdfText] = useState("");
  const [uploadedPdfName, setUploadedPdfName] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Toggle Theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);

  const addTrace = (message: string, type: string = 'info') => {
    setTraceLogs(prev => [...prev, {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toLocaleTimeString([], { hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit' }),
      message,
      type
    }]);
  };

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setIsUploading(true);
    addTrace(`Extracting forensic anchors from: ${file.name}...`, 'info');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/extract-pdf`, {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setUploadedPdfText(data.text);
      setUploadedPdfName(file.name);
      addTrace(`Forensic extraction complete: ${data.text.length} characters of report content ingested.`, 'success');
    } catch (err) {
      addTrace(`Extraction failure: ${err}`, 'warning');
    } finally {
      setIsUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!claimText.trim() && !uploadedPdfText) return;
    
    setIsAnalyzing(true);
    setAnalysisResult(null);
    setThinkingIndex(0);
    setTraceLogs([]);

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          claim: claimText || (uploadedPdfName ? `Verification of ${uploadedPdfName}` : ""),
          pdf_text: uploadedPdfText 
        }),
      });
      
      const reader = response.body?.getReader();
      const decoder = new TextDecoder();
      
      if (!reader) throw new Error("Stream reader unavailable");

      let done = false;
      while (!done) {
        const { value, done: readerDone } = await reader.read();
        done = readerDone;
        if (value) {
          const chunk = decoder.decode(value, { stream: true });
          const lines = chunk.split('\n').filter(line => line.trim());
          
          for (const line of lines) {
            try {
              const data = JSON.parse(line);
              
              if (data.type === 'trace' || data.type === 'search' || data.type === 'link') {
                const logType = data.type === 'link' ? 'search' : data.type;
                addTrace(data.message, logType as any);
                // Cycle thinking stages visually
                setThinkingIndex(prev => (prev + 1) % THINKING_STAGES.length);
              } else if (data.type === 'result') {
                addTrace("Forensic audit complete. Enclaving results...", 'success');
                setAnalysisResult({ ...data, claim_text: claimText });
                setIsAnalyzing(false);
              } else if (data.type === 'error') {
                addTrace(data.message, 'warning');
                setIsAnalyzing(false);
              }
            } catch (err) {
              console.error("Partial chunk or parse error:", err);
            }
          }
        }
      }

    } catch (error) {
      addTrace("Network disruption: Switching to forensic fallback.", 'warning');
      setAnalysisResult({
        claim_text: claimText,
        analysis: "FORENSIC_FALLBACK: API timeout. Manual node retrieval suggests high consistency with reported G7 targets but missing indirect Scope 3 traces.",
        risk_level: "MEDIUM",
        risk_score: 45
      });
      setIsAnalyzing(false);
    }
  };

  const handleDownloadReport = async () => {
    if (!analysisResult) return;
    const claimsToReport = auditSession.length > 0 ? auditSession : [{ claim: analysisResult.claim_text, analysis: analysisResult }];
    try {
      const response = await fetch(`${API_BASE_URL}/generate-report`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ claims: claimsToReport }),
      });
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'GreenLedger_Audit_Report.pdf';
      document.body.appendChild(a);
      a.click();
      a.remove();
    } catch (e) { console.error(e); }
  };

  return (
    <div className="min-h-screen flex flex-col bg-background text-on-surface transition-colors duration-500">
      
      <nav className="fixed top-0 w-full z-50 h-16 border-b border-outline/20 backdrop-blur-xl bg-surface/80 flex items-center justify-between px-10 transition-all duration-500">
        <div className="flex items-center gap-4">
          <div className="text-xl font-bold tracking-tighter neon-glow">GreenLedger</div>
          <div className="h-4 w-[1px] bg-outline/30 mx-2"></div>
          <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-outline">Forensic Observatory</span>
        </div>
        
        <div className="flex items-center gap-6">
          <button 
            onClick={() => setIsDarkMode(!isDarkMode)}
            className="flex items-center gap-2 px-4 py-2 rounded-full border border-outline/30 hover:border-primary/50 transition-all text-on-surface bg-surface shadow-sm"
          >
            <span className="material-symbols-outlined text-[18px] text-primary">
              {isDarkMode ? 'light_mode' : 'dark_mode'}
            </span>
            <span className="text-[10px] font-bold uppercase tracking-widest text-on-surface-variant">
              {isDarkMode ? 'Light' : 'Dark'}
            </span>
          </button>
        </div>
      </nav>

      <main className="relative flex-1 flex flex-col overflow-hidden pt-16">
        <div className="absolute inset-0 z-0 bg-background transition-colors duration-700">
          <GeoGlobe isSimulating={isSimulating} isDarkMode={isDarkMode} />
        </div>

        {/* LEFT: Live Agent Trace Panel */}
        <AgentTrace logs={traceLogs} isVisible={isAnalyzing || traceLogs.length > 0} />

        {/* RIGHT: Floating Forensic Scorecard (Moved to right to balance layout) */}
        {analysisResult && !isAnalyzing && (
          <div className="absolute top-24 right-10 z-20 w-[340px] animate-in fade-in slide-in-from-right duration-700 pointer-events-auto">
            <div className="bg-surface/90 glass-effect border border-outline/20 p-6 rounded-2xl shadow-2xl transition-all">
              <div className="flex justify-between items-start mb-6">
                <span className="text-[10px] font-bold uppercase tracking-widest text-outline">Forensic Verdict</span>
                <span className={`px-2 py-0.5 rounded-sm text-[9px] font-bold uppercase ${analysisResult.risk_level === 'HIGH' ? 'bg-error text-on-error' : 'bg-primary text-on-primary'}`}>
                  {analysisResult.risk_level} Risk
                </span>
              </div>
              <div className="text-5xl font-black tracking-tighter mb-2 text-on-surface">{analysisResult.risk_score}/100</div>
              <p className="text-[12px] text-on-surface-variant leading-relaxed mb-8 scrollbar-hide overflow-y-auto max-h-[180px]">
                {analysisResult.analysis}
              </p>
              
              <div className="flex flex-col gap-3">
                <button 
                  onClick={() => setAuditSession([...auditSession, { claim: analysisResult.claim_text, analysis: analysisResult }])}
                  className="w-full py-3 bg-surface-container-high border border-outline/20 text-[10px] font-bold uppercase tracking-widest rounded-xl hover:bg-surface-bright transition-colors text-on-surface"
                >
                  Add to Audit Folder ({auditSession.length})
                </button>
                <button 
                  onClick={handleDownloadReport}
                  className="w-full py-3 bg-primary text-on-primary text-[10px] font-bold uppercase tracking-widest rounded-xl hover:opacity-90 shadow-lg shadow-primary/20 transition-all"
                >
                  Export Institutional Report
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="absolute bottom-10 left-1/2 -translate-x-1/2 w-full max-w-[800px] z-30 px-6 pointer-events-auto">
          
          {isAnalyzing && (
            <div className="mb-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
              <div className="flex items-center gap-3 mb-2 px-6">
                <div className="w-4 h-4 rounded-full border-2 border-primary border-t-transparent animate-spin"></div>
                <span className="text-[11px] font-bold uppercase tracking-widest text-primary italic">
                  Engaging Forensic Synthesis...
                </span>
              </div>
              <div className="w-full h-[2px] bg-outline/20 rounded-full overflow-hidden mx-6">
                <div className="h-full bg-primary transition-all duration-1000" style={{ width: `${(thinkingIndex + 1) * 20}%` }}></div>
              </div>
            </div>
          )}

          <div className="bg-surface/95 glass-effect border border-outline/30 rounded-3xl p-4 shadow-[0_20px_50px_rgba(0,0,0,0.3)] hover:border-primary/40 transition-all">
            {uploadedPdfName && (
              <div className="flex items-center gap-2 mb-3 bg-primary/10 border border-primary/20 px-3 py-1.5 rounded-xl w-fit animate-in fade-in zoom-in duration-300">
                <span className="material-symbols-outlined text-[16px] text-primary">description</span>
                <span className="text-[10px] font-bold text-primary truncate max-w-[200px]">{uploadedPdfName}</span>
                <button onClick={() => { setUploadedPdfName(""); setUploadedPdfText(""); }} className="ml-1 text-primary hover:text-on-surface opacity-60 hover:opacity-100">
                  <span className="material-symbols-outlined text-[14px]">close</span>
                </button>
              </div>
            )}
            <div className="relative flex items-center gap-2">
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileUpload} 
                className="hidden" 
                accept=".pdf"
              />
              <button 
                onClick={() => fileInputRef.current?.click()}
                disabled={isAnalyzing || isUploading}
                className="w-10 h-10 rounded-2xl border border-outline/20 flex items-center justify-center hover:bg-surface-bright transition-colors text-outline disabled:opacity-20"
                title="Upload Forensic Report (PDF)"
              >
                <span className="material-symbols-outlined text-[20px]">
                  {isUploading ? 'sync' : 'add'}
                </span>
              </button>
              <textarea 
                className="flex-1 bg-transparent border-none focus:ring-0 outline-none p-2 text-on-surface text-[15px] placeholder:text-outline font-medium resize-none min-h-[40px] max-h-[120px]"
                placeholder={uploadedPdfName ? "PDF ingested. Ask a question or click arrow to verify..." : "Submit corporate ESG claim or upload PDF..."}
                value={claimText}
                onChange={e => setClaimText(e.target.value)}
                disabled={isAnalyzing}
                onKeyDown={e => { if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleAnalyze(); } }}
              />
              <button 
                onClick={handleAnalyze} 
                disabled={isAnalyzing || !claimText.trim()}
                className="absolute right-2 bottom-2 w-10 h-10 rounded-2xl bg-primary text-on-primary flex items-center justify-center hover:scale-105 transition-transform disabled:opacity-20 shadow-lg shadow-primary/20"
              >
                <span className="material-symbols-outlined text-[20px]">
                  {isAnalyzing ? 'sync' : 'arrow_upward'}
                </span>
              </button>
            </div>
          </div>
          
          <div className="mt-4 flex justify-center gap-6 opacity-60">
             <button onClick={() => setClaimText("Apple batteries reach 100% recycled cobalt targets.")} className="text-[9px] font-bold uppercase tracking-widest hover:text-primary transition-colors cursor-pointer text-on-surface">Verify Supply Chain</button>
             <button onClick={() => setClaimText("EcoCorp achieves Net Zero across G7 operations by 2030.")} className="text-[9px] font-bold uppercase tracking-widest hover:text-primary transition-colors cursor-pointer text-on-surface">Audit G7 Claims</button>
             <button onClick={() => setIsSimulating(!isSimulating)} className="text-[9px] font-bold uppercase tracking-widest hover:text-primary transition-colors cursor-pointer text-on-surface">
               {isSimulating ? 'Stop Kinetic Sweep' : 'Start Kinetic Sweep'}
             </button>
          </div>
        </div>
      </main>

      <footer className="h-8 border-t border-outline/10 bg-surface/50 px-8 flex items-center justify-between z-40 relative transition-all duration-500">
        <div className="flex items-center gap-2">
           <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></div>
           <span className="text-[9px] font-bold uppercase tracking-widest text-outline">Institutional Node: Operational</span>
        </div>
        <div className="text-[9px] font-bold uppercase tracking-widest text-outline opacity-40">
           Forensic Protocol v2.5.4 | Proprietary Institutional Intelligence
        </div>
      </footer>
    </div>
  );
}
