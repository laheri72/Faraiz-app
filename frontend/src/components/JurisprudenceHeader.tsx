import React from 'react';
import StepIndicator from './StepIndicator';
import { Home, Clock } from 'lucide-react';

interface Props {
    step: number;
    onHome: () => void;
    onHistory: () => void;
}

const JurisprudenceHeader: React.FC<Props> = ({ step, onHome, onHistory }) => {
    return (
        <header className="jurisprudence-header no-print" style={{ borderBottom: '1px solid var(--border-elegant)', paddingBottom: '1.5rem', marginBottom: '2rem' }}>
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-4">
                    <button 
                        className="p-2 hover:bg-gray-100 rounded-lg transition-colors border border-transparent hover:border-gray-200" 
                        onClick={onHome}
                        title="Dashboard Home"
                    >
                        <Home size={20} color="var(--primary)" />
                    </button>
                    <div>
                        <h1 className="serif" style={{ margin: 0, fontSize: '1.5rem', letterSpacing: '-0.02em' }}>Fatemi Wirasat Engine</h1>
                        <p className="subtitle" style={{ margin: 0, fontSize: '0.8rem', opacity: 0.7, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Deterministic Jurisprudence System</p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button 
                        className="flex items-center gap-2 px-3 py-2 hover:bg-gray-100 rounded-lg transition-colors border border-gray-200 text-sm font-medium" 
                        onClick={onHistory}
                    >
                        <Clock size={18} color="var(--primary)" />
                        <span className="hidden-mobile">History</span>
                    </button>
                </div>
            </div>
            {step > 0 && (
                <div style={{ marginTop: '1.5rem' }}>
                    <StepIndicator currentStep={step} />
                </div>
            )}
        </header>
    );
};

export default JurisprudenceHeader;
