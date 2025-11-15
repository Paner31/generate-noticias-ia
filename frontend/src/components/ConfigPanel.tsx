import React, { useState } from 'react';

interface ConfigPanelProps {
  onConfigChange: (config: { customPrompt: string; maxTokens: number; model: string }) => void;
}

export const ConfigPanel: React.FC<ConfigPanelProps> = ({ onConfigChange }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [customPrompt, setCustomPrompt] = useState('');
  const [maxTokens, setMaxTokens] = useState(8000);
  const [model, setModel] = useState('z-ai/glm-4.6');

  const handleApply = () => {
    onConfigChange({ customPrompt, maxTokens, model });
    setIsOpen(false);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Generation Settings</h3>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-blue-600 hover:text-blue-800 font-medium"
        >
          {isOpen ? 'Hide' : 'Configure'}
        </button>
      </div>

      {isOpen && (
        <div className="mt-4 space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Custom Prompt (Optional)
            </label>
            <textarea
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500"
              rows={4}
              placeholder="Add custom instructions for note generation..."
            />
            <p className="text-xs text-gray-500 mt-1">
              Example: "Focus on financial implications" or "Write in a conversational tone"
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Tokens per Note
            </label>
            <input
              type="number"
              value={maxTokens}
              onChange={(e) => setMaxTokens(parseInt(e.target.value))}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
              min="1000"
              max="16000"
            />
            <p className="text-xs text-gray-500 mt-1">
              Default: 8000 tokens (~6000 words)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Model
            </label>
            <select
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md"
            >
              <option value="z-ai/glm-4.6">GLM-4.6 (Recommended - Very Affordable)</option>
              <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
              <option value="anthropic/claude-3-opus">Claude 3 Opus</option>
              <option value="openai/gpt-4-turbo">GPT-4 Turbo</option>
              <option value="openai/gpt-4o">GPT-4o</option>
              <option value="google/gemini-pro-1.5">Gemini Pro 1.5</option>
            </select>
          </div>

          <button
            onClick={handleApply}
            className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 font-medium"
          >
            Apply Settings
          </button>
        </div>
      )}
    </div>
  );
};
