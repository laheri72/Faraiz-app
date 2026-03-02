import React from 'react';
import type { CalculationResult } from '../types';
import { User, ShieldOff, ChevronDown } from 'lucide-react';

interface Props {
    results: CalculationResult[];
}

const SummaryOverview: React.FC<Props> = ({ results }) => {
    const scrollToDetail = (id: string) => {
        const element = document.getElementById(`detail-${id}`);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    return (
        <div className="results-overview mb-4 animate-fade">
            <h3 className="section-title serif">
                <User size={20} /> Quick Overview
            </h3>
            
            <div className="overview-grid">
                {results.map((res, i) => (
                    <div 
                        key={i} 
                        className={`overview-card ${res.is_blocked ? 'blocked' : ''}`}
                        onClick={() => scrollToDetail(res.heir_id)}
                    >
                        <div className="card-top">
                            <span className="relation-name">{res.relation}</span>
                            <span className={`share-badge ${res.is_blocked ? 'blocked' : ''}`}>
                                {res.is_blocked ? 'Blocked' : res.share}
                            </span>
                        </div>
                        
                        {!res.is_blocked ? (
                            <div className="amount-display">
                                <span className="currency">Units</span>
                                <span className="value">{res.amount.toLocaleString()}</span>
                            </div>
                        ) : (
                            <div className="blocked-status">
                                <ShieldOff size={14} /> Mahjub
                            </div>
                        )}
                        
                        <div className="card-footer">
                            <span>View Details</span>
                            <ChevronDown size={14} />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default SummaryOverview;
