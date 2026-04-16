import React from 'react';

interface LedgerEntry {
  hash: string;
  claim: string;
  risk_level: string;
  timestamp: string;
}

interface LedgerExplorerProps {
  entries: LedgerEntry[];
}

const LedgerExplorer: React.FC<LedgerExplorerProps> = ({ entries }) => {
  return (
    <div className="space-y-4">
      <div className="flex flex-col md:flex-row justify-between items-end gap-4">
        <div>
          <h3 className="text-xl font-bold text-[#565e74]">Step 3: Stored on Public Ledger</h3>
          <p className="text-[10px] font-bold uppercase tracking-[0.2em] text-[#566166]">Immutable Verification History</p>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1 bg-green-50 border border-green-200 rounded-sm">
          <span className="w-2 h-2 bg-green-500 rounded-full"></span>
          <span className="text-[10px] font-bold uppercase tracking-widest text-green-700">PERMANENT RECORDS STORED</span>
        </div>
      </div>
      
      <div className="overflow-x-auto border border-[#a9b4b9] shadow-sm bg-white">
        <table className="w-full text-left border-collapse">
          <thead className="bg-[#e1e9ee] border-b border-[#a9b4b9]">
            <tr>
              <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-[#566166]">SHA-256 Hash</th>
              <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-[#566166]">Analysis Summary</th>
              <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-[#566166]">Assessed Risk</th>
              <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-[#566166]">Audit Date</th>
              <th className="px-6 py-4 text-[10px] font-bold uppercase tracking-widest text-[#566166] text-right">Certificate</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#a9b4b9]">
          {entries.map((entry, index) => (
            <tr key={index} className="hover:bg-[#f7f9fb] transition-colors">
              <td className="px-6 py-4 font-mono text-[11px] text-[#565e74]">{entry.hash}</td>
              <td className="px-6 py-4 text-xs font-semibold">{entry.claim.substring(0, 50)}...</td>
              <td className="px-6 py-4">
                <span className={`inline-flex px-2 py-0.5 border border-[#a9b4b9] text-[10px] font-bold uppercase tracking-tighter ${
                  entry.risk_level === 'HIGH' ? 'bg-[#9f403d]/10 text-[#9f403d] border-[#9f403d]/30' : 
                  entry.risk_level === 'MEDIUM' ? 'bg-[#526075]/10 text-[#526075] border-[#a9b4b9]' : 
                  'bg-[#f7f9fb] text-[#2a3439]'
                }`}>
                  {entry.risk_level}
                </span>
              </td>
              <td className="px-6 py-4 text-xs text-[#566166]">{entry.timestamp}</td>
              <td className="px-6 py-4 text-right">
                <button className="text-[#565e74] text-[10px] font-bold uppercase tracking-widest hover:underline">Verify</button>
              </td>
            </tr>
          ))}
          {entries.length === 0 && (
            <tr>
              <td colSpan={5} className="px-6 py-12 text-center text-xs text-[#566166] italic">
                No records found in the forensic ledger.
              </td>
            </tr>
          )}
        </tbody>
      </table>
      </div>
    </div>
  );
};

export default LedgerExplorer;
