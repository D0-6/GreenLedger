"use client";

import { useEffect, useRef } from "react";
import createGlobe from "cobe";

export default function CobeGlobe() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    let phi = 0;
    
    if (!canvasRef.current) return;

    const globe = createGlobe(canvasRef.current, {
      devicePixelRatio: 2,
      width: 1200,
      height: 1200,
      phi: 0,
      theta: 0.1,
      dark: 1,
      diffuse: 1.2,
      mapSamples: 16000,
      mapBrightness: 3,
      baseColor: [0.1, 0.1, 0.15],
      markerColor: [0, 0.95, 1], // Cyan markers for active nodes
      glowColor: [0.05, 0.1, 0.15],
      markers: [
        // London, NYC, Tokyo, Sydney (representing global tracking nodes)
        { location: [51.5072, 0.1276], size: 0.08 },
        { location: [40.7128, -74.0060], size: 0.08 },
        { location: [35.6762, 139.6503], size: 0.05 },
        { location: [-33.8688, 151.2093], size: 0.06 },
        { location: [-23.5505, -46.6333], size: 0.05 }, // Brazil (Amazon tracking)
      ],
      onRender: (state: any) => {
        // Called on every animation frame.
        // `state` will be an empty object, return updated params.
        state.phi = phi;
        phi += 0.003; // Rotation speed
      },
    } as any);

    return () => {
      globe.destroy();
    };
  }, []);

  return (
    <div className="absolute inset-0 w-full h-full flex items-center justify-center opacity-60 mix-blend-screen pointer-events-none z-0 overflow-hidden">
      <div style={{ width: '1200px', height: '1200px' }}>
        <canvas
          ref={canvasRef}
          style={{ width: 1200, height: 1200, opacity: 0 }}
          className="transition-opacity duration-1000 ease-in-out globe-canvas"
          onAnimationEnd={(e) => {
            (e.target as HTMLElement).style.opacity = '1';
          }}
        />
      </div>
      {/* Fallback CSS for fade-in since canvas doesn't emit onAnimationEnd inherently unless we attach a keyframe. 
          A simple inline hack: */}
      <style>{`
        .globe-canvas {
          animation: fade-in 2s forwards;
        }
        @keyframes fade-in {
          0% { opacity: 0; }
          100% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}
