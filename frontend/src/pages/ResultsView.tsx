import React from 'react';
import type { CalculationResult, VerificationData } from '../types';
import { Book, Landmark, CheckCircle, AlertTriangle } from 'lucide-react';

interface Props {
    results: CalculationResult[];
    verification: VerificationData | null;
    onBack: () => void;
}

const ResultsView: React.FC<Props> = ({ results, verification, onBack }) => {
    return (
        <div className="container results-view">
            <h1 className="title">Distribution Results</h1>
            <p className="subtitle">Individual shares calculated with 100% mathematical precision.</p>

            {verification && (
                <div className={`verification-banner ${verification.status.toLowerCase()}`}>
                    <div className="banner-main">
                        {verification.status === 'VALID' ? <CheckCircle size={20} /> : <AlertTriangle size={20} />}
                        <span>Distribution Integrity: <strong>{verification.status}</strong></span>
                    </div>
                    <div className="banner-details">
                        <span>Estate: {verification.estate_total.toLocaleString()}</span>
                        <span>Distributed: {verification.total_distributed.toLocaleString()}</span>
                        <span>Sum: {verification.fraction_sum}</span>
                    </div>
                </div>
            )}
            
            <div className="results-grid">
                {results.map((res) => (
                    <div key={res.heir_id} className="result-card">
                        <div className="header">
                            <span className="relation">{res.relation} <small className="heir-id">#{res.heir_id.split('_')[1]}</small></span>
                            <span className="share-tag">{res.share}</span>
                        </div>
                        <div className="amount-section">
                            <Landmark size={20} className="icon" />
                            <span className="amount">{res.amount.toLocaleString()}</span>
                        </div>
                        <div className="reasoning-section">
                            <h4><Book size={16} /> Jurisprudence Basis</h4>
                            <div className="arabic-list">
                                {res.arabic_reasoning.map((text, i) => (
                                    <p key={i} className="arabic-text" dir="rtl">{text}</p>
                                ))}
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <div className="footer-actions">
                <button className="primary-btn" onClick={onBack}>New Calculation</button>
            </div>
        </div>
    );
};

export default ResultsView;
