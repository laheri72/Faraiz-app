import React, { useState } from 'react';
import type { CalculationStep } from '../types';
import { Calculator, ChevronDown, ChevronUp } from 'lucide-react';

interface Props {
    steps: CalculationStep[];
}

const MathDistributionCard: React.FC<Props> = ({ steps }) => {
    const [isOpen, setIsOpen] = useState(false);

    // We only want the Mathematical Distribution step (usually step 3)
    const mathStep = steps.find(s => s.title.includes("MATHEMATICAL")) || steps[2];

    if (!mathStep) return null;

    return (
        <div className="math-card-wrapper mb-4">
            {/* Collapsed trigger bar */}
            <button
                className="math-card-trigger"
                onClick={() => setIsOpen(prev => !prev)}
                aria-expanded={isOpen}
            >
                <div className="math-card-trigger-left">
                    <Calculator size={18} />
                    <span className="math-card-trigger-title">Calculation Proof</span>
                    <span className="math-card-trigger-subtitle">Layered Engine Logic · {mathStep.items.length} steps</span>
                </div>
                <div className="math-card-trigger-right">
                    <span className="math-card-toggle-label">{isOpen ? 'Hide' : 'Show'}</span>
                    {isOpen ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                </div>
            </button>

            {/* Expandable body */}
            <div className={`math-card-body ${isOpen ? 'open' : ''}`}>
                <div className="math-card-content">
                    <div className="font-mono text-xs sm:text-sm space-y-3 bg-light p-4 rounded-xl border border-elegant">
                        {mathStep.items.map((item, i) => {
                            const hasEquals = item.includes(' = ');
                            const parts = hasEquals ? item.split(' = ') : [item, ''];
                            return (
                                <div key={i} className="math-step-row">
                                    <span className="math-step-label">{parts[0]}</span>
                                    {parts[1] && (
                                        <span className="math-step-value">{parts[1]}</span>
                                    )}
                                </div>
                            );
                        })}
                    </div>

                    <p className="math-card-footnote">
                        This distribution follows Fatemi Wirasat principles: 1. Biological Proximity (Blocking),
                        2. Qur'anic Fixed Portions (Fara'id), 3. Proportional Return (Radd).
                    </p>
                </div>
            </div>
        </div>
    );
};

export default MathDistributionCard;
