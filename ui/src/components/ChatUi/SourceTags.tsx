import { Dispatch, SetStateAction } from "react"

interface SourceTagsProps {
  sources: string[],
  close: Dispatch<SetStateAction<boolean>>
}

export default function SourceTags({ sources, close }: Readonly<SourceTagsProps>) {
  if (!sources.length) return null

  return (
    <div className="absolute top-0 left-0 bg-white w-full h-full z-50 overflow-y-auto flex flex-wrap items-start gap-2 p-10">
      <button className="absolute top-4 right-4 rounded-md bg-gray-200 px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-300" onClick={() => close(false)}>Close</button>
      <span className="text-lg font-bold uppercase tracking-wide text-gray-800">Sources</span>
      {sources.map((source) => (
        <span
          key={source}
          className="rounded-sm border border-blue-200 bg-blue-50 p-3 text-xs font-medium text-blue-700"
        >
          {source}
        </span>
      ))}
    </div>
  )
}
