import axios from 'axios';
import type {
  SearchRequest,
  SearchResponse,
  GenerateNotesRequest,
  GenerateNotesResponse,
  JobStatusResponse
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
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

  getJobStatus: async (jobId: string): Promise<JobStatusResponse> => {
    const response = await api.get<JobStatusResponse>(`/api/generate/status/${jobId}`);
    return response.data;
  },
};

export default api;
