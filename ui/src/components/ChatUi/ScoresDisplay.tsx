import { useAppState } from '../../context/AppStateContext'
import ScaleIndicator from './ScaleIndicator';

export default function ScoresDisplay() {
  const { state: { error, scores, sources } } = useAppState();
  const  {
    answer_relevance,
    context_relevance,
    groundedness,
    estimated_cost,
    latency_ms
  } = scores;

  if (error) {
    return (
      <div className="w-full max-w-2xl rounded-lg border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700">
        {error}
      </div>
    )
  }

  return (
    <div className="w-full h-full min-h-0 flex flex-col gap-y-2 font-mono overflow-hidden">
      <div className="w-full flex-1 min-h-0 p-2 rounded-lg border border-gray-200 overflow-y-hidden">
        <h3 className='m-0 mb-2'>Agent Scores</h3>
        <p className='m-0 text-sm font-bold'>Context Relevance: <span className="text-xs font-normal">Did we pull the exact right policy clause?</span></p>
        <ScaleIndicator score={context_relevance} />

        <p className='m-0 text-sm font-bold'>Groundedness: <span className="text-xs font-normal">Is every word in th answer backed by the documents?</span></p>
        <ScaleIndicator score={groundedness} />
        
        <p className='m-0 text-sm font-bold'>Answer Relevance: <span className="text-xs font-normal">Did we directly answer what was asked with no fluff?</span></p>
        <ScaleIndicator score={answer_relevance} />

        <p className='m-0 text-sm font-bold'>Latency: <span className="text-xs font-normal">Time to first token</span></p>
        <p className='mt-1 bg-gray-200 rounded-md px-2 py-1 inline-block text-xs'>{latency_ms} ms</p>

      </div>
      <div className="w-full h-1/5 flex flex-col text-center justify-center shrink-0 rounded-lg border border-gray-200 p-2 bg-slate-50/50">
        <h3 className='m-1 text-sm tracking-tighter'>trueDocs AI vs. Call Center Call</h3>
        <div className='flex flex-row gap-2'>
          <p className={`mt-1 w-1/2 ${estimated_cost ? 'bg-green-200' : 'bg-gray-500'} rounded-md px-1 py-1 inline-block text-sm truncate`}>{estimated_cost?.toFixed(5)} USD</p>
          <p className='mt-1 w-1/2 bg-gray-200 rounded-md px-1 py-1 inline-block text-sm truncate'>~${sources.length > 10 ? 12 : 4}.00 USD</p>
        </div>
      </div>
    </div>
  )
}
