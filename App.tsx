import React, { useState, useEffect } from 'react';

const OLD_URL = "www.thepoweraddicts.ch";
const NEW_URL = "https://www.kmupower.com";
const REDIRECT_SECONDS = 10;

const App: React.FC = () => {
  const [countdown, setCountdown] = useState<number>(REDIRECT_SECONDS);

  useEffect(() => {
    if (countdown <= 0) {
      window.location.href = NEW_URL;
      return;
    }

    const timer = setInterval(() => {
      setCountdown((prevCountdown) => prevCountdown - 1);
    }, 1000);

    return () => clearInterval(timer);
  }, [countdown]);

  const handleRedirectClick = () => {
    window.location.href = NEW_URL;
  };

  const progressPercentage = ((REDIRECT_SECONDS - countdown) / REDIRECT_SECONDS) * 100;

  return (
    <div className="min-h-screen bg-slate-900 text-white flex items-center justify-center p-4 selection:bg-cyan-500 selection:text-slate-900">
      <div className="w-full max-w-2xl bg-slate-800/60 backdrop-blur-sm border border-slate-700 rounded-2xl shadow-2xl shadow-cyan-500/10 overflow-hidden transform transition-all hover:scale-[1.01] duration-500">
        <div className="p-8 md:p-12 text-center">
          <div className="flex justify-center mb-6">
            <svg className="w-16 h-16 text-cyan-400" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 4.5 21 12m0 0-7.5 7.5M21 12H3" />
            </svg>
          </div>
          <h1 className="text-3xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-cyan-400 mb-4">
            Wir sind umgezogen!
          </h1>
          <p className="text-slate-300 text-lg md:text-xl mb-2">
            <strong className="text-white font-semibold">{OLD_URL}</strong> hat sich weiterentwickelt und heisst jetzt
          </p>
          <p className="text-4xl md:text-6xl font-bold text-cyan-400 mb-8 tracking-tight">
            KMU Power
          </p>
          
          <p className="text-slate-400 mb-8 max-w-lg mx-auto">
            Vielen Dank für Ihre Treue! Um Ihnen einen noch besseren Service zu bieten, haben wir uns umbenannt und unsere Webseite erneuert. Sie werden in Kürze automatisch weitergeleitet.
          </p>
          
          <div className="mb-8">
            <button
              onClick={handleRedirectClick}
              className="w-full md:w-auto bg-cyan-500 hover:bg-cyan-400 text-slate-900 font-bold py-3 px-8 rounded-lg text-lg transform hover:scale-105 transition-transform duration-300 focus:outline-none focus:ring-4 focus:ring-cyan-300 focus:ring-opacity-50"
            >
              Jetzt zu kmupower.com
            </button>
          </div>

          <div className="text-slate-400">
            <p className="mb-3">Automatische Weiterleitung in...</p>
            <p className="text-6xl font-bold text-white mb-4">{countdown}</p>
            <div className="w-full bg-slate-700 rounded-full h-2.5">
              <div
                className="bg-gradient-to-r from-cyan-500 to-blue-500 h-2.5 rounded-full transition-all duration-1000 ease-linear"
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
          </div>
        </div>
        <div className="bg-slate-900/50 px-8 py-4 text-center text-sm text-slate-500">
          <p>Sie werden von <span className="font-mono">{OLD_URL}</span> nach <span className="font-mono">{NEW_URL}</span> weitergeleitet.</p>
        </div>
      </div>
    </div>
  );
};

export default App;
