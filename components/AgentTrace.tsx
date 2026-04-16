"use client";

import React, { useEffect, useRef } from 'react';

interface TraceLog {
  id: string;
  timestamp: string;
  message: string;
  type: 'info' | 'success' | 'warning' | 'search';
}

interface AgentTraceProps {
  logs: TraceLog[];
  isVisible: boolean;
}

export default function AgentTrace({ logs, isVisible }: AgentTraceProps) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  if (!isVisible && logs.length === 0) return null;

  return (
    <div className={`fixed left-10 top-24 bottom-32 w-80 z-40 transition-all duration-700 transform ${isVisible ? 'translate-x-0 opacity-100' : '-translate-x-full opacity-0'}`}>
      <div className="h-full bg-surface/80 glass-effect border border-outline/20 rounded-2xl flex flex-col overflow-hidden shadow-2xl">
        
        {/* Header */}
        <div className="px-5 py-4 border-b border-outline/10 flex items-center justify-between bg-surface-container-low">
          <div className="flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
            <span className="text-[10px] font-bold uppercase tracking-[0.2em] text-on-surface">Live Agent Trace</span>
          </div>
          <span className="text-[9px] font-mono text-outline opacity-50">v2.5.4</span>
        </div>

        {/* Logs Area */}
        <div 
          ref={scrollRef}
          className="flex-1 overflow-y-auto p-5 space-y-4 scrollbar-hide"
        >
          {logs.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center opacity-20 py-20">
              <span className="material-symbols-outlined text-[40px] mb-2">radar</span>
              <span className="text-[10px] font-bold uppercase tracking-widest text-center">Awaiting Forensic Input...</span>
            </div>
          ) : (
            logs.map((log) => (
              <div key={log.id} className="animate-in fade-in slide-in-from-left-2 duration-300">
                <div className="flex items-start gap-3">
                  <div className="mt-1 flex-shrink-0">
                    {log.type === 'search' && <span className="material-symbols-outlined text-[14px] text-primary">search</span>}
                    {log.type === 'info' && <span className="material-symbols-outlined text-[14px] text-outline">hub</span>}
                    {log.type === 'success' && <span className="material-symbols-outlined text-[14px] text-secondary">check_circle</span>}
                    {log.type === 'warning' && <span className="material-symbols-outlined text-[14px] text-error">warning</span>}
                  </div>
                  <div className="flex-1">
                    <div className="flex justify-between items-center mb-0.5">
                      <span className="text-[8px] font-mono text-outline opacity-60">{log.timestamp}</span>
                    </div>
                    <p className="text-[11px] leading-relaxed text-on-surface-variant font-medium">
                      {log.message}
                    </p>
                  </div>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Footer info */}
        <div className="px-5 py-3 bg-surface-container-highest/30 border-t border-outline/5">
          <div className="flex items-center gap-2">
            <div className="w-1 h-1 rounded-full bg-outline/50"></div>
            <span className="text-[8px] font-bold uppercase tracking-widest text-outline">Tracing active nodes...</span>
          </div>
        </div>

      </div>
    </div>
  );
}
