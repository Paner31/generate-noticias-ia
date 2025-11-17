import { useState } from 'react';
import { SearchForm } from './components/SearchForm';
import { SearchResults } from './components/SearchResults';
import { GeneratedNotes } from './components/GeneratedNotes';
import { ConfigPanel } from './components/ConfigPanel';
import { searchAPI, generateAPI } from './services/api';
import type {
  SearchRequest,
  SearchResult,
  LinkGroup,
  GeneratedNote,
} from './types';

type AppState = 'search' | 'results' | 'complete';

function App() {
  const [state, setState] = useState<AppState>('search');
  const [isSearching, setIsSearching] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);

  const [searchId, setSearchId] = useState<string | null>(null);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [generatedNotes, setGeneratedNotes] = useState<GeneratedNote[]>([]);

  const [config, setConfig] = useState({
    customPrompt: '',
    maxTokens: 8000,
    model: 'anthropic/claude-3.5-sonnet',
  });

  const handleSearch = async (request: SearchRequest) => {
    setIsSearching(true);
    try {
      const response = await searchAPI.search(request);
      setSearchId(response.search_id);
      setSearchResults(response.results);
      setState('results');
    } catch (error: any) {
      alert(`Search failed: ${error.message}`);
    } finally {
      setIsSearching(false);
    }
  };

  const handleGenerate = async (selectedUrls: string[], groups: LinkGroup[]) => {
    if (!searchId) return;

    setIsGenerating(true);
    try {
      const response = await generateAPI.generateNotes({
        search_id: searchId,
        selected_urls: selectedUrls,
        link_groups: groups,
        custom_prompt: config.customPrompt || undefined,
        max_tokens: config.maxTokens,
        model: config.model || undefined,
      });

      setGeneratedNotes(response.notes);
      setState('complete');
    } catch (error: any) {
      alert(`Generation failed: ${error.message}`);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleReset = () => {
    setState('search');
    setSearchId(null);
    setSearchResults([]);
    setGeneratedNotes([]);
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">News Generator</h1>
          <p className="text-gray-600 mt-1">
            Search, curate, and generate professional news articles
          </p>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {state === 'search' && (
          <SearchForm onSearch={handleSearch} isLoading={isSearching} />
        )}

        {state === 'results' && (
          <>
            <ConfigPanel onConfigChange={setConfig} />
            <SearchResults
              results={searchResults}
              onGenerate={handleGenerate}
              isGenerating={isGenerating}
            />

            {isGenerating && (
              <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
                <div className="bg-white rounded-lg p-8 max-w-md w-full mx-4">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600 mx-auto mb-4"></div>
                    <h3 className="text-xl font-bold mb-2">Generando Notas...</h3>
                    <p className="text-gray-600 mb-4">
                      Esto puede tomar varios minutos. Por favor espera.
                    </p>
                    <div className="text-sm text-gray-500">
                      <p>• Obteniendo contenido completo de las fuentes</p>
                      <p>• Generando artículos con IA</p>
                      <p>• Creando contenido para redes sociales</p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </>
        )}

        {state === 'complete' && (
          <GeneratedNotes notes={generatedNotes} onReset={handleReset} />
        )}
      </main>

      <footer className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-600 text-sm">
          Powered by Perplexity Search & OpenRouter AI
        </div>
      </footer>
    </div>
  );
}

export default App;
