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
  function_name?: string;
  time_complexity?: {
    big_o: string;
    explanation: string;
    patterns: string[];
    confidence: string;
  };
}

interface ProjectData {
  metrics?: any;
  advanced_report?: any;
  nextgen_report?: any;
  dependencies?: any;
  git_history?: any;
}

type TabName = 'visualization' | 'analysis' | 'documentation';

const App: React.FC = () => {
  const [storyboard, setStoryboard] = useState<StoryboardData | null>(null);
  const [projectData, setProjectData] = useState<ProjectData | null>(null);
  const [documentation, setDocumentation] = useState<string>('');
  const [currentStep, setCurrentStep] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [activeTab, setActiveTab] = useState<TabName>('visualization');

  useEffect(() => {
    // Fetch data from API endpoints
    const fetchData = async () => {
      try {
        // Get storyboard data
        const storyboardRes = await fetch('/api/storyboard');
        if (storyboardRes.ok) {
          const data = await storyboardRes.json();
          setStoryboard(data);
        }
      } catch (error) {
        console.error('Failed to load storyboard:', error);
      }

      try {
        // Get project analysis data
        const projectRes = await fetch('/api/project');
        if (projectRes.ok) {
          const data = await projectRes.json();
          setProjectData(data);
        }
      } catch (error) {
        console.error('Failed to load project data:', error);
      }

      try {
        // Get documentation
        const docsRes = await fetch('/api/documentation');
        if (docsRes.ok) {
          const text = await docsRes.text();
          setDocumentation(text);
        }
      } catch (error) {
        console.error('Failed to load documentation:', error);
      }
    };

    fetchData();
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

  const currentFrame = storyboard?.frames[currentStep];

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🎯 Vipey - Code Intelligence Platform</h1>
        <div className="status-indicator">
          <span className="status-dot"></span>
          <span>Live Dashboard</span>
        </div>
      </header>

      <div className="tabs">
        <button
          className={`tab ${activeTab === 'visualization' ? 'active' : ''}`}
          onClick={() => setActiveTab('visualization')}
        >
          📊 Visualization
        </button>
        <button
          className={`tab ${activeTab === 'analysis' ? 'active' : ''}`}
          onClick={() => setActiveTab('analysis')}
        >
          📈 Project Analysis
        </button>
        <button
          className={`tab ${activeTab === 'documentation' ? 'active' : ''}`}
          onClick={() => setActiveTab('documentation')}
        >
          📚 Documentation
        </button>
      </div>

      <div className="tab-content">
        {activeTab === 'visualization' && (
          <div className="visualization-tab">
            {storyboard ? (
              <>
                {storyboard.time_complexity && (
                  <div className="complexity-card">
                    <h3>⏱️ Time Complexity Analysis</h3>
                    <div className="complexity-value">{storyboard.time_complexity.big_o}</div>
                    <p className="complexity-explanation">{storyboard.time_complexity.explanation}</p>
                    {storyboard.time_complexity.patterns.length > 0 && (
                      <div className="complexity-patterns">
                        {storyboard.time_complexity.patterns.map((pattern, idx) => (
                          <span key={idx} className="badge badge-info">{pattern}</span>
                        ))}
                      </div>
                    )}
                    <div className="complexity-confidence">
                      <span className={`badge badge-${storyboard.time_complexity.confidence}`}>
                        Confidence: {storyboard.time_complexity.confidence}
                      </span>
                    </div>
                  </div>
                )}

                <div className="execution-info">
                  <div className="info-item">
                    <span className="info-label">Function:</span>
                    <code>{storyboard.function_name || 'unknown'}</code>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Total Frames:</span>
                    <span className="info-value">{storyboard.frames.length}</span>
                  </div>
                  <div className="info-item">
                    <span className="info-label">Return Value:</span>
                    <code>{JSON.stringify(storyboard.return_value)}</code>
                  </div>
                </div>

                <div className="visualization-grid">
                  <div className="code-section">
                    <h2>📝 Source Code</h2>
                    <CodePane
                      code={storyboard.source_code || "# No source code available"}
                      highlightLine={currentFrame?.line || 0}
                    />
                  </div>
                  <div className="variables-section">
                    <h2>🔍 Variables</h2>
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
              </>
            ) : (
              <div className="loading">Loading visualization data...</div>
            )}
          </div>
        )}

        {activeTab === 'analysis' && (
          <div className="analysis-tab">
            {projectData ? (
              <div dangerouslySetInnerHTML={{ __html: projectData as any }} />
            ) : (
              <div className="loading">Loading analysis data...</div>
            )}
          </div>
        )}

        {activeTab === 'documentation' && (
          <div className="documentation-tab">
            {documentation ? (
              <div className="doc-content" dangerouslySetInnerHTML={{ __html: documentation }} />
            ) : (
              <div className="loading">Loading documentation...</div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
