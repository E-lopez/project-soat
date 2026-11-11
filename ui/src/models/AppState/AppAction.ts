import { scoresT } from "../interfaces/QueryResponseChunk";

export type AppAction =
  | { type: 'START_QUERY' }
  | { type: 'SET_QUERY_RESPONSE'; payload: { answer: string } }
  | { type: 'SET_QUERY_SOURCES'; payload: { sources: string[] } }
  | { type: 'SET_INDEX_STATUS'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'SET_QUERY_METRICS'; payload: { scores: scoresT | {} } };