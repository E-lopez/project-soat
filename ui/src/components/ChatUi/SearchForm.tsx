import { FormEvent, RefObject, useState } from 'react'
import { useAppState } from '../../context/AppStateContext'
import { sendQuery} from '../../services/api'

interface SearchFormProps {
  responseRef: RefObject<HTMLDivElement>
}

export default function SearchForm({ responseRef }: Readonly<SearchFormProps>) {
  const { state, dispatch } = useAppState()
  const [question, setQuestion] = useState('')
  const [company, setCompany] = useState('')

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!question.trim() || state.loading) return

    if (window.innerWidth < 768) {
      responseRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    dispatch({ type: 'START_QUERY' })
    try {
      const response = sendQuery(question.trim(), company)
      for await (const chunk of response) {
        if (chunk.type === 'answer_chunk') {
          dispatch({ type: 'SET_QUERY_RESPONSE', payload: { answer: chunk.content ?? '' } })
        } 
        else if (chunk.type === 'sources'){
          dispatch({ type: 'SET_QUERY_SOURCES', payload: { sources: chunk.sources ?? [] } })
        }
         else {
          dispatch({ type: 'SET_QUERY_METRICS', payload: { scores: { ...chunk.scores, latency_ms: chunk.latency_ms } } })
        }
      }
    } catch (err) {
      dispatch({
        type: 'SET_ERROR',
        payload: err instanceof Error ? err.message : 'An unexpected error occurred.',
      })
    }
  }

  return (
    <div className='flex flex-col text-center w-full max-w-3xl px-4'>
      <p className="text-md text-gray-500">
          Ask Anything: Airline Contracts of Carriage
      </p>
      <form onSubmit={handleSubmit} className="flex w-full rounded-full border border-gray-300 bg-blue-100 p-1 focus-within:ring-2 focus-within:ring-blue-500 transition-shadow my-2">
        <select
          value={company ?? ''}
          onChange={(e) => setCompany(e.target.value ? e.target.value : '')}
          disabled={state.loading}
          className="bg-transparent pl-2 md:pl-4 pr-1 py-3 text-xs md:text-sm text-gray-800 font-bold focus:outline-none disabled:text-gray-400 border-r border-gray-300 cursor-pointer w-[80px] md:w-auto shrink-0"
        >
          <option value="">All</option>
          <option value="Cape Air">Cape Air</option>
          <option value="United Airlines">United</option>
          <option value="Frontier">Frontier</option>
        </select>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value.slice(0, 500))}
          placeholder="Carry-on dimensions?"
          maxLength={500}
          disabled={state.loading}
          className="bg-transparent flex-1 min-w-0 pl-2 pr-1 py-3 text-sm focus:outline-none disabled:text-gray-400"
        />
        {question.length > 400 && (
          <span className="self-center pr-2 text-xs text-gray-400 shrink-0">{500 - question.length}</span>
        )}
        <button
          type="submit"
          disabled={state.loading || !question.trim()}
          className="px-3 md:px-6 py-3 rounded-full bg-blue-200 hover:bg-blue-400 text-gray-700 text-xs md:text-sm font-extrabold transition-colors disabled:opacity-40 disabled:bg-transparent disabled:text-gray-400 disabled:cursor-not-allowed whitespace-nowrap shrink-0"
        >
          Search
        </button>
      </form>
      <div className='flex flex-col md:flex-row gap-2 md:justify-between'>
        <p className='text-md text-gray-700 text-center bg-gray-200 p-1 rounded-md'>Or choose a question</p>
        {questions.map((q, i) => (
          <button
            key={i + q.airline}
            onClick={() => {
              setQuestion(q.question);
              setCompany(q.airline ?? '');
            }}
            type='button'
            className="px-3 py-1 text-xs rounded-full bg-blue-100 hover:bg-blue-200 text-gray-700 transition-colors"
          >
            {q.question}
          </button>
        ))}
      </div>
    </div>
  )
}

const questions =  [  {
    question: 'What are the carry-on baggage dimensions in Frontier?',
    airline: 'Frontier',
  },
  {
    question: 'My baggage was damaged in a United flight. What to do?',
    airline: 'United Airlines',
  },
  {
    question: 'Can I travel with a child with disabilities?',
    airline: '',
  },
]