import React from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Shield, Activity, RefreshCw, AlertTriangle } from 'lucide-react';

const AutomatedResponseMonitor = () => {
  // Recent interventions data
  const interventions = [
    {
      type: 'emergency_recovery',
      status: 'success',
      metrics: {
        coherence: { before: 0.82, after: 0.88 },
        response_time_ms: 150
      }
    },
    {
      type: 'load_shedding',
      status: 'success',
      metrics: {
        load: { before: 0.95, after: 0.60 },
        response_time_ms: 180
      }
    },
    {
      type: 'resource_scaling',
      status: 'success',
      metrics: {
        capacity: { before: '100%', after: '200%' },
        response_time_ms: 200
      }
    }
  ];

  const getStatusColor = (status) => {
    return status === 'success' ? 'text-green-500' : 'text-red-500';
  };

  const getInterventionIcon = (type) => {
    switch (type) {
      case 'emergency_recovery':
        return <Shield className="w-5 h-5 text-blue-500" />;
      case 'load_shedding':
        return <Activity className="w-5 h-5 text-yellow-500" />;
      case 'resource_scaling':
        return <RefreshCw className="w-5 h-5 text-purple-500" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-gray-500" />;
    }
  };

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <CardTitle>Automated Response Monitor</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* System Status */}
          <div className="grid grid-cols-3 gap-4">
            <div className="p-4 bg-green-50 rounded-lg">
              <div className="text-sm font-medium text-green-600">Active Responses</div>
              <div className="mt-1 text-2xl font-semibold text-green-700">3</div>
            </div>
            <div className="p-4 bg-blue-50 rounded-lg">
              <div className="text-sm font-medium text-blue-600">Avg Response Time</div>
              <div className="mt-1 text-2xl font-semibold text-blue-700">177ms</div>
            </div>
            <div className="p-4 bg-yellow-50 rounded-lg">
              <div className="text-sm font-medium text-yellow-600">Success Rate</div>
              <div className="mt-1 text-2xl font-semibold text-yellow-700">100%</div>
            </div>
          </div>

          {/* Recent Interventions */}
          <div className="space-y-4">
            <h3 className="text-lg font-medium">Recent Interventions</h3>
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
                        Response Time: {intervention.metrics.response_time_ms}ms
                      </div>
                    </div>
                  </div>
                  <div className={`text-sm font-medium ${getStatusColor(intervention.status)}`}>
                    {intervention.status.toUpperCase()}
                  </div>
                </div>
                <div className="mt-3 grid grid-cols-2 gap-4 text-sm">
                  {Object.entries(intervention.metrics).map(([key, value]) => {
                    if (key !== 'response_time_ms') {
                      return (
                        <div key={key} className="flex justify-between">
                          <span className="text-gray-500">{key}:</span>
                          <span>{typeof value.before === 'number' ? 
                            `${value.before.toFixed(2)} → ${value.after.toFixed(2)}` :
                            `${value.before} → ${value.after}`}
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
      </CardContent>
    </Card>
  );
};

export default AutomatedResponseMonitor;