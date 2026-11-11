import { useEffect, useRef, useState } from 'react'
import AchievementCard from './AchievementCard'
import achievements from './achievements.data'
import Scheduler from '../Scheduler/Scheduler'


export default function Achievements() {
  const ref = useRef<HTMLDivElement>(null)
  const [active, setActive] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setActive(true) },
      { threshold: 0.2 }
    )
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [])

  return (
    <div ref={ref} className="flex flex-col h-auto w-full md:w-4/5  justify-center items-center gap-8 px-6 md:px-8 mb-10 rounded-md py-8 mt-10 md:mt-0">
      <div className="text-center">
        <h2 className="text-2xl md:text-3xl font-black text-gray-800 tracking-tight">What Have I Done for Others</h2>
        <div className="mt-2 mx-auto w-12 h-1 bg-red-500 rounded-full" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full">
        {achievements.map((a) => (
          <AchievementCard key={a.figure} {...a} active={active} />
        ))}
      </div>

      <p className="text-center text-lg font-bold text-gray-700 mt-2">
        Let's build your next goal{' '}
        <span className="text-orange-500">together</span>
        <span className={`inline-block ml-1 transition-transform duration-700 ${active ? 'translate-x-1' : ''}`}>→</span>
      </p>
      <Scheduler />
    </div>
  )
}
