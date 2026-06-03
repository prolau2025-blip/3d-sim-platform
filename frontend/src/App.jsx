import React, { useState } from 'react'
import GeneratorForm from './components/GeneratorForm'
import SplatViewer from './components/SplatViewer'
import { Layers } from 'lucide-react'

function App() {
  const [jobId, setJobId] = useState(null)
  const [status, setStatus] = useState('IDLE') // IDLE, PENDING, GENERATING, READY, FAILED
  const [splatUrl, setSplatUrl] = useState(null)

  return (
    <div className="min-h-screen bg-slate-900 text-slate-50 relative overflow-hidden flex flex-col">
      {/* Background decoration */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-blue-500/20 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-purple-500/20 blur-[120px] rounded-full pointer-events-none" />

      {/* Header */}
      <header className="px-8 py-6 flex items-center justify-between relative z-10 border-b border-white/10 glass mb-8 mx-8 mt-8 rounded-2xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center shadow-lg">
            <Layers className="text-white w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400">
            Marble Clone
          </h1>
        </div>
        <div className="text-sm font-medium text-slate-400">
          Powered by Gemini & 3DGS
        </div>
      </header>

      {/* Main Content area */}
      <main className="flex-1 flex px-8 pb-8 gap-8 relative z-10 h-full max-h-full">
        {/* Left column: Controls */}
        <div className="w-1/3 flex flex-col gap-6">
          <GeneratorForm 
            setJobId={setJobId} 
            setStatus={setStatus}
            setSplatUrl={setSplatUrl}
          />
        </div>

        {/* Right column: 3D Viewer */}
        <div className="flex-1 glass rounded-3xl overflow-hidden relative shadow-2xl border border-white/10 min-h-[500px]">
          {status === 'IDLE' && (
            <div className="absolute inset-0 flex flex-col items-center justify-center text-slate-500">
              <Layers className="w-16 h-16 mb-4 opacity-50" />
              <p>Enter a prompt to generate a 3D environment</p>
            </div>
          )}
          
          {(status === 'PENDING' || status === 'GENERATING') && (
            <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-900/80 backdrop-blur-sm z-20">
              <div className="w-16 h-16 border-4 border-blue-500/30 border-t-blue-500 rounded-full animate-spin mb-6"></div>
              <p className="text-xl font-medium animate-pulse">
                {status === 'PENDING' ? 'Analyzing with Gemini...' : 'Generating 3DGS...'}
              </p>
            </div>
          )}

          {status === 'READY' && splatUrl && (
            <SplatViewer splatUrl={splatUrl} />
          )}
        </div>
      </main>
    </div>
  )
}

export default App
