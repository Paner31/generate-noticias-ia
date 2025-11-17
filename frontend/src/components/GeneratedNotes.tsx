import React, { useState } from 'react';
import { marked } from 'marked';
import type { GeneratedNote } from '../types';

interface GeneratedNotesProps {
  notes: GeneratedNote[];
  onReset: () => void;
}

type TabType = 'note' | 'image';

export const GeneratedNotes: React.FC<GeneratedNotesProps> = ({ notes, onReset }) => {
  console.log('[GeneratedNotes] Received notes:', notes);
  console.log('[GeneratedNotes] Notes count:', notes.length);

  if (notes.length > 0) {
    console.log('[GeneratedNotes] First note details:', {
      note_id: notes[0].note_id,
      has_content: !!notes[0].content,
      content_length: notes[0].content?.length,
      has_image_prompt: !!notes[0].image_prompt,
      image_prompt: notes[0].image_prompt,
      has_instagram_copy: !!notes[0].instagram_copy,
      instagram_copy: notes[0].instagram_copy,
      has_facebook_copy: !!notes[0].facebook_copy,
      facebook_copy: notes[0].facebook_copy,
      has_linkedin_copy: !!notes[0].linkedin_copy,
      linkedin_copy: notes[0].linkedin_copy
    });
  }

  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<Record<string, TabType>>({});

  const getActiveTab = (noteId: string): TabType => {
    return activeTab[noteId] || 'note';
  };

  const setTab = (noteId: string, tab: TabType) => {
    setActiveTab(prev => ({ ...prev, [noteId]: tab }));
  };

  const copyToClipboard = async (content: string, noteId: string) => {
    try {
      // Convert markdown to HTML
      const htmlContent = await marked(content);

      // Add styling to ensure black text and proper formatting for Gmail/Word
      const styledHtml = `
        <div style="font-family: Arial, sans-serif; font-size: 14px; color: #000000; line-height: 1.6;">
          ${htmlContent}
        </div>
        <style>
          h1, h2, h3, h4, h5, h6 { color: #000000; font-weight: bold; margin-top: 1em; margin-bottom: 0.5em; }
          h1 { font-size: 2em; }
          h2 { font-size: 1.5em; }
          h3 { font-size: 1.17em; }
          p { margin: 0.5em 0; color: #000000; }
          ul, ol { margin: 0.5em 0; padding-left: 2em; }
          li { color: #000000; margin: 0.25em 0; }
          strong, b { font-weight: bold; color: #000000; }
          em, i { font-style: italic; }
          a { color: #0066cc; text-decoration: underline; }
        </style>
      `;

      // Create a ClipboardItem with both HTML and plain text
      const blob = new Blob([styledHtml], { type: 'text/html' });
      const textBlob = new Blob([content], { type: 'text/plain' });

      const clipboardItem = new ClipboardItem({
        'text/html': blob,
        'text/plain': textBlob,
      });

      await navigator.clipboard.write([clipboardItem]);

      // Show success feedback
      setCopiedId(noteId);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
      // Fallback to plain text if HTML copy fails
      navigator.clipboard.writeText(content);
      setCopiedId(noteId);
      setTimeout(() => setCopiedId(null), 2000);
    }
  };

  const copyPlainText = async (content: string, noteId: string) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedId(noteId);
      setTimeout(() => setCopiedId(null), 2000);
    } catch (error) {
      console.error('Failed to copy:', error);
    }
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
        {notes.map((note, index) => {
          const currentTab = getActiveTab(note.note_id);

          return (
            <div key={note.note_id} className="border border-gray-200 rounded-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <h3 className="text-xl font-semibold">Note {index + 1}</h3>
              </div>

              {/* Tabs */}
              <div className="border-b border-gray-200 mb-4">
                <div className="flex space-x-1">
                  <button
                    onClick={() => setTab(note.note_id, 'note')}
                    className={`px-4 py-2 font-medium text-sm transition-colors ${
                      currentTab === 'note'
                        ? 'border-b-2 border-blue-600 text-blue-600'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    Note
                  </button>
                  <button
                    onClick={() => setTab(note.note_id, 'image')}
                    className={`px-4 py-2 font-medium text-sm transition-colors ${
                      currentTab === 'image'
                        ? 'border-b-2 border-blue-600 text-blue-600'
                        : 'text-gray-600 hover:text-gray-800'
                    }`}
                  >
                    Image
                  </button>
                </div>
              </div>

              {/* Note Tab Content */}
              {currentTab === 'note' && (
                <>
                  <div className="flex justify-end mb-4">
                    <button
                      onClick={() => copyToClipboard(note.content, note.note_id)}
                      className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                        copiedId === note.note_id
                          ? 'bg-green-600 text-white'
                          : 'bg-blue-600 text-white hover:bg-blue-700'
                      }`}
                    >
                      {copiedId === note.note_id ? '✓ Copied!' : 'Copy (Formatted)'}
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
                </>
              )}

              {/* Image Tab Content */}
              {currentTab === 'image' && (
                <div className="space-y-6">
                  {/* Image Prompt */}
                  <div>
                    <div className="flex justify-between items-center mb-2">
                      <h4 className="text-lg font-semibold text-gray-800">Image Prompt</h4>
                      <button
                        onClick={() => copyPlainText(note.image_prompt || '', `${note.note_id}-image`)}
                        className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                          copiedId === `${note.note_id}-image`
                            ? 'bg-green-600 text-white'
                            : 'bg-blue-600 text-white hover:bg-blue-700'
                        }`}
                      >
                        {copiedId === `${note.note_id}-image` ? '✓ Copied!' : 'Copy'}
                      </button>
                    </div>
                    <div className="bg-gray-50 p-4 rounded-md">
                      <p className="text-gray-800 text-sm leading-relaxed">
                        {note.image_prompt || 'No image prompt generated'}
                      </p>
                    </div>
                  </div>

                  {/* Social Media Copies */}
                  <div className="border-t pt-4">
                    <h4 className="text-lg font-semibold text-gray-800 mb-4">Social Media Copies</h4>

                    {/* Instagram */}
                    <div className="mb-4">
                      <div className="flex justify-between items-center mb-2">
                        <h5 className="text-sm font-semibold text-gray-700">Instagram</h5>
                        <button
                          onClick={() => copyPlainText(note.instagram_copy || '', `${note.note_id}-instagram`)}
                          className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                            copiedId === `${note.note_id}-instagram`
                              ? 'bg-green-600 text-white'
                              : 'bg-purple-600 text-white hover:bg-purple-700'
                          }`}
                        >
                          {copiedId === `${note.note_id}-instagram` ? '✓ Copied!' : 'Copy'}
                        </button>
                      </div>
                      <div className="bg-purple-50 p-3 rounded-md">
                        <p className="text-gray-800 text-sm">
                          {note.instagram_copy || 'No Instagram copy generated'}
                        </p>
                      </div>
                    </div>

                    {/* Facebook */}
                    <div className="mb-4">
                      <div className="flex justify-between items-center mb-2">
                        <h5 className="text-sm font-semibold text-gray-700">Facebook</h5>
                        <button
                          onClick={() => copyPlainText(note.facebook_copy || '', `${note.note_id}-facebook`)}
                          className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                            copiedId === `${note.note_id}-facebook`
                              ? 'bg-green-600 text-white'
                              : 'bg-blue-500 text-white hover:bg-blue-600'
                          }`}
                        >
                          {copiedId === `${note.note_id}-facebook` ? '✓ Copied!' : 'Copy'}
                        </button>
                      </div>
                      <div className="bg-blue-50 p-3 rounded-md">
                        <p className="text-gray-800 text-sm">
                          {note.facebook_copy || 'No Facebook copy generated'}
                        </p>
                      </div>
                    </div>

                    {/* LinkedIn */}
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <h5 className="text-sm font-semibold text-gray-700">LinkedIn</h5>
                        <button
                          onClick={() => copyPlainText(note.linkedin_copy || '', `${note.note_id}-linkedin`)}
                          className={`px-3 py-1 rounded-md text-xs font-medium transition-colors ${
                            copiedId === `${note.note_id}-linkedin`
                              ? 'bg-green-600 text-white'
                              : 'bg-indigo-600 text-white hover:bg-indigo-700'
                          }`}
                        >
                          {copiedId === `${note.note_id}-linkedin` ? '✓ Copied!' : 'Copy'}
                        </button>
                      </div>
                      <div className="bg-indigo-50 p-3 rounded-md">
                        <p className="text-gray-800 text-sm">
                          {note.linkedin_copy || 'No LinkedIn copy generated'}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
