import React from 'react';
import type { CalculationResult } from '../types';
import RuleExplanation from './RuleExplanation';
import { ShieldOff } from 'lucide-react';

interface Props {
    results: CalculationResult[];
}

const ResultsTable: React.FC<Props> = ({ results }) => {
    return (
        <div className="distribution-list">
            {results.map((res, i) => (
                <div 
                    key={i} 
                    id={`detail-${res.heir_id}`}
                    className="distribution-card animate-fade" 
                    style={{ 
                        animationDelay: `${i * 0.1}s`, 
                        opacity: res.is_blocked ? 0.7 : 1,
                        scrollMarginTop: '2rem'
                    }}
                >
                    <div className="header">
                        <div>
                            <span className="relation">{res.relation}</span>
                            <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>Heir ID: {res.heir_id}</div>
                        </div>
                        <span className={`share serif ${res.is_blocked ? 'blocked-label' : ''}`}>
                            {res.is_blocked ? 'MAHJUB' : res.share}
                        </span>
                    </div>
                    
                    {!res.is_blocked ? (
                        <div className="amount">
                            {res.amount.toLocaleString()} <small style={{ fontSize: '0.9rem', fontWeight: 'normal' }}>Units</small>
                        </div>
                    ) : (
                        <div className="blocking-info" style={{ color: 'var(--error)', fontWeight: '600', display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                            <ShieldOff size={16} />
                            Blocked by {res.blocked_by || 'Superior Heir'}
                        </div>
                    )}
                    
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
