import React from 'react';
import type { CalculationResult } from '../types';
import { ShieldOff } from 'lucide-react';

interface Props {
    results: CalculationResult[];
    currency?: string;
}

// Same palette as DistributionPieChart for consistency
const PALETTE = [
    '#064e3b', '#d4af37', '#065f46', '#78350f', '#b45309',
    '#047857', '#92400e', '#059669', '#f59e0b', '#10b981',
    '#c2410c', '#34d399',
];

const HeirAnchorStrip: React.FC<Props> = ({ results, currency = '₹' }) => {
    const scrollToDetail = (id: string) => {
        const element = document.getElementById(`detail-${id}`);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    const activeHeirs = results.filter(r => !r.is_blocked);
    const blockedHeirs = results.filter(r => r.is_blocked);
    const maxAmount = activeHeirs.length > 0 ? Math.max(...activeHeirs.map(r => r.amount)) : 1;

    let colorIdx = 0;

    return (
        <div className="heir-anchor-wrapper mb-4">
            <div className="heir-anchor-label">
                <span className="heir-anchor-label-text">↓ Jump to Heir</span>
                <span className="heir-anchor-label-count">{results.length} heirs in this distribution</span>
            </div>

            <div className="heir-anchor-strip">
                {activeHeirs.map((res) => {
                    const color = PALETTE[colorIdx % PALETTE.length];
                    colorIdx++;
                    const opacity = 0.35 + 0.65 * (res.amount / maxAmount);

                    return (
                        <button
                            key={res.heir_id}
                            className="heir-anchor-pill"
                            onClick={() => scrollToDetail(res.heir_id)}
                            style={{
                                '--pill-color': color,
                                '--pill-opacity': opacity,
                            } as React.CSSProperties}
                            title={`${res.relation} · ${((res.share_percentage || 0) * 100).toFixed(1)}% · ${currency} ${res.amount.toLocaleString()}`}
                        >
                            <span className="heir-pill-dot" style={{ background: color }} />
                            <div className="heir-pill-info">
                                <span className="heir-pill-name">{res.relation}</span>
                                <span className="heir-pill-amount">{currency} {res.amount.toLocaleString()}</span>
                            </div>
                            <span className="heir-pill-share">{res.share}</span>
                        </button>
                    );
                })}

                {blockedHeirs.map((res) => (
                    <button
                        key={res.heir_id}
                        className="heir-anchor-pill blocked"
                        onClick={() => scrollToDetail(res.heir_id)}
                        title={`${res.relation} · Mahjub (Blocked)`}
                    >
                        <ShieldOff size={11} style={{ flexShrink: 0, color: '#9ca3af' }} />
                        <div className="heir-pill-info">
                            <span className="heir-pill-name">{res.relation}</span>
                            <span className="heir-pill-amount blocked-label">Mahjub</span>
                        </div>
                    </button>
                ))}
            </div>
        </div>
    );
};

export default HeirAnchorStrip;
