import React from 'react';
import type { CalculationResult } from '../types';
import { Book, Landmark } from 'lucide-react';

interface Props {
    results: CalculationResult[];
    onBack: () => void;
}

const ResultsView: React.FC<Props> = ({ results, onBack }) => {
    return (
        <div className="container results-view">
            <h1 className="title">Distribution Results</h1>
            <p className="subtitle">The following shares have been calculated based on Daim al-Islam jurisprudence.</p>
            
            <div className="results-grid">
                {results.map((res, index) => (
                    <div key={index} className="result-card">
                        <div className="header">
                            <span className="relation">{res.heir}</span>
                            <span className="share-tag">{res.share}</span>
                        </div>
                        <div className="amount-section">
                            <Landmark size={20} className="icon" />
                            <span className="amount">{res.amount.toLocaleString()}</span>
                        </div>
                        <div className="reasoning-section">
                            <h4><Book size={16} /> Legal Reasoning</h4>
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
