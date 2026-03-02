import React from 'react';

interface Props {
    currentStep: number;
}

const StepIndicator: React.FC<Props> = ({ currentStep }) => {
    const steps = ['Estate', 'Heirs', 'Summary', 'Results'];
    
    return (
        <div className="step-indicator" style={{ marginTop: '2rem' }}>
            {steps.map((label, i) => {
                const stepNum = i + 1;
                const isActive = stepNum === currentStep;
                const isCompleted = stepNum < currentStep;
                
                return (
                    <div 
                        key={label} 
                        className={`step ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}
                        title={label}
                    >
                        {isCompleted ? '✓' : stepNum}
                    </div>
                );
            })}
        </div>
    );
};

export default StepIndicator;
