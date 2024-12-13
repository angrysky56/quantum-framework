import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Zap, Shield, Activity, RefreshCw, CheckCircle } from 'lucide-react';

const AutomatedInterventionMonitor = () => {
  // Sample intervention data
  const interventions = [
    {
      type: 'automated_coherence_optimization',
      status: 'active',
      metrics: {
        coherence_change: 0.05,
        execution_time_ms: 120,
        confidence: 0.9
      }
    },
    {
      type: 'automated_resource_scaling',
      status: 'active',
      metrics: {
        load_change: -0.15,
        execution_time_ms: 180,
        confidence: 0.95
      }
    }
  ];

  const metricHistory = [
    { time: '00:00', coherence: 0.85, stability: 0.88, load: 0.70 },
    { time: '00:01', coherence: 0.87, stability: 0.89, load: 0.65 },
    { time: '00:02', coherence: 0.90, stability: 0.91, load: 0.60 },
    { time: '00:03', coherence: 0.92, stability: 0.92, load: 0.55 }
  ];

  const getInterventionIcon = (type) => {
    switch (type) {
      case 'automated_coherence_optimization':
        return <Shield className="w-5 h-5 text-blue-500" />;
      case 'automated_resource_scaling':
        return <RefreshCw className="w-5 h-5 text-green-500" />;
      case 'automated_stability_enhancement':
        return <Activity className="w-5 h-5 text-yellow-500" />;
      default:
        return <Zap className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Automated Intervention Monitor</CardTitle>
          <Zap className="w-6 h-6 text-blue-500" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Metrics Chart */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Metric Trends</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={metricHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="time" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="coherence" 
                    stroke="#3b82f6" 
                    name="Coherence"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="stability" 
                    stroke="#22c55e" 
                    name="Stability"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="load" 
                    stroke="#ef4444" 
                    name="Load"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Active Interventions */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Active Interventions</h3>
            <div className="grid gap-4">
              {interventions.map((intervention, index) => (
                <div 
                  key={index}
                  className="p-4 bg-white border rounded-lg shadow-sm"
                >
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      {getInterventionIcon(intervention.type)}
                      <div>
                        <div className="font-medium">
                          {intervention.type.split('_').map(word => 
                            word.charAt(0).toUpperCase() + word.slice(1)
                          ).join(' ')}
                        </div>
                        <div className="text-sm text-gray-500">
                          Execution Time: {intervention.metrics.execution_time_ms}ms
                        </div>
                      </div>
                    </div>
                    <div className="text-sm font-medium text-green-500">
                      ACTIVE
                    </div>
                  </div>
                  <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                    {Object.entries(intervention.metrics).map(([key, value]) => {
                      if (key !== 'execution_time_ms') {
                        return (
                          <div key={key} className="flex justify-between">
                            <span className="text-gray-500">
                              {key.split('_').map(word => 
                                word.charAt(0).toUpperCase() + word.slice(1)
                              ).join(' ')}:
                            </span>
                            <span>
                              {typeof value === 'number' 
                                ? (key.includes('change') 
                                  ? (value > 0 ? '+' : '') + (value * 100).toFixed(1) + '%' 
                                  : value.toFixed(2))
                                : value}
                            </span>
                          </div>
                        );
                      }
                      return null;
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* System Status */}
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm font-medium text-blue-600">Active Interventions</div>
              <div className="mt-1 text-2xl font-semibold text-blue-700">2</div>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-sm font-medium text-green-600">Success Rate</div>
              <div className="mt-1 text-2xl font-semibold text-green-700">95%</div>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <div className="text-sm font-medium text-purple-600">Avg Response Time</div>
              <div className="mt-1 text-2xl font-semibold text-purple-700">150ms</div>
            </div>
          </div>

          {/* Predictive Insights */}
          <div className="p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg">
            <h3 className="text-lg font-medium mb-2">AI Native Insights</h3>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span>Vector coherence maintaining optimal levels through predictive scaling</span>
              </div>
              <div className="flex items-center space-x-2">
                <Activity className="w-5 h-5 text-blue-500" />
                <span>Quantum tunnel stability enhanced by automated pattern recognition</span>
              </div>
              <div className="flex items-center space-x-2">
                <Shield className="w-5 h-5 text-purple-500" />
                <span>Fractal optimization patterns emerging in resource distribution</span>
              </div>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default AutomatedInterventionMonitor;