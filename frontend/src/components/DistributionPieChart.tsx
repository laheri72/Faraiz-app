import React, { useState } from 'react';
import type { CalculationResult } from '../types';

interface Props {
    results: CalculationResult[];
    currency?: string;
}

// Curated palette matching the emerald/gold theme
const PALETTE = [
    '#064e3b', // primary emerald
    '#d4af37', // gold
    '#065f46', // primary-light
    '#78350f', // secondary amber
    '#b45309', // accent amber
    '#047857', // emerald 700
    '#92400e', // amber 800
    '#059669', // emerald 600
    '#f59e0b', // amber 400
    '#10b981', // emerald 500
    '#c2410c', // orange 700
    '#34d399', // emerald 400
];

const BLOCKED_COLOR = '#d1d5db'; // gray for blocked heirs

interface SliceData {
    relation: string;
    percentage: number;
    amount: number;
    share: string;
    is_blocked: boolean;
    color: string;
    startAngle: number;
    endAngle: number;
}

function polarToCartesian(cx: number, cy: number, r: number, angleDeg: number) {
    const rad = ((angleDeg - 90) * Math.PI) / 180;
    return {
        x: cx + r * Math.cos(rad),
        y: cy + r * Math.sin(rad),
    };
}



function buildSlices(results: CalculationResult[]): SliceData[] {
    const total = results.reduce((s, r) => s + (r.is_blocked ? 0 : r.amount), 0);
    let currentAngle = 0;
    let colorIdx = 0;
    return results.map(r => {
        const pct = total > 0 && !r.is_blocked ? (r.amount / total) : 0;
        const sweep = pct * 360;
        const slice: SliceData = {
            relation: r.relation,
            percentage: r.is_blocked ? 0 : parseFloat(((r.share_percentage || 0) * 100).toFixed(2)),
            amount: r.amount,
            share: r.share,
            is_blocked: r.is_blocked,
            color: r.is_blocked ? BLOCKED_COLOR : PALETTE[colorIdx % PALETTE.length],
            startAngle: currentAngle,
            endAngle: currentAngle + sweep,
        };
        if (!r.is_blocked) colorIdx++;
        currentAngle += sweep;
        return slice;
    });
}

