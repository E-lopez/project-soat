export type scoresT = {
    answer_relevance?: number,
    context_relevance?: number,
    groundedness?: number,
    latency_ms?: number,
    input_tokens?: number,
    output_tokens?: number,
    estimated_cost?: number,
    model_id?: string,
    user_query?: string
  }

export interface QueryResponseChunk {
  type: 'answer_chunk' | 'metrics' | 'sources';
  content?: string;
  sources?: string[];
  scores: scoresT;
  latency_ms?: number;
}