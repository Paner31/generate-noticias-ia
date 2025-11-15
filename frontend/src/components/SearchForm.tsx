import React, { useState } from 'react';
import type { SearchRequest } from '../types';

interface SearchFormProps {
  onSearch: (request: SearchRequest) => void;
  isLoading: boolean;
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch, isLoading }) => {
  const [query, setQuery] = useState('');
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [filters, setFilters] = useState({
    max_results: 10,
    max_tokens: 1000,
    search_recency: '',
    country: '',
    language: '',
    domain_filter: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const request: SearchRequest = {
      query,
      max_results: filters.max_results,
      max_tokens: filters.max_tokens,
    };

    if (filters.search_recency) {
      request.search_recency = filters.search_recency as any;
    }
    if (filters.country) {
      request.country = filters.country;
    }
    if (filters.language) {
      request.language = filters.language;
    }
    if (filters.domain_filter) {
      request.domain_filter = filters.domain_filter.split(',').map(d => d.trim());
    }

    onSearch(request);
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6">
      <h2 className="text-2xl font-bold mb-4">Search News</h2>

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="query" className="block text-sm font-medium text-gray-700 mb-2">
            Search Query
          </label>
          <input
            type="text"
            id="query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            placeholder="Enter your search query..."
            required
          />
        </div>

        <div className="mb-4">
          <button
            type="button"
            onClick={() => setShowAdvanced(!showAdvanced)}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            {showAdvanced ? '− Hide' : '+ Show'} Advanced Filters
          </button>
        </div>

        {showAdvanced && (
          <div className="space-y-4 mb-4 p-4 bg-gray-50 rounded-md">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Results
                </label>
                <input
                  type="number"
                  value={filters.max_results}
                  onChange={(e) => setFilters({ ...filters, max_results: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  min="1"
                  max="50"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Tokens per Result
                </label>
                <input
                  type="number"
                  value={filters.max_tokens}
                  onChange={(e) => setFilters({ ...filters, max_tokens: parseInt(e.target.value) })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  min="100"
                  max="4000"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Time Filter
                </label>
                <select
                  value={filters.search_recency}
                  onChange={(e) => setFilters({ ...filters, search_recency: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="">All time</option>
                  <option value="hour">Last hour</option>
                  <option value="day">Last day</option>
                  <option value="week">Last week</option>
                  <option value="month">Last month</option>
                  <option value="year">Last year</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Country
                </label>
                <input
                  type="text"
                  value={filters.country}
                  onChange={(e) => setFilters({ ...filters, country: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="e.g., US, MX, ES"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Language
                </label>
                <input
                  type="text"
                  value={filters.language}
                  onChange={(e) => setFilters({ ...filters, language: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="e.g., en, es, fr"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Domain Filter
                </label>
                <input
                  type="text"
                  value={filters.domain_filter}
                  onChange={(e) => setFilters({ ...filters, domain_filter: e.target.value })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                  placeholder="Comma-separated domains"
                />
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          disabled={isLoading || !query.trim()}
          className="w-full bg-blue-600 text-white py-3 px-6 rounded-md hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-medium transition-colors"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </form>
    </div>
  );
};
