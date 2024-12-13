import React, { useState, useEffect } from 'react';
import { Circle, Zap, Atom } from 'lucide-react';

const PatternMergeVisualizer = ({ onMergeComplete }) => {
  const [mergeState, setMergeState] = useState('ready');
  const [coherence, setCoherence] = useState(1.0);
  const [quantumPhase, setQuantumPhase] = useState(0);

  useEffect(() => {
    if (mergeState === 'merging') {
      // Simulate quantum merge process
      let phase = 0;
      const interval = setInterval(() => {
        phase += Math.PI / 16;
        setQuantumPhase(phase);
        setCoherence(0.93 + Math.sin(phase) * 0.07);
        
        if (phase >= Math.PI * 2) {
          clearInterval(interval);
          setMergeState('complete');
          onMergeComplete?.();
        }
      }, 100);

      return () => clearInterval(interval);
    }
  }, [mergeState]);

  const startMerge = () => setMergeState('merging');

  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-xl">
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-bold text-white">Quantum Pattern Merge</h2>
        <div className="flex items-center space-x-2">
          <Zap className={`w-5 h-5 ${coherence > 0.95 ? 'text-green-400' : 'text-yellow-400'}`} />
          <span className="text-white">
            Coherence: {(coherence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      <div className="relative h-64 flex items-center justify-center">
        {/* Pattern Visualization */}
        <div className="relative">
          {/* Quantum Pattern */}
          <div className="absolute -left-16 top-0 transform -translate-y-1/2">
            <div className={`transition-all duration-500 ${
              mergeState === 'merging' ? 'translate-x-16' : ''
            }`}>
              <Circle 
                className="w-12 h-12 text-purple-500"
                style={{
                  opacity: Math.cos(quantumPhase) * 0.5 + 0.5
                }}
              />
            </div>
          </div>

          {/* Dream Pattern */}
          <div className="absolute -right-16 top-0 transform -translate-y-1/2">
            <div className={`transition-all duration-500 ${
              mergeState === 'merging' ? '-translate-x-16' : ''
            }`}>
              <Circle 
                className="w-12 h-12 text-blue-500"
                style={{
                  opacity: Math.sin(quantumPhase) * 0.5 + 0.5
                }}
              />
            </div>
          </div>

          {/* Merged Pattern */}
          {mergeState !== 'ready' && (
            <div className="absolute left-1/2 top-0 transform -translate-x-1/2 -translate-y-1/2">
              <Atom 
                className={`w-16 h-16 text-green-400 transition-all duration-1000 ${
                  mergeState === 'complete' ? 'opacity-100 scale-100' : 'opacity-0 scale-0'
                }`}
              />
            </div>
          )}

          {/* Quantum Field Visualization */}
          <div className="absolute inset-0 flex items-center justify-center">
            <div className={`w-32 h-32 rounded-full transition-all duration-500
              ${mergeState === 'merging' ? 'bg-purple-500' : 'bg-transparent'}
              opacity-20 animate-pulse`}
              style={{
                transform: `scale(${1 + Math.sin(quantumPhase) * 0.2})`,
                animationDuration: '2s'
              }}
            />
          </div>
        </div>
      </div>

      {/* Controls */}
      <div className="flex justify-center mt-4">
        <button
          onClick={startMerge}
          disabled={mergeState !== 'ready'}
          className={`px-6 py-2 rounded-lg font-medium transition-all
            ${mergeState === 'ready' 
              ? 'bg-blue-600 hover:bg-blue-700 text-white' 
              : 'bg-gray-700 text-gray-400'}`}
        >
          {mergeState === 'ready' ? 'Begin Quantum Merge' : 
           mergeState === 'merging' ? 'Merging...' : 
           'Merge Complete'}
        </button>
      </div>

      {/* Status Panel */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">State</h3>
          <p className="text-lg font-bold text-white capitalize">{mergeState}</p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Phase</h3>
          <p className="text-lg font-bold text-white">
            {((quantumPhase / (Math.PI * 2)) * 100).toFixed(0)}%
          </p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Stability</h3>
          <p className="text-lg font-bold text-white">
            {((1 - Math.abs(Math.sin(quantumPhase))) * 100).toFixed(0)}%
          </p>
        </div>
      </div>
    </div>
  );
};

export default PatternMergeVisualizer;