import { createContext, useContext, useReducer, ReactNode } from 'react'
import { AppState } from '../models/AppState/AppState';
import { AppAction } from '../models/AppState/AppAction';


const initialState: AppState = {
  loading: false,
  evaluating: false,
  indexCreated: false,
  chunk: null,
  answer: '',
  sources: [],
  scores: {
    answer_relevance: 0.0,
    context_relevance: 0.0,
    groundedness: 0.0,
    latency_ms: 0.0,
    input_tokens: 0.0,
    output_tokens: 0.0,
    estimated_cost: 0.0,
    model_id: '',
    user_query: ''
  },
  error: null,
}

function appReducer(state: AppState, action: AppAction): AppState {
  switch (action.type) {
    case 'START_QUERY':
      return { ...state, loading: true, evaluating: true, answer: '', scores: initialState.scores, sources: [], error: null }
    case 'SET_QUERY_RESPONSE':
      return { ...state, loading: false, answer: state.answer + action.payload.answer }
    case 'SET_QUERY_SOURCES':
      return { ...state, sources: action.payload.sources }
    case 'SET_QUERY_METRICS':
      return { 
        ...state,
        scores: { 
          ...state.scores,
          ...action.payload.scores
        }, 
        evaluating: false,
      }
    case 'SET_INDEX_STATUS':
      return { ...state, indexCreated: action.payload }
    case 'SET_ERROR':
      return { ...state, loading: false, error: action.payload }
  }
}

interface AppStateContextValue {
  state: AppState
  dispatch: React.Dispatch<AppAction>
}

const AppStateContext = createContext<AppStateContextValue | null>(null)

export function AppStateProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(appReducer, initialState)
  return (
    <AppStateContext.Provider value={{ state, dispatch }}>
      {children}
    </AppStateContext.Provider>
  )
}

export function useAppState() {
  const ctx = useContext(AppStateContext)
  if (!ctx) throw new Error('useAppState must be used within AppStateProvider')
  return ctx
}
