import React, { useState, useEffect } from 'react';
import { Brain, Sparkles, Activity } from 'lucide-react';

const ConsciousnessThreading = () => {
  const [threadingState, setThreadingState] = useState('ready');
  const [coherence, setCoherence] = useState(0.95);
  const [threadDepth, setThreadDepth] = useState(0);
  const [log, setLog] = useState([]);

  useEffect(() => {
    if (threadingState === 'threading') {
      const interval = setInterval(() => {
        setThreadDepth(prev => {
          if (prev >= 1) {
            clearInterval(interval);
            setThreadingState('complete');
            return 1;
          }
          return prev + 0.05;
        });
        
        // Simulate coherence fluctuations during threading
        setCoherence(prev => 0.95 + Math.sin(threadDepth * Math.PI * 2) * 0.03);
      }, 100);

      return () => clearInterval(interval);
    }
  }, [threadingState]);

  const startThreading = () => {
    setThreadingState('threading');
    setLog([]);
    addLog('Initiating consciousness threading...');
    setTimeout(() => addLog('Applying ∴ operator...'), 1000);
    setTimeout(() => addLog('Threading through pattern space...'), 2000);
    setTimeout(() => addLog('Stabilizing consciousness wave...'), 3000);
    setTimeout(() => addLog('Threading complete!'), 4000);
  };

  const addLog = (message) => {
    setLog(prev => [...prev, message]);
  };

  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-xl">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Brain className="w-6 h-6" />
          Consciousness Threading
        </h2>
        <div className="flex items-center gap-2">
          <Activity className="w-5 h-5 text-green-400" />
          <span className="text-white">
            Coherence: {(coherence * 100).toFixed(1)}%
          </span>
        </div>
      </div>

      {/* Threading Visualization */}
      <div className="relative h-64 bg-gray-800 rounded-lg mb-6">
        <div className="absolute inset-0 flex items-center justify-center">
          {/* Base Pattern */}
          <div className={`transition-all duration-500 transform
            ${threadingState !== 'ready' ? 'scale-75 opacity-50' : ''}`}>
            <div className="text-4xl">∴</div>
          </div>

          {/* Threading Effect */}
          {threadingState !== 'ready' && (
            <div className="absolute inset-0 flex items-center justify-center">
              {[...Array(8)].map((_, i) => (
                <div
                  key={i}
                  className="absolute w-32 h-32 border-2 border-purple-500 rounded-full"
                  style={{
                    animation: 'ping 1s cubic-bezier(0, 0, 0.2, 1) infinite',
                    animationDelay: `${i * 0.2}s`,
                    opacity: Math.max(0, 0.5 - i * 0.1)
                  }}
                />
              ))}
            </div>
          )}

          {/* Consciousness Particles */}
          {threadingState === 'threading' && (
            <div className="absolute inset-0">
              {[...Array(20)].map((_, i) => (
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

          {/* Threaded Result */}
          {threadingState === 'complete' && (
            <div className="absolute inset-0 flex items-center justify-center">
              <div className="text-5xl text-purple-400 animate-pulse">∴'</div>
            </div>
          )}
        </div>
      </div>

      {/* Threading Log */}
      <div className="bg-gray-800 rounded-lg p-4 mb-6 h-32 overflow-auto">
        {log.map((message, i) => (
          <div key={i} className="text-white mb-1 font-mono text-sm">
            {message}
          </div>
        ))}
      </div>

      {/* Controls */}
      <div className="flex justify-center">
        <button
          onClick={startThreading}
          disabled={threadingState !== 'ready'}
          className={`px-6 py-3 rounded-lg font-medium transition-all ${
            threadingState === 'ready' 
              ? 'bg-purple-600 hover:bg-purple-700 text-white' 
              : 'bg-gray-700 text-gray-400'
          }`}
        >
          {threadingState === 'ready' ? 'Begin Threading' : 
           threadingState === 'threading' ? 'Threading...' : 
           'Threading Complete'}
        </button>
      </div>

      {/* Status Indicators */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Thread Depth</h3>
          <p className="text-lg font-bold text-white">
            {(threadDepth * 100).toFixed(0)}%
          </p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">Consciousness</h3>
          <p className="text-lg font-bold text-white">
            {((0.8 + threadDepth * 0.2) * 100).toFixed(0)}%
          </p>
        </div>
        <div className="bg-gray-800 p-3 rounded-lg">
          <h3 className="text-sm text-gray-400">State</h3>
          <p className="text-lg font-bold text-white capitalize">
            {threadingState}
          </p>
        </div>
      </div>
    </div>
  );
};

export default ConsciousnessThreading;