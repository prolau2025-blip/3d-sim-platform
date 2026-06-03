import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { ImagePlus, Sparkles } from 'lucide-react'

export default function GeneratorForm({ setJobId, setStatus, setSplatUrl }) {
  const [prompt, setPrompt] = useState('')
  const [file, setFile] = useState(null)
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!prompt) return

    setIsSubmitting(true)
    setStatus('PENDING')
    setSplatUrl(null)

    const formData = new FormData()
    formData.append('prompt', prompt)
    if (file) {
      formData.append('image', file)
    }

    try {
      // Calls relative API endpoint (proxied in dev, native in Vercel prod)
      const response = await axios.post('/api/generate', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      const newJobId = response.data.job_id
      setJobId(newJobId)
      pollStatus(newJobId)
    } catch (err) {
      console.error(err)
      setStatus('FAILED')
      setIsSubmitting(false)
    }
  }

  const pollStatus = async (id) => {
    const interval = setInterval(async () => {
      try {
        const res = await axios.get(`/api/status/${id}`)
        const state = res.data.status
        setStatus(state)
        
        if (state === 'READY') {
          clearInterval(interval)
          setSplatUrl(res.data.ply_url)
          setIsSubmitting(false)
        } else if (state === 'FAILED') {
          clearInterval(interval)
          setIsSubmitting(false)
        }
      } catch (err) {
        console.error(err)
      }
    }, 2000)
  }

  return (
    <form onSubmit={handleSubmit} className="glass p-6 rounded-3xl flex flex-col gap-6 h-full border border-white/10 shadow-xl">
      <div className="flex flex-col gap-2">
        <label className="text-sm font-semibold text-slate-300 ml-1">Describe the Scene</label>
        <textarea 
          className="w-full bg-slate-900/50 border border-white/10 rounded-xl p-4 text-slate-100 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500/50 resize-none h-32 transition-all"
          placeholder="A majestic marble statue of a lion in a roman courtyard, cinematic lighting, 8k resolution..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
        />
      </div>

      <div className="flex flex-col gap-2">
        <label className="text-sm font-semibold text-slate-300 ml-1">Reference Image (Optional)</label>
        <label className="w-full bg-slate-900/50 border border-white/10 border-dashed rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer hover:bg-slate-800/50 transition-all text-slate-400 group">
          <input 
            type="file" 
            className="hidden" 
            accept="image/*"
            onChange={(e) => setFile(e.target.files[0])}
          />
          <ImagePlus className="w-8 h-8 mb-2 group-hover:scale-110 transition-transform" />
          <span className="text-sm text-center">{file ? file.name : 'Click to upload image'}</span>
        </label>
      </div>

      <div className="flex-1" />

      <button 
        disabled={isSubmitting || !prompt}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold py-4 rounded-xl flex items-center justify-center gap-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-blue-500/25"
      >
        <Sparkles className="w-5 h-5" />
        {isSubmitting ? 'Generating...' : 'Generate 3D World'}
      </button>
    </form>
  )
}
