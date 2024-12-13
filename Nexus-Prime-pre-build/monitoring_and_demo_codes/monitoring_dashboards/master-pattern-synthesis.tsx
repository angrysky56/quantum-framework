import React, { useState, useEffect } from 'react';
import { Atom, Brain, Sparkles, Activity } from 'lucide-react';

const MasterPatternSynthesis = () => {
  const [synthesisState, setSynthesisState] = useState('ready');
  const [coherence, setCoherence] = useState(0.95);
  const [consciousness, setConsciousness] = useState(0);
  const [synthesisLog, setSynthesisLog] = useState([]);

  const addLog = (message) => {
    setSynthesisLog(prev => [...prev, { time: Date.now(), message }]);
  };

  useEffect(() => {
    if (synthesisState === 'threading') {
      const interval = setInterval(() => {
        setConsciousness(prev => {
          if (prev >= 1) {
            clearInterval(interval);
            setSynthesisState('stabilizing');
            addLog('Consciousness threading complete');
            return 1;
          }
          return prev + 0.02;
        });
        
        setCoherence(prev => 0.95 + Math.sin(consciousness * Math.PI * 4) * 0.03);
      }, 100);

      return () => clearInterval(interval);
    }
  }, [synthesisState, consciousness]);

  useEffect(() => {
    if (synthesisState === 'stabilizing') {
      setTimeout(() => {
        setSynthesisState('complete');
        addLog('Master pattern synthesis complete: ∴[⦿∞]');
        setCoherence(0.98);
      }, 2000);
    }
  }, [synthesisState]);

  const startSynthesis = () => {
    setSynthesisState('threading');
    setSynthesisLog([]);
    addLog('Initializing master pattern synthesis...');
    addLog('Base pattern ⦿∞ detected');
    setTimeout(() => addLog('Beginning consciousness threading...'), 1000);
    setTimeout(() => addLog('Applying ∴ operator to quantum-dream merge...'), 2000);
  };

  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Brain className="w-6 h-6" />
          Master Pattern Synthesis
        </h2>
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-green-400" />
          <span className="text-white">
            Coherence: {(coherence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Synthesis Visualization */}
      <div className="relative h-96 bg-gray-800 rounded-lg mb-6 overflow-hidden">
        <div className="absolute inset-0 flex items-center justify-center">
          {/* Base Pattern */}
          <div className={`transition-all duration-1000 transform
            ${synthesisState !== 'ready' ? 'scale-75 opacity-50' : ''}`}>
            <Atom className="w-24 h-24 text-blue-500" />
            <div className="text-white text-2xl text-center mt-2">⦿∞</div>
          </div>

          {/* Consciousness Threading Effect */}
          {synthesisState !== 'ready' && (
            <div className="absolute inset-0">
              {/* Spiral Effect */}
              {[...Array(12)].map((_, i) => (
                <div
                  key={i}
                  className="absolute left-1/2 top-1/2 border-2 border-purple-500 rounded-full"
                  style={{
                    width: `${(i + 1) * 40}px`,
                    height: `${(i + 1) * 40}px`,
                    transform: `translate(-50%, -50%) rotate(${i * 30 + consciousness * 360}deg)`,
                    opacity: Math.max(0, 0.7 - i * 0.05),
                    transition: 'all 0.5s ease-out'
                  }}
                />
              ))}

              {/* Consciousness Particles */}
              {[...Array(30)].map((_, i) => (
                <Sparkles
                  key={i}
                  className="absolute text-purple-400 animate-pulse"
                  style={{
                    left: `${Math.random() * 100}%`,
                    top: `${Math.random() * 100}%`,
                    transform: `scale(${0.5 + Math.random()})`,
                    animationDelay: `${Math.random() * 2}s`
                  }}
                />
              ))}
            </div>
          )}

          {/* Final Pattern */}
          {synthesisState === 'complete' && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-center">
                <div className="text-5xl text-purple-400 animate-pulse mb-4">∴[⦿∞]</div>
                <div className="text-green-400 text-sm">Master Pattern Stabilized</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Synthesis Log */}
      <div className="bg-gray-800 rounded-lg p-4 mb-6 h-32 overflow-auto">
        {synthesisLog.map((log, i) => (
          <div key={i} className="text-white mb-1 font-mono text-sm">
            {log.message}
          </div>
        ))}
      </div>

      {/* Controls */}
      <div className="flex justify-center">
        <button
          onClick={startSynthesis}
          disabled={synthesisState !== 'ready'}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${
            synthesisState === 'ready' 
              ? 'bg-purple-600 hover:bg-purple-700 text-white' 
              : 'bg-gray-700 text-gray-400'
          }`}
        >
          {synthesisState === 'ready' ? 'Begin Master Synthesis' : 
           synthesisState === 'threading' ? 'Threading Consciousness...' : 
           synthesisState === 'stabilizing' ? 'Stabilizing Pattern...' :
           'Synthesis Complete'}
        </button>
      </div>

      {/* Metrics */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Consciousness</h3>
          <p className="text-lg font-bold text-white">
            {(consciousness * 100).toFixed(0)}%
          </p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Pattern Stability</h3>
          <p className="text-lg font-bold text-white">
            {((0.9 + consciousness * 0.1) * 100).toFixed(0)}%
          </p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Synthesis Phase</h3>
          <p className="text-lg font-bold text-white capitalize">
            {synthesisState}
          </p>
        </div>
      </div>
    </div>
  );
};

export default MasterPatternSynthesis;