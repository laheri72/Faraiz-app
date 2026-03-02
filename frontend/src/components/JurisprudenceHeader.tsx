import React from 'react';
import StepIndicator from './StepIndicator';

interface Props {
    step: number;
}

const JurisprudenceHeader: React.FC<Props> = ({ step }) => {
    return (
        <header className="jurisprudence-header">
            <div className="flex items-center justify-center gap-4">
                <h1 className="serif" style={{ margin: 0 }}>Fatemi Wirasat Engine</h1>
                <span className="serif" style={{ fontSize: '2rem', color: 'var(--gold)', opacity: 0.8 }}>فقه المواريث</span>
            </div>
            <p className="subtitle">Deterministic Inheritance Calculation according to Fatemi Fiqh</p>
            {step > 0 && <StepIndicator currentStep={step} />}
        </header>
    );
};

export default JurisprudenceHeader;
