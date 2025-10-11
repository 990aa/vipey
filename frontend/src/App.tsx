// App.tsx
import React, { useState, useEffect } from 'react';
import { CodePane } from './components/CodePane';
import { Controls } from './components/Controls';
import { VisualizationPane } from './components/VisualizationPane';

interface Frame {
  line: number;
  event_type: string;
  locals: Record<string, any>;
}

interface StoryboardData {
  frames: Frame[];
  return_value: any;
  source_code?: string;
}

const App: React.FC = () => {
  const [storyboard, setStoryboard] = useState<StoryboardData | null>(null);
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);

  useEffect(() => {
    // Load storyboard data from the injected script tag
    const dataElement = document.getElementById('storyboard-data');
    if (dataElement && dataElement.textContent) {
      try {
        const data = JSON.parse(dataElement.textContent);
        setStoryboard(data);
      } catch (error) {
        console.error('Failed to parse storyboard data:', error);
      }
    }
  }, []);

  useEffect(() => {
    let interval: number | undefined;
    if (isPlaying && storyboard) {
      interval = window.setInterval(() => {
        setCurrentStep((prev) => {
          if (prev >= storyboard.frames.length - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, 500);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying, storyboard]);

  if (!storyboard) {
    return <div>Loading...</div>;
  }

  const currentFrame = storyboard.frames[currentStep];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100vh' }}>
      <h1 style={{ textAlign: 'center', margin: '10px 0' }}>Vipey Visualization</h1>
      <div style={{ display: 'flex', flex: 1, overflow: 'hidden' }}>
        <div style={{ flex: 1, overflow: 'auto', borderRight: '1px solid #ccc', padding: '10px' }}>
          <h2>Code</h2>
          <CodePane 
            code={storyboard.source_code || "# No source code available"} 
            highlightLine={currentFrame?.line || 0} 
          />
        </div>
        <div style={{ flex: 1, overflow: 'auto', padding: '10px' }}>
          <h2>Variables</h2>
          <VisualizationPane variable={currentFrame?.locals} />
        </div>
      </div>
      <Controls
        currentStep={currentStep}
        totalSteps={storyboard.frames.length}
        isPlaying={isPlaying}
        onStepChange={setCurrentStep}
        onPlayPause={() => setIsPlaying(!isPlaying)}
      />
    </div>
  );
};

export default App;
