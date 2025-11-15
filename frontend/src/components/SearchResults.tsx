import React, { useState } from 'react';
import type { SearchResult, LinkGroup } from '../types';

interface SearchResultsProps {
  results: SearchResult[];
  onGenerate: (selectedUrls: string[], groups: LinkGroup[]) => void;
  isGenerating: boolean;
}

export const SearchResults: React.FC<SearchResultsProps> = ({
  results,
  onGenerate,
  isGenerating
}) => {
  const [selectedUrls, setSelectedUrls] = useState<Set<string>>(new Set());
  const [groups, setGroups] = useState<LinkGroup[]>([]);
  const [groupingMode, setGroupingMode] = useState(false);
  const [currentGroupUrls, setCurrentGroupUrls] = useState<Set<string>>(new Set());
  const [groupName, setGroupName] = useState('');

  const toggleUrlSelection = (url: string) => {
    const newSelected = new Set(selectedUrls);
    if (newSelected.has(url)) {
      newSelected.delete(url);
    } else {
      newSelected.add(url);
    }
    setSelectedUrls(newSelected);
  };

  const toggleUrlForGrouping = (url: string) => {
    const newGroupUrls = new Set(currentGroupUrls);
    if (newGroupUrls.has(url)) {
      newGroupUrls.delete(url);
    } else {
      newGroupUrls.add(url);
    }
    setCurrentGroupUrls(newGroupUrls);
  };

  const createGroup = () => {
    if (currentGroupUrls.size < 2) {
      alert('Please select at least 2 URLs to create a group');
      return;
    }

    const newGroup: LinkGroup = {
      group_id: `group-${Date.now()}`,
      name: groupName || `Group ${groups.length + 1}`,
      urls: Array.from(currentGroupUrls),
    };

    setGroups([...groups, newGroup]);

    // Remove grouped URLs from individual selection
    const newSelected = new Set(selectedUrls);
    currentGroupUrls.forEach(url => newSelected.delete(url));
    setSelectedUrls(newSelected);

    // Reset grouping state
    setCurrentGroupUrls(new Set());
    setGroupName('');
    setGroupingMode(false);
  };

  const removeGroup = (groupId: string) => {
    setGroups(groups.filter(g => g.group_id !== groupId));
  };

  const handleGenerate = () => {
    const totalNotes = selectedUrls.size + groups.length;

    if (totalNotes === 0) {
      alert('Please select at least one URL or create a group');
      return;
    }

    if (totalNotes > 5) {
      alert('Maximum 5 notes allowed (individual URLs + groups)');
      return;
    }

    onGenerate(Array.from(selectedUrls), groups);
  };

  const isUrlInGroup = (url: string) => {
    return groups.some(g => g.urls.includes(url));
  };

  const totalNotesCount = selectedUrls.size + groups.length;

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">
          Search Results ({results.length})
        </h2>

        <div className="flex gap-2">
          <button
            onClick={() => setGroupingMode(!groupingMode)}
            className={`px-4 py-2 rounded-md font-medium ${
              groupingMode
                ? 'bg-red-600 text-white hover:bg-red-700'
                : 'bg-green-600 text-white hover:bg-green-700'
            }`}
          >
            {groupingMode ? 'Cancel Grouping' : 'Create Group'}
          </button>
        </div>
      </div>

      {groupingMode && (
        <div className="mb-4 p-4 bg-blue-50 border border-blue-200 rounded-md">
          <h3 className="font-semibold mb-2">Creating Group ({currentGroupUrls.size} selected)</h3>
          <input
            type="text"
            value={groupName}
            onChange={(e) => setGroupName(e.target.value)}
            placeholder="Group name (optional)"
            className="w-full px-3 py-2 border border-gray-300 rounded-md mb-2"
          />
          <button
            onClick={createGroup}
            disabled={currentGroupUrls.size < 2}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-gray-400"
          >
            Save Group
          </button>
        </div>
      )}

      {groups.length > 0 && (
        <div className="mb-4">
          <h3 className="font-semibold mb-2">Groups ({groups.length})</h3>
          <div className="space-y-2">
            {groups.map(group => (
              <div key={group.group_id} className="p-3 bg-purple-50 border border-purple-200 rounded-md">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <div className="font-medium text-purple-900">{group.name}</div>
                    <div className="text-sm text-purple-700">{group.urls.length} sources</div>
                  </div>
                  <button
                    onClick={() => removeGroup(group.group_id)}
                    className="text-red-600 hover:text-red-800 text-sm font-medium"
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="space-y-4 mb-6">
        {results.map((result, index) => {
          const isInGroup = isUrlInGroup(result.url);
          const isSelected = selectedUrls.has(result.url);
          const isGroupSelected = groupingMode && currentGroupUrls.has(result.url);

          return (
            <div
              key={index}
              className={`p-4 border rounded-md transition-colors ${
                isInGroup
                  ? 'bg-purple-50 border-purple-300 opacity-60'
                  : isSelected
                  ? 'bg-blue-50 border-blue-300'
                  : isGroupSelected
                  ? 'bg-green-50 border-green-300'
                  : 'bg-white border-gray-200 hover:border-gray-300'
              }`}
            >
              <div className="flex items-start gap-3">
                {!isInGroup && (
                  <input
                    type="checkbox"
                    checked={groupingMode ? isGroupSelected : isSelected}
                    onChange={() =>
                      groupingMode
                        ? toggleUrlForGrouping(result.url)
                        : toggleUrlSelection(result.url)
                    }
                    className="mt-1"
                  />
                )}

                <div className="flex-1">
                  <h3 className="font-semibold text-lg mb-1">{result.title}</h3>
                  {result.source && (
                    <p className="text-sm text-gray-600 mb-2">{result.source}</p>
                  )}
                  <p className="text-gray-700 mb-2">{result.summary}</p>
                  <a
                    href={result.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-600 hover:underline text-sm"
                  >
                    {result.url}
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="border-t pt-4">
        <div className="flex justify-between items-center mb-4">
          <div className="text-sm text-gray-600">
            Selected: {totalNotesCount} / 5 notes
          </div>
          <button
            onClick={handleGenerate}
            disabled={isGenerating || totalNotesCount === 0 || totalNotesCount > 5}
            className="bg-green-600 text-white px-6 py-3 rounded-md hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors"
          >
            {isGenerating ? 'Generating...' : 'Generate Notes'}
          </button>
        </div>
      </div>
    </div>
  );
};
