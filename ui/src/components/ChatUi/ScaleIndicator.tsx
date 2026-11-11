import { useAppState } from "../../context/AppStateContext"

export default function ScaleIndicator({score = 0.0}: Readonly<{ score: number | undefined }>) {
  const { state } = useAppState()
  
  return (
    <div className="w-full flex justify-center gap-1 font-mono mt-4 mb-6">
      <p className='text-xs m-0'>none</p>
      {
        Array.from({ length: 10 }).map((_, i) => (
          <div 
            key={i}
            className={`h-4 rounded-full ${state.evaluating && 'animate-ping bg-red-200'} ${i < score*10 ? 'bg-blue-500' : 'bg-gray-200'}`}
            style={{ width: '1rem' }}
          />
        ))
      }
      <p className='text-xs m-0'>totally</p>
    </div>
  )
}
