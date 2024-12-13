import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, TrendingUp, TrendingDown, Activity } from 'lucide-react';

const TransitionMonitorDashboard = () => {
  // Sample transition data from our analysis
  const transitionVelocities = [
    { transition: 'extreme_load->moderate_load_stable', velocity: 0.5000, risk: 'high' },
    { transition: 'healthy_stable->moderate_load_stable', velocity: 0.2000, risk: 'high' },
    { transition: 'moderate_load_variable->high_load_stressed', velocity: 0.2000, risk: 'high' },
    { transition: 'high_load_stressed->extreme_load', velocity: 0.2000, risk: 'high' },
    { transition: 'moderate_load_stable->moderate_load_variable', velocity: 0.1500, risk: 'medium' }
  ];

  const stateMetrics = [
    { state: 'healthy_stable', coherence: 0.92, load: 0.20, stability: 0.95 },
    { state: 'moderate_load_stable', coherence: 0.88, load: 0.40, stability: 0.92 },
    { state: 'moderate_load_variable', coherence: 0.85, load: 0.55, stability: 0.87 },
    { state: 'high_load_stressed', coherence: 0.82, load: 0.75, stability: 0.81 },
    { state: 'extreme_load', coherence: 0.80, load: 0.95, stability: 0.75 }
  ];

  const getRiskColor = (risk) => {
    const colors = {
      high: '#ef4444',
      medium: '#f97316',
      low: '#22c55e'
    };
    return colors[risk] || '#6b7280';
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>State Transition Monitor</CardTitle>
          <Activity className="w-6 h-6 text-blue-500" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Transition Metrics Graph */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">State Transition Metrics</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={stateMetrics}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="state" 
                    angle={-45} 
                    textAnchor="end" 
                    height={80}
                    interval={0}
                  />
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
                    dataKey="load" 
                    stroke="#ef4444" 
                    name="Load"
                    strokeWidth={2}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="stability" 
                    stroke="#22c55e" 
                    name="Stability"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Transition Velocities */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Transition Velocities</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={transitionVelocities}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="transition" 
                    angle={-45} 
                    textAnchor="end" 
                    height={80}
                    interval={0}
                  />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar 
                    dataKey="velocity" 
                    name="Transition Velocity"
                    fill="#3b82f6"
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Critical Transitions */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Critical Transitions</h3>
            <div className="grid gap-4">
              {transitionVelocities.filter(t => t.risk === 'high').map((transition) => (
                <div 
                  key={transition.transition}
                  className="p-4 bg-white border rounded-lg border-l-4"
                  style={{ borderLeftColor: getRiskColor(transition.risk) }}
                >
                  <div className="flex justify-between items-center">
                    <div>
                      <div className="font-medium">{transition.transition}</div>
                      <div className="text-sm text-gray-500">
                        Risk Level: {transition.risk.toUpperCase()}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <div className="text-sm font-medium">
                        Velocity: {transition.velocity.toFixed(4)}
                      </div>
                      {transition.velocity > 0.3 ? (
                        <TrendingUp className="w-4 h-4 text-red-500" />
                      ) : (
                        <TrendingDown className="w-4 h-4 text-yellow-500" />
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default TransitionMonitorDashboard;