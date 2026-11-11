import { useAppState } from "../../context/AppStateContext"

export default function PlaceHolder() {
  const { state } = useAppState()

  if (state.error) {
    return (
      <div className="w-full max-w-2xl rounded-lg border border-red-200 bg-red-50 px-5 py-8 text-sm text-red-700">
        {state.error} Error!
      </div>
    )
  }
  
  return (
    <div className="h-[1rem] text-gray-500 font-mono">
      {!state.loading &&
        <div>
          <h2>Ask a question to get started!</h2>
          <p className="text-sm">Select an airline from the list on the left</p>
          <p className="text-sm">Select <strong>-All Airlines-</strong> to compare between companies</p>
          <p className="text-sm">The Agent will read the Contracts of Carriage and give a precise answer to your query</p>
          <p className="text-sm">See performace metrics in real time!</p>
        </div> 
      }
    </div>
  )
}
