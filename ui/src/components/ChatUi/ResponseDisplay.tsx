import Markdown from 'react-markdown'
import { useAppState } from '../../context/AppStateContext'
import SourceTags from './SourceTags'
import ScoresDisplay from './ScoresDisplay';
import LoadingIndicator from './LoadingIndicator';
import PlaceHolder from './PlaceHolder';
import { RefObject, useState } from 'react';

interface ResponseDisplayProps {
  responseRef: RefObject<HTMLDivElement>
}

export default function ResponseDisplay({ responseRef }: Readonly<ResponseDisplayProps>) {
  const { state } = useAppState()
  const [sourcesVisible, setSourcesVisible] = useState<boolean>(false)

  if (state.error) {
    const isRateLimit = state.error.toLowerCase().includes('daily query limit')
    const isForbidden = state.error.toLowerCase().includes('prohibited')

    return (
      <div className="w-full max-w-2xl rounded-lg border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
        <p className="font-bold mb-1">
          {
            isRateLimit && '⏳ Daily limit reached '
          }
          {
            isForbidden && '🚫 Query not allowed '
          }
        </p>
        <p>{state.error}</p>
      </div>
    )
  }

  return (
    <div className="relative w-full max-w-4xl px-4">
      <div ref={responseRef} >
        <div className="flex flex-col md:flex-row gap-2 md:h-[32rem]">
          <div className="relative flex flex-col w-full md:w-3/5 min-w-0 min-h-[50vh] max-h-[60vh] md:max-h-none md:min-h-[30rem] prose prose-sm bg-white rounded-lg border border-gray-200 px-6 py-5 shadow-sm overflow-auto overscroll-contain scrollbar-thin [scrollbar-width:thin] [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-track]:bg-transparent [&::-webkit-scrollbar-thumb]:bg-gray-200 [&::-webkit-scrollbar-thumb]:rounded-full">
            {state.answer
              ? 
              <Markdown>{state.answer}</Markdown>
              : <PlaceHolder />
            }
            <LoadingIndicator />
            {
              state.answer && 
              <button
                type="button"
                onClick={() => setSourcesVisible(!sourcesVisible)}
                className="sticky bottom-0 w-full mt-3 px-6 py-3 rounded-full bg-blue-200 hover:bg-blue-300 text-gray-700 text-sm font-extrabold transition-colors"
              >
                Read the sources
              </button>
            }
          </div>

          <div className="w-full md:w-2/5 min-w-0 gap-2 prose prose-sm max-w-none shadow-sm">
            {Object.keys(state.scores).length !== 0
              ? <ScoresDisplay />
              : <div className="text-gray-500">Agent Scores will appear here</div>
            } 
          </div>
        </div>
        {sourcesVisible && <SourceTags sources={state.sources} close={setSourcesVisible} />}
      </div>
      <div className="pt-2 max-w-4xl text-gray-500 text-center">
        {notes.map((note, index) => (
          <p key={index} className="text-sm text-gray-500 pb-2">
            * {note}
          </p>
        ))}
      </div>
    </div>
  )
}

const notes = [
  'Low scores also talk about the quality of the data. If the data is not relevant, the model will not be able to answer the question correctly.',
  'The pricing per query displayed above includes generation + evaluation. In the real world, the evaluation is not run for every query, so the cost is lower than what is displayed.',
]