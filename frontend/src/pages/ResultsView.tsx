import React from 'react';
import type { CalculationResult, VerificationData } from '../types';
import { BookOpen, CheckCircle, RotateCcw, ShieldCheck } from 'lucide-react';

interface Props {
    results: CalculationResult[];
    verification: VerificationData | null;
    onBack: () => void;
}

const ResultsView: React.FC<Props> = ({ results, verification, onBack }) => {
    return (
        <div className="animate-fade">
            <h2 className="section-title serif">
                <ShieldCheck size={22} color="var(--primary)" />
                Final Distribution Decree
            </h2>
            <p className="text-muted mb-4">
                The distribution below is based on the deterministic application of Fatemi Fiqh rules.
            </p>

            <div className="distribution-list">
                {results.map((res, i) => (
                    <div key={i} className="distribution-card animate-fade" style={{ animationDelay: `${i * 0.1}s` }}>
                        <div className="header">
                            <div>
                                <span className="relation">{res.relation}</span>
                                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Heir ID: {res.heir_id}</div>
                            </div>
                            <span className="share serif">{res.share}</span>
                        </div>
                        <div className="amount">
                            {res.amount.toLocaleString()} <small style={{ fontSize: '0.9rem', fontWeight: 'normal' }}>Units</small>
                        </div>
                        
                        {res.arabic_reasoning && res.arabic_reasoning.length > 0 && (
                            <div className="rule-box">
                                <h5 className="flex items-center gap-2">
                                    <BookOpen size={14} /> Jurisprudence Rule
                                </h5>
                                {res.arabic_reasoning.map((text, idx) => (
                                    <div key={idx} className="rule-item" style={{ marginBottom: '1rem' }}>
                                        <p className="arabic-text">{text}</p>
                                        <p style={{ fontSize: '0.85rem', color: 'var(--accent)', marginTop: '0.25rem' }}>
                                            {res.rules_used[idx] || "Constitutional Rule"}
                                        </p>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {verification && (
                <div className="verification-panel">
                    <h3 className="serif flex items-center justify-center gap-2">
                        <CheckCircle size={20} color="var(--success)" />
                        Verification Audit
                    </h3>
                    <div className="verification-grid">
                        <div className="v-item">
                            <span className="v-label">Net Estate</span>
                            <span className="v-value">{verification.estate_total.toLocaleString()}</span>
                        </div>
                        <div className="v-item">
                            <span className="v-label">Distributed</span>
                            <span className="v-value">{verification.total_distributed.toLocaleString()}</span>
                        </div>
                        <div className="v-item">
                            <span className="v-label">Fraction Sum</span>
                            <span className="v-value">{verification.fraction_sum}</span>
                        </div>
                    </div>
                    <div style={{ marginTop: '1.5rem', fontWeight: '800', color: verification.status === 'VALID' ? 'var(--success)' : 'var(--error)' }}>
                        SYSTEM STATUS: {verification.status}
                    </div>
                </div>
            )}

            <div className="flex justify-center mt-4">
                <button 
                    className="btn-outline flex items-center gap-2" 
                    onClick={onBack}
                >
                    <RotateCcw size={18} /> New Calculation
                </button>
            </div>
        </div>
    );
};

export default ResultsView;
