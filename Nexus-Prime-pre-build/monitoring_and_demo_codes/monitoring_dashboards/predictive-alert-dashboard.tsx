import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, Bell, TrendingUp, Activity } from 'lucide-react';

const PredictiveAlertDashboard = () => {
  const [alertHistory] = useState([
    {
      timestep: 3,
      type: 'stability_degradation',
      severity: 'high',
      metrics: { stability: 0.87, coherence: 0.87, load: 0.5 }
    },
    {
      timestep: 4,
      type: 'load_spike',
      severity: 'high',
      metrics: { stability: 0.81, coherence: 0.84, load: 0.7 }
    },
    {
      timestep: 4,
      type: 'coherence_breakdown',
      severity: 'critical',
      metrics: { stability: 0.81, coherence: 0.84, load: 0.7 }
    }
  ]);

  const metricHistory = [
    { timestep: 1, stability: 0.95, coherence: 0.92, load: 0.2 },
    { timestep: 2, stability: 0.92, coherence: 0.90, load: 0.3 },
    { timestep: 3, stability: 0.87, coherence: 0.87, load: 0.5 },
    { timestep: 4, stability: 0.81, coherence: 0.84, load: 0.7 },
    { timestep: 5, stability: 0.75, coherence: 0.82, load: 0.9 }
  ];

  const getSeverityColor = (severity) => {
    const colors = {
      critical: 'text-red-500 bg-red-50',
      high: 'text-orange-500 bg-orange-50',
      medium: 'text-yellow-500 bg-yellow-50',
      low: 'text-green-500 bg-green-50'
    };
    return colors[severity] || 'text-gray-500 bg-gray-50';
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Predictive Alert System</CardTitle>
          <Bell className="w-6 h-6 text-blue-500" />
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Metric Trends */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">System Metrics</h3>
            <div className="h-64">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={metricHistory}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="timestep" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="stability" 
                    stroke="#22c55e" 
                    name="Stability"
                    strokeWidth={2}
                  />
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
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Active Alerts */}
          <div className="space-y-2">
            <h3 className="text-lg font-medium">Alert History</h3>
            <div className="space-y-3">
              {alertHistory.map((alert, index) => (
                <div 
                  key={`${alert.timestep}-${index}`}
                  className={`p-4 rounded-lg border ${getSeverityColor(alert.severity)}`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-medium">
                        {alert.type.split('_').map(word => 
                          word.charAt(0).toUpperCase() + word.slice(1)
                        ).join(' ')}
                      </div>
                      <div className="text-sm text-gray-500">
                        Timestep: {alert.timestep}
                      </div>
                    </div>
                    <div className="flex items-center space-x-2">
                      <AlertCircle className="w-5 h-5" />
                      <span className="text-sm font-medium">
                        {alert.severity.toUpperCase()}
                      </span>
                    </div>
                  </div>
                  <div className="mt-2 text-sm">
                    <div>Stability: {alert.metrics.stability.toFixed(2)}</div>
                    <div>Coherence: {alert.metrics.coherence.toFixed(2)}</div>
                    <div>Load: {alert.metrics.load.toFixed(2)}</div>
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

export default PredictiveAlertDashboard;