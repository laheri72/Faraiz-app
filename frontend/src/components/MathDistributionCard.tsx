import React from 'react';
import type { CalculationStep } from '../types';
import { Calculator, ArrowRight } from 'lucide-react';

interface Props {
    steps: CalculationStep[];
}

const MathDistributionCard: React.FC<Props> = ({ steps }) => {
    // We only want the Mathematical Distribution step (usually step 3)
    const mathStep = steps.find(s => s.title.includes("MATHEMATICAL")) || steps[2];

    if (!mathStep) return null;

    return (
        <div className="card mb-8 overflow-hidden border-primary shadow-lg" style={{ borderLeftWidth: '6px' }}>
            <div className="bg-primary text-white p-4 sm:p-5 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <Calculator size={24} className="flex-shrink-0" />
                    <h3 className="serif text-white m-0 text-lg sm:text-xl">Mathematical Distribution</h3>
                </div>
                <div className="hidden sm:block text-xs opacity-80 font-mono">Layered Engine Logic</div>
            </div>
            
            <div className="p-4 sm:p-6 lg:p-8">
                <div>
                    {/* Math Steps Column */}
                    <div className="animate-fade">
                        <h4 className="serif border-b pb-2 mb-4 flex items-center gap-2 text-primary font-bold">
                            <ArrowRight size={18} className="text-gold" />
                            Calculation Steps
                        </h4>
                        <div className="font-mono text-xs sm:text-sm space-y-3 bg-light p-4 rounded-xl border border-elegant shadow-inner">
                            {mathStep.items.map((item, i) => {
                                const hasEquals = item.includes(' = ');
                                const parts = hasEquals ? item.split(' = ') : [item, ''];
                                return (
                                    <div key={i} className="flex flex-col xs:flex-row justify-between gap-1 xs:gap-4 border-b border-dashed border-elegant pb-2 last:border-0">
                                        <span className="text-muted truncate">{parts[0]}</span>
                                        <span className="font-bold text-primary xs:text-right">{parts[1]}</span>
                                    </div>
                                );
                            })}
                        </div>
                    </div>
                </div>
                
                <div className="mt-8 pt-4 border-t border-elegant text-center">
                    <p className="text-muted italic text-[10px] sm:text-xs leading-relaxed max-w-lg mx-auto">
                        This distribution follows Fatemi Wirasat principles: 1. Biological Proximity (Blocking), 
                        2. Qur'anic Fixed Portions (Fara'id), 3. Proportional Return (Radd).
                    </p>
                </div>
            </div>
        </div>
    );
};

export default MathDistributionCard;
