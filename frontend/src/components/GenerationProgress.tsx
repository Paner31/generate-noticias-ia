import React, { useEffect, useState } from 'react';
import type { JobStatusResponse, GeneratedNote } from '../types';
import { generateAPI } from '../services/api';

interface GenerationProgressProps {
  jobId: string;
  onComplete: (notes: GeneratedNote[]) => void;
}

export const GenerationProgress: React.FC<GenerationProgressProps> = ({
  jobId,
  onComplete,
}) => {
  const [status, setStatus] = useState<JobStatusResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const pollStatus = async () => {
      try {
        const response = await generateAPI.getJobStatus(jobId);
        setStatus(response);

        if (response.status === 'completed') {
          onComplete(response.notes);
        } else if (response.status === 'failed') {
          setError(response.error || 'Generation failed');
        }
      } catch (err: any) {
        setError(err.message || 'Failed to fetch status');
      }
    };

    // Poll every 2 seconds
    const interval = setInterval(pollStatus, 2000);
    pollStatus(); // Initial call

    return () => clearInterval(interval);
  }, [jobId, onComplete]);

  if (error) {
    return (
      <div className="bg-red-50 border border-red-300 rounded-md p-4">
        <h3 className="font-semibold text-red-900 mb-2">Error</h3>
        <p className="text-red-700">{error}</p>
      </div>
    );
  }

  if (!status) {
    return (
      <div className="bg-blue-50 border border-blue-300 rounded-md p-4">
        <p className="text-blue-700">Loading status...</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h3 className="text-xl font-bold mb-4">Generating Notes...</h3>

      <div className="mb-4">
        <div className="flex justify-between text-sm mb-1">
          <span className="font-medium">Progress</span>
          <span className="text-gray-600">{status.progress}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div
            className="bg-blue-600 h-3 rounded-full transition-all duration-300"
            style={{ width: `${status.progress}%` }}
          />
        </div>
      </div>

      <div className="text-sm text-gray-600 mb-4">
        Status: <span className="font-medium capitalize">{status.status}</span>
      </div>

      {status.notes.length > 0 && (
        <div>
          <h4 className="font-semibold mb-2">Generated Notes ({status.notes.length})</h4>
          <div className="space-y-2">
            {status.notes.map((note, index) => (
              <div key={note.note_id} className="p-3 bg-green-50 border border-green-200 rounded-md">
                <div className="font-medium text-green-900">Note {index + 1}</div>
                <div className="text-sm text-green-700">{note.sources.length} source(s)</div>
                <div className="text-xs text-green-600">Tokens: {note.tokens_used}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