const DistributionPieChart: React.FC<Props> = ({ results, currency = '₹' }) => {
    const [hovered, setHovered] = useState<number | null>(null);

    const activeResults = results.filter(r => !r.is_blocked);
    const blockedResults = results.filter(r => r.is_blocked);
    const totalAmount = results.reduce((s, r) => s + r.amount, 0);
    const slices = buildSlices(results);

    const CX = 130, CY = 130, R = 100, INNER_R = 58;
    const GAP = 2.5; // gap between slices in degrees

    if (results.length === 0) return null;

    const hoveredSlice = hovered !== null ? slices[hovered] : null;

    return (
        <div className="dist-chart-wrapper no-print">
            {/* Glassmorphism card */}
            <div className="dist-chart-card">
                {/* Header */}
                <div className="dist-chart-header">
                    <div className="dist-chart-title-group">
                        <span className="dist-chart-arabic" dir="rtl">توزيع التركة</span>
                        <span className="dist-chart-subtitle">Estate Distribution at a Glance</span>
                    </div>
                    <div className="dist-chart-badge">
                        <span>{activeResults.length} Heir{activeResults.length !== 1 ? 's' : ''}</span>
                        {blockedResults.length > 0 && (
                            <span className="dist-chart-badge-blocked">{blockedResults.length} Blocked</span>
                        )}
                    </div>
                </div>

                {/* Body: chart + legend */}
                <div className="dist-chart-body">
                    {/* SVG Donut */}
                    <div className="dist-chart-svg-wrapper">
                        <svg
                            viewBox="0 0 260 260"
                            width="260"
                            height="260"
                            className="dist-chart-svg"
                            onMouseLeave={() => setHovered(null)}
                        >
                            {/* Outer glow ring */}
                            <circle cx={CX} cy={CY} r={R + 12} fill="none" stroke="rgba(212,175,55,0.15)" strokeWidth="20" />
                            <circle cx={CX} cy={CY} r={R + 4} fill="none" stroke="rgba(212,175,55,0.08)" strokeWidth="6" />

                            {/* Slices */}
                            {slices.map((slice, i) => {
                                if (slice.is_blocked) return null;
                                const isHov = hovered === i;
                                const gapStart = slice.startAngle + GAP / 2;
                                const gapEnd = slice.endAngle - GAP / 2;
                                if (gapEnd <= gapStart) return null;

                                const outerR = isHov ? R + 8 : R;

                                const startOuter = polarToCartesian(CX, CY, outerR, gapStart);
                                const endOuter = polarToCartesian(CX, CY, outerR, gapEnd);
                                const startInner = polarToCartesian(CX, CY, INNER_R, gapStart);
                                const endInner = polarToCartesian(CX, CY, INNER_R, gapEnd);

                                const largeArc = gapEnd - gapStart <= 180 ? '0' : '1';

                                const pathD = [
                                    `M ${startOuter.x} ${startOuter.y}`,
                                    `A ${outerR} ${outerR} 0 ${largeArc} 1 ${endOuter.x} ${endOuter.y}`,
                                    `L ${endInner.x} ${endInner.y}`,
                                    `A ${INNER_R} ${INNER_R} 0 ${largeArc} 0 ${startInner.x} ${startInner.y}`,
                                    'Z'
                                ].join(' ');

                                // Mid-angle for label
                                const midAngle = (gapStart + gapEnd) / 2;
                                const labelR = (outerR + INNER_R) / 2;
                                const labelPt = polarToCartesian(CX, CY, labelR, midAngle);
                                const showLabel = (gapEnd - gapStart) > 18;

                                return (
                                    <g key={i}>
                                        <path
                                            d={pathD}
                                            fill={slice.color}
                                            opacity={hovered !== null && !isHov ? 0.45 : 1}
                                            style={{
                                                transition: 'all 0.25s cubic-bezier(0.4,0,0.2,1)',
                                                cursor: 'pointer',
                                                filter: isHov ? `drop-shadow(0 0 8px ${slice.color}88)` : 'none',
                                            }}
                                            onMouseEnter={() => setHovered(i)}
                                        />
                                        {showLabel && (
                                            <text
                                                x={labelPt.x}
                                                y={labelPt.y}
                                                textAnchor="middle"
                                                dominantBaseline="middle"
                                                fontSize="9"
                                                fontWeight="700"
                                                fill="white"
                                                style={{ pointerEvents: 'none', userSelect: 'none', textShadow: '0 1px 3px rgba(0,0,0,0.4)' }}
                                            >
                                                {slice.percentage.toFixed(1)}%
                                            </text>
                                        )}
                                    </g>
                                );
                            })}

                            {/* Center hole content */}
                            <circle cx={CX} cy={CY} r={INNER_R - 2} fill="rgba(253,251,247,0.92)" />
                            <circle cx={CX} cy={CY} r={INNER_R - 2} fill="url(#glassGradCenter)" />

                            {/* SVG definition for center gradient */}
                            <defs>
                                <radialGradient id="glassGradCenter" cx="35%" cy="30%">
                                    <stop offset="0%" stopColor="rgba(255,255,255,0.9)" />
                                    <stop offset="100%" stopColor="rgba(253,251,247,0.7)" />
                                </radialGradient>
                            </defs>

                            {/* Center text */}
                            {hoveredSlice ? (
                                <>
                                    <text x={CX} y={CY - 10} textAnchor="middle" dominantBaseline="middle"
                                        fontSize="10" fontWeight="700" fill="#064e3b" style={{ pointerEvents: 'none' }}>
                                        {hoveredSlice.relation}
                                    </text>
                                    <text x={CX} y={CY + 6} textAnchor="middle" dominantBaseline="middle"
                                        fontSize="13" fontWeight="800" fill="#1a2e05" style={{ pointerEvents: 'none' }}>
                                        {hoveredSlice.percentage.toFixed(1)}%
                                    </text>
                                    <text x={CX} y={CY + 22} textAnchor="middle" dominantBaseline="middle"
                                        fontSize="8" fill="#4b5563" style={{ pointerEvents: 'none' }}>
                                        {hoveredSlice.share}
                                    </text>
                                </>
                            ) : (
                                <>
                                    <text x={CX} y={CY - 8} textAnchor="middle" dominantBaseline="middle"
                                        fontSize="8.5" fill="#4b5563" style={{ pointerEvents: 'none' }}>
                                        Total Estate
                                    </text>
                                    <text x={CX} y={CY + 7} textAnchor="middle" dominantBaseline="middle"
                                        fontSize="10" fontWeight="800" fill="#064e3b" style={{ pointerEvents: 'none' }}>
                                        {currency} {totalAmount.toLocaleString()}
                                    </text>
                                    <text x={CX} y={CY + 22} textAnchor="middle" dominantBaseline="middle"
                                        fontSize="7.5" fill="#78350f" style={{ pointerEvents: 'none' }}>
                                        Hover a segment
                                    </text>
                                </>
                            )}
                        </svg>
                    </div>

                    {/* Legend */}
                    <div className="dist-chart-legend">
                        {slices.map((slice, i) => (
                            <div
                                key={i}
                                className={`dist-chart-legend-item ${hovered === i ? 'active' : ''} ${slice.is_blocked ? 'blocked-item' : ''}`}
                                onMouseEnter={() => !slice.is_blocked && setHovered(i)}
                                onMouseLeave={() => setHovered(null)}
                            >
                                <span
                                    className="dist-chart-legend-dot"
                                    style={{ background: slice.color, opacity: slice.is_blocked ? 0.4 : 1 }}
                                />
                                <div className="dist-chart-legend-text">
                                    <span className="dist-legend-relation">{slice.relation}</span>
                                    {slice.is_blocked ? (
                                        <span className="dist-legend-blocked-label">Mahjub (Blocked)</span>
                                    ) : (
                                        <span className="dist-legend-pct">{slice.percentage.toFixed(2)}% · {slice.share}</span>
                                    )}
                                </div>
                                {!slice.is_blocked && (
                                    <span className="dist-legend-amount">
                                        {currency} {slice.amount.toLocaleString()}
                                    </span>
                                )}
                            </div>
                        ))}
                    </div>
                </div>

                {/* Footer strip */}
                <div className="dist-chart-footer">
                    <span>🔬 Fatemi Fara'id Engine · Verified Distribution</span>
                    <span className="dist-chart-footer-right">Hover segments to inspect</span>
                </div>
            </div>
        </div>
    );
};

export default DistributionPieChart;
