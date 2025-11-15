import React from 'react';
import type { GeneratedNote } from '../types';

interface GeneratedNotesProps {
  notes: GeneratedNote[];
  onReset: () => void;
}

export const GeneratedNotes: React.FC<GeneratedNotesProps> = ({ notes, onReset }) => {
  const copyToClipboard = (content: string) => {
    navigator.clipboard.writeText(content);
    alert('Note copied to clipboard!');
  };

  const totalTokens = notes.reduce((sum, note) => sum + note.tokens_used, 0);

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Generated Notes ({notes.length})</h2>
        <button
          onClick={onReset}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 font-medium"
        >
          New Search
        </button>
      </div>

      <div className="mb-4 p-3 bg-gray-50 rounded-md">
        <div className="text-sm text-gray-700">
          Total tokens used: <span className="font-semibold">{totalTokens.toLocaleString()}</span>
        </div>
      </div>

      <div className="space-y-6">
        {notes.map((note, index) => (
          <div key={note.note_id} className="border border-gray-200 rounded-lg p-6">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-semibold">Note {index + 1}</h3>
              <button
                onClick={() => copyToClipboard(note.content)}
                className="bg-gray-600 text-white px-3 py-1 rounded-md hover:bg-gray-700 text-sm"
              >
                Copy
              </button>
            </div>

            <div className="prose max-w-none mb-4">
              <div className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                {note.content}
              </div>
            </div>

            <div className="border-t pt-4 mt-4">
              <div className="text-sm text-gray-600 mb-2">
                <span className="font-medium">Sources ({note.sources.length}):</span>
              </div>
              <ul className="space-y-1">
                {note.sources.map((source, idx) => (
                  <li key={idx} className="text-sm">
                    <a
                      href={source}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-blue-600 hover:underline"
                    >
                      {source}
                    </a>
                  </li>
                ))}
              </ul>
            </div>

            <div className="border-t pt-3 mt-3 flex justify-between text-xs text-gray-500">
              <span>Model: {note.model}</span>
              <span>Tokens: {note.tokens_used.toLocaleString()}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
