import React from 'react';
import type { CalculationResult } from '../types';
import RuleExplanation from './RuleExplanation';

interface Props {
    results: CalculationResult[];
}

const ResultsTable: React.FC<Props> = ({ results }) => {
    return (
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
                    
                    <RuleExplanation 
                        rules={res.rules_used} 
                        reasoning={res.arabic_reasoning} 
                    />
                </div>
            ))}
        </div>
    );
};

export default ResultsTable;
