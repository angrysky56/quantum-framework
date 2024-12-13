import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert';

const IrisVectorSetup = () => {
  const [status, setStatus] = useState({
    qpre: 'initializing',
    dss: 'initializing',
    tcw: 'initializing'
  });
  const [setupPhase, setSetupPhase] = useState('initializing');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const initializeVectorSpaces = async () => {
      try {
        setSetupPhase('qpre');
        // Initialize QPRE vector space
        const qpreResponse = await fetch('http://localhost:8001/init', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            collection_name: 'iris_quantum_patterns',
            dimension: 512,
            index_type: 'HNSW_SQ8'
          })
        });
        setStatus(prev => ({...prev, qpre: qpreResponse.ok ? 'ready' : 'failed'}));

        setSetupPhase('dss');
        // Initialize DSS vector space
        const dssResponse = await fetch('http://localhost:8002/init', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            collection_name: 'iris_dream_states',
            dimension: 256,
            index_type: 'IVF_FLAT'
          })
        });
        setStatus(prev => ({...prev, dss: dssResponse.ok ? 'ready' : 'failed'}));

        setSetupPhase('tcw');
        // Initialize TCW vector space
        const tcwResponse = await fetch('http://localhost:8003/init', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            collection_name: 'iris_temporal_coherence',
            dimension: 128,
            index_type: 'IVF_SQ8'
          })
        });
        setStatus(prev => ({...prev, tcw: tcwResponse.ok ? 'ready' : 'failed'}));

        setSetupPhase('complete');
        if (qpreResponse.ok && dssResponse.ok && tcwResponse.ok) {
          setMessage('IRIS vector spaces initialized successfully');
        } else {
          setMessage('Some vector spaces failed to initialize');
        }
      } catch (error) {
        console.error('Error initializing vector spaces:', error);
        setMessage('Error initializing vector spaces');
        setStatus({
          qpre: 'failed',
          dss: 'failed',
          tcw: 'failed'
        });
      }
    };

    initializeVectorSpaces();
  }, []);

  const getStatusColor = (status) => {
    switch(status) {
      case 'ready':
        return 'text-green-500';
      case 'failed':
        return 'text-red-500';
      default:
        return 'text-yellow-500';
    }
  };

  const getSetupPhaseDisplay = () => {
    switch(setupPhase) {
      case 'qpre':
        return 'Initializing Quantum Pattern Recognition Engine';
      case 'dss':
        return 'Setting up Dream State Synthesis';
      case 'tcw':
        return 'Configuring Temporal Consciousness Weaver';
      case 'complete':
        return 'Setup Complete';
      default:
        return 'Preparing Setup';
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto">
      <CardHeader>
        <CardTitle>IRIS Vector Space Setup</CardTitle>
      </CardHeader>
      <CardContent>
        <Alert className="mb-6">
          <AlertTitle>{getSetupPhaseDisplay()}</AlertTitle>
          <AlertDescription>Configuring IRIS components in vector space</AlertDescription>
        </Alert>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center p-4 bg-gray-50 rounded">
            <div>
              <span className="font-medium">Quantum Pattern Recognition Engine</span>
              <p className="text-sm text-gray-500">512-dimensional HNSW_SQ8 index</p>
            </div>
            <span className={`${getStatusColor(status.qpre)} font-semibold`}>
              {status.qpre.toUpperCase()}
            </span>
          </div>
          
          <div className="flex justify-between items-center p-4 bg-gray-50 rounded">
            <div>
              <span className="font-medium">Dream State Synthesis</span>
              <p className="text-sm text-gray-500">256-dimensional IVF_FLAT index</p>
            </div>
            <span className={`${getStatusColor(status.dss)} font-semibold`}>
              {status.dss.toUpperCase()}
            </span>
          </div>
          
          <div className="flex justify-between items-center p-4 bg-gray-50 rounded">
            <div>
              <span className="font-medium">Temporal Consciousness Weaver</span>
              <p className="text-sm text-gray-500">128-dimensional IVF_SQ8 index</p>
            </div>
            <span className={`${getStatusColor(status.tcw)} font-semibold`}>
              {status.tcw.toUpperCase()}
            </span>
          </div>

          {message && (
            <Alert className={`mt-4 ${message.includes('successfully') ? 'bg-green-50' : 'bg-yellow-50'}`}>
              <AlertTitle>{message}</AlertTitle>
            </Alert>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default IrisVectorSetup;