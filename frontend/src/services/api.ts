import axios from 'axios';
import type {
  SearchRequest,
  SearchResponse,
  GenerateNotesRequest,
  GenerateNotesResponse
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 600000, // 600 seconds timeout (10 minutes)
});

export const searchAPI = {
  search: async (request: SearchRequest): Promise<SearchResponse> => {
    const response = await api.post<SearchResponse>('/api/search/', request);
    return response.data;
  },

  getSearchResults: async (searchId: string): Promise<SearchResponse> => {
    const response = await api.get<SearchResponse>(`/api/search/${searchId}`);
    return response.data;
  },

  deleteSearch: async (searchId: string): Promise<void> => {
    await api.delete(`/api/search/${searchId}`);
  },
};

export const generateAPI = {
  generateNotes: async (request: GenerateNotesRequest): Promise<GenerateNotesResponse> => {
    const response = await api.post<GenerateNotesResponse>('/api/generate/', request);
    return response.data;
  },
};

export default api;
