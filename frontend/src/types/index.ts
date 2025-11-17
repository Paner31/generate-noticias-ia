export interface SearchResult {
  url: string;
  title: string;
  summary: string;
  source?: string;
}

export interface SearchResponse {
  results: SearchResult[];
  search_id: string;
  total_results: number;
}

export interface SearchRequest {
  query: string;
  max_results?: number;
  max_tokens?: number;
  search_recency?: 'hour' | 'day' | 'week' | 'month' | 'year';
  country?: string;
  search_after_date?: string;
  search_before_date?: string;
  domain_filter?: string[];
  language?: string;
}

export interface LinkGroup {
  group_id: string;
  name?: string;
  urls: string[];
}

export interface GenerateNotesRequest {
  search_id: string;
  selected_urls: string[];
  link_groups: LinkGroup[];
  custom_prompt?: string;
  max_tokens?: number;
  model?: string;
}

export interface GeneratedNote {
  note_id: string;
  content: string;
  sources: string[];
  tokens_used: number;
  model: string;
  image_prompt?: string;
  instagram_copy?: string;
  facebook_copy?: string;
  linkedin_copy?: string;
}

export interface GenerateNotesResponse {
  notes: GeneratedNote[];
  total_notes: number;
  message: string;
}
