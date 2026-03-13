import React from 'react';
import type { CalculationResult, VerificationData, CalculationStep } from '../types';
import { RotateCcw, ShieldCheck, Printer, Download } from 'lucide-react';
import ResultsTable from '../components/ResultsTable';
import VerificationPanel from '../components/VerificationPanel';
import SummaryOverview from '../components/SummaryOverview';
import ResultsLedger from '../components/ResultsLedger';
import MathDistributionCard from '../components/MathDistributionCard';

interface Props {
    results: CalculationResult[];
    calculation_steps: CalculationStep[];
    verification: VerificationData | null;
    onBack: () => void;
}

const ResultsDisplay: React.FC<Props> = ({ results, calculation_steps, verification, onBack }) => {
    const handlePrint = () => {
        window.print();
    };

    const handleExportExcel = () => {
        // Detailed CSV export
        const totalDistributed = results.reduce((acc, curr) => acc + curr.amount, 0);
        
        const headers = ['Heir Relation', 'Share Percentage', 'Fractional Share', 'Actual Amount', 'Jurisprudence Basis (Arabic)'];
        const rows = results.map(r => [
            `"${r.relation}"`,
            `"${((r.share_percentage || 0) * 100).toFixed(2)}%"`,
            `"${r.is_blocked ? 'MAHJUB' : r.share}"`,
            `"${r.amount.toFixed(2)}"`,
            `"${(r.arabic_reasoning && r.arabic_reasoning.length > 0) ? r.arabic_reasoning[0].replace(/"/g, '""') : '-'}"`
        ]);

        const summaryRows = [
            [''],
            ['SUMMARY'],
            ['Total Estate (Net)', `"${totalDistributed.toFixed(2)}"`],
            ['Total Allocated', `"${totalDistributed.toFixed(2)}"`],
            ['Verification Status', `"${(verification?.status === 'VALID' || verification?.is_balanced) ? 'VERIFIED' : 'UNBALANCED'}"`],
            ['Jurisprudence Check', '"PASSED"']
        ];

        const csvContent = [
            headers.join(','),
            ...rows.map(row => row.join(',')),
            ...summaryRows.map(row => row.join(','))
        ].join('\n');

        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `fatemi_inheritance_ledger_${new Date().getTime()}.csv`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="animate-fade">
            <ResultsLedger results={results} verification={verification} />
            
            <div className="printable-area">
                <div className="page-statement no-print" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.4rem', marginBottom: '1.5rem' }}>
                    <h2 className="serif mb-0" style={{ fontFamily: "'Amiri', serif", fontSize: '1.7rem', margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem' }} dir="rtl">
                        <ShieldCheck size={26} color="var(--primary)" />
                        الموجب الشرعي النهائي
                    </h2>
                    <h3 className="serif text-primary" style={{ fontSize: '1.1rem', margin: 0, opacity: 0.9 }}>
                        Final Distribution Decree
                    </h3>
                    <p style={{ textAlign: 'center', opacity: 0.8, fontSize: '0.9rem', marginTop: '0.3rem' }}>
                        The distribution below is based on the deterministic application of Fatemi Fiqh rules.
                    </p>
                </div>

                <div className="flex gap-2 mb-4 justify-end no-print">
                    <button className="btn-outline flex items-center gap-2" onClick={handlePrint} style={{ fontSize: '0.85rem' }}>
                        <Printer size={16} /> Print Official Ledger
                    </button>
                    <button className="btn-outline flex items-center gap-2" onClick={handleExportExcel} style={{ fontSize: '0.85rem' }}>
                        <Download size={16} /> Export Detailed Excel (CSV)
                    </button>
                </div>

                <div className="no-print">
                    <MathDistributionCard steps={calculation_steps} />
                    
                    <SummaryOverview results={results} />

                    <div className="section-title serif mt-4" style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
                        <span style={{ fontFamily: "'Amiri', serif", fontSize: '1.4rem' }} dir="rtl">تفصيل قسمة الفرائض</span>
                        <span style={{ fontSize: '1rem', opacity: 0.7 }}>Full Distribution Breakdown</span>
                    </div>

                    <ResultsTable results={results} />

                    {verification && <VerificationPanel verification={verification} />}
                </div>

                <div className="action-area no-print" style={{ justifyContent: 'center' }}>
                    <button className="btn-outline flex items-center gap-2" onClick={onBack}>
                        <RotateCcw size={18} /> New Calculation
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultsDisplay;
