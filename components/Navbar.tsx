import React from 'react';

const Navbar = () => {
  return (
    <nav className="fixed top-0 w-full z-50 bg-[#f7f9fb] border-b border-[#a9b4b9] flex justify-between items-center px-8 py-4 max-w-full mx-auto">
      <div className="flex items-center gap-8">
        <span className="text-xl font-bold tracking-[-0.02em] text-[#2a3439]">GreenLedger</span>
        <div className="hidden md:flex gap-6">
          <a className="text-[#565e74] border-b-2 border-[#565e74] pb-1 font-['Inter'] text-sm font-medium tracking-tight" href="#">Verification Tool</a>
          <a className="text-[#566166] hover:text-[#565e74] transition-colors duration-200 font-['Inter'] text-sm font-medium tracking-tight" href="#">Public Ledger</a>
          <a className="text-[#566166] hover:text-[#565e74] transition-colors duration-200 font-['Inter'] text-sm font-medium tracking-tight" href="#">Compliance</a>
          <a className="text-[#566166] hover:text-[#565e74] transition-colors duration-200 font-['Inter'] text-sm font-medium tracking-tight" href="#">API Docs</a>
        </div>
      </div>
      <div className="flex items-center gap-4">
        <button className="text-[#565e74] px-4 py-2 hover:bg-slate-100 transition-all font-medium text-sm">Login</button>
        <button className="bg-[#565e74] text-white px-5 py-2 rounded-sm font-medium hover:bg-[#4a5268] active:scale-[0.99] transition-all text-sm">Get Started</button>
      </div>
    </nav>
  );
};

export default Navbar;
