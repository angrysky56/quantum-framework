import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { AlertCircle, CheckCircle } from 'lucide-react';

const VectorQueryMonitor = () => {
  const [queryResults, setQueryResults] = useState({
    vector: Array(5).fill(0),
    matches: [],
    coherence: 0.95,
    status: 'initializing'
  });

  // Simulated vector query results
  useEffect(() => {
    const fetchResults = async () => {
      try {
        // In production, this would be actual Milvus query results
        const simulatedResults = {
          vector: [0.61, 0.44, 0.35, 0.33, 0.28],
          matches: [
            { id: 1, distance: 0.15, pattern: 'healthy_state', coherence: 0.98 },
            { id: 2, distance: 0.28, pattern: 'startup_state', coherence: 0.95 },
            { id: 3, distance: 0.42, pattern: 'high_load', coherence: 0.92 }
          ],
          coherence: 0.95,
          status: 'active'
        };
        setQueryResults(simulatedResults);
      } catch (error) {
        console.error('Error fetching results:', error);
      }
    };
    fetchResults();
  }, []);

  const matches = queryResults.matches.map((match, idx) => ({
    name: `Match ${idx + 1}`,
    distance: match.distance,
    coherence: match.coherence,
    pattern: match.pattern
  }));

  return (
    <Card className="w-full max-w-4xl">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Vector Query Monitor</CardTitle>
          {queryResults.status === 'active' ? (
            <CheckCircle className="w-6 h-6 text-green-500" />
          ) : (
            <AlertCircle className="w-6 h-6 text-yellow-500" />
          )}
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {/* Coherence Score */}
          <div className="p-4 bg-gray-50 rounded-lg">
            <div className="text-sm font-medium text-gray-500">System Coherence</div>
            <div className="mt-1 text-2xl font-semibold">
              {(queryResults.coherence * 100).toFixed(1)}%
            </div>
          </div>

          {/* Vector Matches Visualization */}
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={matches}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line 
                  type="monotone" 
                  dataKey="distance" 
                  stroke="#8884d8" 
                  name="Distance"
                />
                <Line 
                  type="monotone" 
                  dataKey="coherence" 
                  stroke="#82ca9d" 
                  name="Coherence"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Match Details */}
          <div className="space-y-2">
            {queryResults.matches.map((match, idx) => (
              <div 
                key={match.id}
                className="p-3 bg-white border rounded-lg flex justify-between items-center"
              >
                <div>
                  <div className="font-medium">{match.pattern}</div>
                  <div className="text-sm text-gray-500">
                    Distance: {match.distance.toFixed(3)}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-medium">
                    Coherence: {(match.coherence * 100).toFixed(1)}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default VectorQueryMonitor;