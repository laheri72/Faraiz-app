import React from 'react';
import type { CalculationResult, VerificationData } from '../types';
import { RotateCcw, ShieldCheck } from 'lucide-react';
import ResultsTable from '../components/ResultsTable';
import VerificationPanel from '../components/VerificationPanel';
import SummaryOverview from '../components/SummaryOverview';

interface Props {
    results: CalculationResult[];
    verification: VerificationData | null;
    onBack: () => void;
}

const ResultsDisplay: React.FC<Props> = ({ results, verification, onBack }) => {
    return (
        <div className="animate-fade">
            <div className="page-statement">
                <h2 className="serif">
                    <ShieldCheck size={22} color="var(--primary)" style={{ verticalAlign: 'middle', marginRight: '0.5rem' }} />
                    Final Distribution Decree
                </h2>
                <p>The distribution below is based on the deterministic application of Fatemi Fiqh rules.</p>
            </div>

            <SummaryOverview results={results} />

            <div className="section-title serif mt-4" style={{ marginBottom: '1.5rem' }}>
                Full Distribution Breakdown
            </div>

            <ResultsTable results={results} />

            {verification && <VerificationPanel verification={verification} />}

            <div className="action-area" style={{ justifyContent: 'center' }}>
                <button className="btn-outline flex items-center gap-2" onClick={onBack}>
                    <RotateCcw size={18} /> New Calculation
                </button>
            </div>
        </div>
    );
};

export default ResultsDisplay;
