// apps/web/components/TimeBridge/index.tsx
import React from 'react';

// Interface for TimelineEvent as defined in the roadmap
interface TimelineEvent {
  date: Date;
  type: 'demand_spike' | 'production_cutoff' | 'event';
  intensity: number;
  feasibility: 'green' | 'yellow' | 'red';
  evidence: string[];
}

interface TimeBridgeProps {
  events: TimelineEvent[];
}

const TimeBridge: React.FC<TimeBridgeProps> = ({ events }) => {
  return (
    <div className="time-bridge-container p-4 border rounded-lg shadow-md">
      <h2 className="text-xl font-semibold mb-4">TimeBridge Timeline</h2>
      {events.length === 0 ? (
        <p className="text-gray-500">No events to display.</p>
      ) : (
        <ul>
          {events.map((event, index) => (
            <li key={index} className="mb-2 p-2 border-b last:border-b-0">
              <div className="flex justify-between items-center">
                <span className="font-medium">{event.date.toDateString()}</span>
                <span className={`px-2 py-1 rounded-full text-xs font-bold ${
                  event.feasibility === 'green' ? 'bg-green-200 text-green-800' :
                  event.feasibility === 'yellow' ? 'bg-yellow-200 text-yellow-800' :
                  'bg-red-200 text-red-800'
                }`}>
                  {event.feasibility.toUpperCase()}
                </span>
              </div>
              <p className="text-sm text-gray-700">Type: {event.type}</p>
              <p className="text-sm text-gray-700">Intensity: {event.intensity}</p>
              {event.evidence && event.evidence.length > 0 && (
                <p className="text-xs text-gray-600">Evidence: {event.evidence.join(', ')}</p>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default TimeBridge;
