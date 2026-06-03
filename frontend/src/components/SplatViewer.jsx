import React, { useRef, useEffect } from 'react'
import * as GaussianSplats3D from '@mkkellogg/gaussian-splats-3d'

export default function SplatViewer({ splatUrl }) {
  const containerRef = useRef(null)

  useEffect(() => {
    if (!containerRef.current) return
    
    let viewer = null
    try {
      viewer = new GaussianSplats3D.Viewer({
        selfDrivenMode: true,
        useWebXR: false,
        rootElement: containerRef.current,
        cameraUp: [0, 1, 0],
        initialCameraPosition: [0, 1, 5],
        initialCameraLookAt: [0, 0, 0],
        sharedMemoryForWorkers: false // CRITICAL FIX: Disables SharedArrayBuffer which breaks on Vercel without strict CORS headers
      })

      viewer.addSplatScene(splatUrl, {
        splatAlphaCrop: 0.1,
      })
      .then(() => {
        viewer.start()
      })
      .catch((err) => {
          console.error("Failed to load splat scene:", err);
      });
    } catch(err) {
      console.error("Viewer initialization failed:", err)
    }

    return () => {
      if (viewer) {
          try {
              viewer.dispose();
          } catch(e) {}
      }
      if (containerRef.current) {
          containerRef.current.innerHTML = '';
      }
    }
  }, [splatUrl])

  return (
    <div ref={containerRef} className="w-full h-full relative" style={{ minHeight: '500px' }} />
  )
}
