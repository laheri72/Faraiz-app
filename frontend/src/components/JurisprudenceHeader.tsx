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
        <header className="jurisprudence-header no-print" style={{ borderBottom: '1px solid var(--border-elegant)', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
            <div className="flex justify-between items-center">
                <div className="flex items-center gap-3 md:gap-4">
                    <button
                        className="p-1.5 md:p-2 hover:bg-gray-100 rounded-lg transition-colors border border-transparent hover:border-gray-200"
                        onClick={onHome}
                        title="Dashboard Home"
                    >
                        <Home size={18} color="var(--primary)" className="md:w-5 md:h-5" />
                    </button>
                    <div>
                        <h1 className="serif" style={{ margin: 0, fontSize: 'clamp(1.1rem, 4vw, 1.4rem)', letterSpacing: '-0.01em', lineHeight: 1.2 }}>Fatemi Wirasat Engine</h1>
                        <p className="subtitle" style={{ margin: 0, fontSize: 'clamp(0.85rem, 3vw, 1rem)', opacity: 0.8, fontFamily: "'Amiri', serif" }}>مستبصرا من كتب الفقه الفاطمي</p>
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button
                        className="flex items-center gap-2 px-2.5 py-1.5 md:px-3 md:py-2 hover:bg-gray-100 rounded-lg transition-colors border border-gray-200 text-xs md:text-sm font-medium"
                        onClick={onHistory}
                    >
                        <Clock size={16} color="var(--primary)" className="md:w-4.5 md:h-4.5" />
                        <span className="hidden-mobile">History</span>
                    </button>
                </div>
            </div>
            {step > 0 && (
                <div style={{ marginTop: '0.75rem' }}>
                    <StepIndicator currentStep={step} />
                </div>
            )}
        </header>
    );
};

export default JurisprudenceHeader;
