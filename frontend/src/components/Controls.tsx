// Controls.tsx
import React from 'react';

interface ControlsProps {
  currentStep: number;
  totalSteps: number;
  isPlaying: boolean;
  onStepChange: (step: number) => void;
  onPlayPause: () => void;
}

export const Controls: React.FC<ControlsProps> = ({
  currentStep,
  totalSteps,
  isPlaying,
  onStepChange,
  onPlayPause,
}) => {
  const handlePrevious = () => {
    if (currentStep > 0) {
      onStepChange(currentStep - 1);
    }
  };

  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      onStepChange(currentStep + 1);
    }
  };

  return (
    <div style={{ 
      padding: '25px', 
      background: '#e3f2fd',
      borderRadius: '8px',
      border: '1px solid #64b5f6',
      display: 'flex',
      flexDirection: 'column',
      gap: '15px',
      boxShadow: '0 4px 8px rgba(21, 101, 192, 0.2)'
    }}>
      <div style={{ display: 'flex', gap: '12px', justifyContent: 'center', alignItems: 'center' }}>
        <button onClick={handlePrevious} disabled={currentStep === 0}>
          ⏮️ Previous
        </button>
        <button onClick={onPlayPause} style={{
          background: isPlaying ? 'linear-gradient(135deg, #e74c3c 0%, #c0392b 100%)' : 'linear-gradient(135deg, #2ecc71 0%, #27ae60 100%)',
          color: 'white',
          border: 'none',
          padding: '12px 24px',
          fontSize: '15px',
          fontWeight: 'bold',
          boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)'
        }}>
          {isPlaying ? '⏸️ Pause' : '▶️ Play'}
        </button>
        <button onClick={handleNext} disabled={currentStep === totalSteps - 1}>
          Next ⏭️
        </button>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '15px', color: '#1a237e' }}>
        <span style={{ fontWeight: 600, minWidth: '120px', fontSize: '15px' }}>
          Step {currentStep + 1} of {totalSteps}
        </span>
        <input
          type="range"
          min="0"
          max={totalSteps - 1}
          value={currentStep}
          onChange={(e) => onStepChange(parseInt(e.target.value))}
          style={{ 
            flex: 1,
            height: '8px',
            borderRadius: '4px',
            outline: 'none',
            background: '#90caf9',
            cursor: 'pointer'
          }}
        />
      </div>
    </div>
  );
};
