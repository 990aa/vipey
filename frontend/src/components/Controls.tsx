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
      padding: '20px', 
      borderTop: '1px solid #ccc',
      display: 'flex',
      flexDirection: 'column',
      gap: '10px'
    }}>
      <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', alignItems: 'center' }}>
        <button onClick={handlePrevious} disabled={currentStep === 0}>
          Previous
        </button>
        <button onClick={onPlayPause}>
          {isPlaying ? 'Pause' : 'Play'}
        </button>
        <button onClick={handleNext} disabled={currentStep === totalSteps - 1}>
          Next
        </button>
      </div>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <span>Step {currentStep + 1} of {totalSteps}</span>
        <input
          type="range"
          min="0"
          max={totalSteps - 1}
          value={currentStep}
          onChange={(e) => onStepChange(parseInt(e.target.value))}
          style={{ flex: 1 }}
        />
      </div>
    </div>
  );
};
