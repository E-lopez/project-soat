import { RefObject } from "react";
import ResponseDisplay from "./ResponseDisplay";
import SearchForm from "./SearchForm";
import { useRef } from "react";

interface ChatUiProps {
  searchRef: RefObject<HTMLDivElement>
}

export default function ChatUi({ searchRef }: Readonly<ChatUiProps>) {
  const responseRef = useRef<HTMLDivElement>(null)

  return (
    <div ref={searchRef} className="flex flex-col justify-center items-center gap-8 min-h-screen py-16 md:py-0 md:h-[100vh]">
      <SearchForm responseRef={responseRef} />
      <ResponseDisplay responseRef={responseRef} />
    </div>
  )
}