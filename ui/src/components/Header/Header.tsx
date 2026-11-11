import { useEffect, useRef } from 'react'

interface HeaderProps {
  onCtaClick: () => void
}

export default function Header({ onCtaClick }: Readonly<HeaderProps>) {
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const mouse = useRef({ x: 0, y: 0 })
  const animRef = useRef<number>(0)

  const containerRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    const container = containerRef.current
    if (!canvas || !container) return
    const ctx = canvas.getContext('2d')!

    const DOT_SPACING = 28
    const DOT_RADIUS = 1.2
    const INFLUENCE = 120
    const MAX_SHIFT = 6

    const resize = () => {
      canvas.width = canvas.offsetWidth
      canvas.height = canvas.offsetHeight
    }
    resize()
    window.addEventListener('resize', resize)

    const onMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect()
      mouse.current = { x: e.clientX - rect.left, y: e.clientY - rect.top }
    }
    container.addEventListener('mousemove', onMouseMove)

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height)
      const cols = Math.ceil(canvas.width / DOT_SPACING) + 1
      const rows = Math.ceil(canvas.height / DOT_SPACING) + 1

      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          const ox = c * DOT_SPACING
          const oy = r * DOT_SPACING
          const dx = ox - mouse.current.x
          const dy = oy - mouse.current.y
          const dist = Math.sqrt(dx * dx + dy * dy)
          const factor = Math.max(0, 1 - dist / INFLUENCE)
          const shift = factor * MAX_SHIFT
          const nx = ox - (dx / (dist || 1)) * shift
          const ny = oy - (dy / (dist || 1)) * shift
          const alpha = 0.15 + factor * 0.5

          ctx.beginPath()
          ctx.arc(nx, ny, DOT_RADIUS + factor * 1.2, 0, Math.PI * 2)
          ctx.fillStyle = `rgba(100, 116, 139, ${alpha})`
          ctx.fill()
        }
      }
      animRef.current = requestAnimationFrame(draw)
    }
    draw()

    return () => {
      cancelAnimationFrame(animRef.current)
      window.removeEventListener('resize', resize)
      container.removeEventListener('mousemove', onMouseMove)
    }
  }, [])

  return (
    <div ref={containerRef} className="relative flex justify-center align-center h-[100vh] w-full p-8 bg-sky-200 overflow-hidden">
      <canvas ref={canvasRef} className="absolute inset-0 w-full h-full" />

      <div className="relative flex flex-col justify-center align-center gap-14 w-full max-w-[1024px] 2xl:max-w-[1024px]">
        <div className="flex flex-col md:flex-row gap-2 justify-center">
          <div className="flex md:w-1/3 justify-center bg-red-100 pr-2 pb-2">
            <h1 className="text-6xl xl:text-7xl text-right font-bold text-gray-900 py-2 sm:py-0">Stop Searching. <br/> <span className='text-orange-500'>Start Solving.</span></h1>
          </div>

          <div className="flex flex-col md:w-2/3 justify-center px-5">
            <h2 className="font-mono text-lg md:text-2xl xl:text-3xl"> <span className='text-sky-700'>Supercharge your</span> <strong>support team, sales reps, and ops</strong> with an AI that actually knows your business inside out.</h2>
            <h2 className="font-mono text-lg md:text-2xl xl:text-3xl mt-8 text-gray-900 border-l-4 border-orange-400 pl-4"> Custom made for you  <br/> fast  <br/> secure  <br/> reliable<span className='text-orange-500'>.</span></h2>
          </div>
        </div>

        <div className="flex justify-center">
          <button
            type="button"
            onClick={onCtaClick}
            className="hover:bg-blue-200 bg-blue-400 hover:text-orange-500 text-white font-bold text-lg py-2 px-4 rounded-full shadow-md transition-colors"
          >
            See it in action!
          </button>
        </div>
      </div>
    </div>
  )
}