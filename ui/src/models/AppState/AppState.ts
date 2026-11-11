import { QueryResponseChunk, scoresT } from '../interfaces/QueryResponseChunk'

export interface AppState {
  loading: boolean
  evaluating: boolean
  indexCreated: boolean
  chunk: QueryResponseChunk | null
  answer: string
  scores: scoresT
  sources: string[]
  error: string | null
}