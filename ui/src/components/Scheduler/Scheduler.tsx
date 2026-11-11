import { useEffect, useRef } from 'react'

export default function Scheduler() {
  const buttonRef = useRef<HTMLElement>(null)

  useEffect(() => {
    const SCRIPT_SRC = 'https://calendar.google.com/calendar/scheduling-button-script.js'
    const LINK_HREF = 'https://calendar.google.com/calendar/scheduling-button-script.css'

    const loadButton = () => {
      (window as any).calendar?.schedulingButton.load({
        url: 'https://calendar.google.com/calendar/appointments/schedules/AcZssZ2qfGt5Lgh_4H5zhhnGEPGYALciIHG_7HwvMhF_Bs5eYukbbJlbtvQdMA3JKwBBQJEUOCHeioSR?gv=true',
        color: '#039BE5',
        label: 'Book a 20-Min Architecture Audit',
        target: buttonRef.current,
      })
    }

    if (document.querySelector(`script[src="${SCRIPT_SRC}"]`)) {
      loadButton()
      return
    }

    const link = document.createElement('link')
    link.href = LINK_HREF
    link.rel = 'stylesheet'
    document.head.appendChild(link)

    const script = document.createElement('script')
    script.src = SCRIPT_SRC
    script.async = true
    script.onload = loadButton
    document.head.appendChild(script)
  }, [buttonRef])

  return (
    <div className="flex flex-col items-center gap-8 px-8 mb-10 pt-16 md:pt-0">
      <div>
        <span ref={buttonRef} />
      </div>
    </div>
  )
}