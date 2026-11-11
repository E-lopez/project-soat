import { useRef } from 'react'
import Header from '../components/Header/Header'
import ChatUi from '../components/ChatUi/ChatUi'
import Bio from '../components/Bio/Bio'
import Footer from '../components/Footer/Footer'
import Achievements from '../components/Achievements/Achievements'

export default function Home() {
  const searchRef = useRef<HTMLDivElement>(null)

  const scrollToSearch = () => {
    searchRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center justify-start pb-20">
      <button 
        type="button"
        onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}
      >
        <h1 className="fixed z-50 top-4 right-4 text-3xl text-right font-light text-gray-700 bg-gray-200 px-4 py-1 rounded-xl ">true<span className="text-sky-500">Docs</span> <span className="bg-sky-500 text-white p-1">AI</span></h1>
      </button>
      <Header onCtaClick={scrollToSearch} />
      <ChatUi searchRef={searchRef} />

      <Achievements />
      <Bio />
      <Footer />
    </div>
  )
}

