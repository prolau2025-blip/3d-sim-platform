import React, { useRef, useEffect } from 'react'

export default function SplatViewer({ splatUrl }) {
  const containerRef = useRef(null)

  useEffect(() => {
    let viewer = null
    let mounted = true

    import('@mkkellogg/gaussian-splats-3d').then((GaussianSplats3D) => {
      if (!containerRef.current || !mounted) return
      
      viewer = new GaussianSplats3D.Viewer({
        selfDrivenMode: true,
        useWebXR: false,
        rootElement: containerRef.current,
        cameraUp: [0, -1, 0],
        initialCameraPosition: [0, 2, 5],
        initialCameraLookAt: [0, 0, 0]
      })

      viewer.addSplatScene(splatUrl, {
        splatAlphaCrop: 0.1,
      })
      .then(() => {
        if (mounted) {
          viewer.start()
        }
      })
      .catch((err) => {
          console.error("Failed to load splat scene:", err);
      });
    }).catch(err => {
        console.error("Failed to import gaussian-splats-3d", err);
    })

    return () => {
      mounted = false
      if (viewer) {
          // Attempt to dispose if viewer has a dispose method
          try {
              if (viewer.dispose) viewer.dispose();
          } catch(e) {}
      }
    }
  }, [splatUrl])

  return (
    <div ref={containerRef} className="w-full h-full relative" />
  )
}
