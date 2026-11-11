export default function Bio() {

  return (
    <div className="flex flex-col h-auto w-full md:w-4/5 bg-gray-100 justify-center items-center gap-8 px-6 md:px-8 mb-10 rounded-md py-8 mt-10 md:mt-0">
      <h2 className='text-2xl md:text-3xl font-bold text-right px-2'>Why I build this</h2>
      <div className="flex flex-col md:flex-row gap-4 text-gray-600">
        <p className="w-full md:w-1/2 text-justify">
          After engineering software solutions for major enterprises —the help center AI search bar for <span className='text-green-900 font-bold'>REI</span>- I noticed a recurring pattern: <strong>companies were paying thousands every month for black boxes that didn't actually fit their business.</strong>
        </p>
        <p className="w-full md:w-1/2 text-justify">
          Big companies can afford dedicated engineering teams to build fast, accurate, in-house AI search. But growing SMBs are usually stuck choosing between overpriced subscriptions or clunky tools that hallucinate answers.
        </p>
      </div>
      <div className="px-8 py-4 text-justify border-t-4 border-blue-100">
        <p className="text-lg text-gray-800">I started this project to bridge that gap. My goal is simple: bring high-precision, enterprise-grade RAG architecture to growing teams—helping you save on software bloat, empower your employees, and give your customers instant, accurate answers.</p>
        <p className='mt-4'><strong>Nearshore Advantage:</strong> Latam Based Full US business-hour alignment (COT/EST), fluent English communication, and senior enterprise engineering at transparent SMB-friendly rates.</p>
      </div>
    </div>
    
  )
}