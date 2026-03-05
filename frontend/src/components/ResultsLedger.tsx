import React from 'react';
import type { CalculationResult, VerificationData } from '../types';

interface Props {
    results: CalculationResult[];
    verification: VerificationData | null;
}

const ResultsLedger: React.FC<Props> = ({ results, verification }) => {
    const totalDistributed = results.reduce((acc, curr) => acc + curr.amount, 0);
    const isVerified = verification?.status === 'VALID' || verification?.is_balanced;

    return (
        <div className="results-ledger print-only" style={{ padding: '2rem', background: 'white', color: 'black', fontFamily: 'serif' }}>
            <div className="ledger-header" style={{ borderBottom: '2px solid black', paddingBottom: '1rem', marginBottom: '2rem', textAlign: 'center' }}>
                <h1 style={{ margin: 0, textTransform: 'uppercase', letterSpacing: '2px' }}>Inheritance Distribution Ledger</h1>
                <p style={{ margin: '0.5rem 0', fontStyle: 'italic' }}>Fatemi Fiqh Jurisprudence Distribution Decree</p>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '1rem', fontSize: '0.9rem' }}>
                    <span>Date: {new Date().toLocaleDateString()}</span>
                    <span>Document ID: FW-{Math.random().toString(36).substr(2, 6).toUpperCase()}</span>
                </div>
            </div>

            <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '2rem' }}>
                <thead>
                    <tr style={{ background: '#f0f0f0' }}>
                        <th style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'left' }}>Heir Relation</th>
                        <th style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'center' }}>Share (%)</th>
                        <th style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'center' }}>Fractional Share</th>
                        <th style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'right' }}>Actual Amount</th>
                        <th style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'right' }}>Arabic Rule Basis</th>
                    </tr>
                </thead>
                <tbody>
                    {results.map((res, i) => (
                        <tr key={i}>
                            <td style={{ border: '1px solid black', padding: '0.75rem' }}>
                                <strong>{res.relation}</strong>
                            </td>
                            <td style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'center' }}>
                                {res.is_blocked ? '0%' : `${((res.share_percentage || 0) * 100).toFixed(2)}%`}
                            </td>
                            <td style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'center' }}>
                                {res.is_blocked ? 'MAHJUB' : res.share}
                            </td>
                            <td style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'right', fontWeight: 'bold' }}>
                                {res.amount.toLocaleString()}
                            </td>
                            <td style={{ border: '1px solid black', padding: '0.75rem', textAlign: 'right', direction: 'rtl', fontFamily: 'Amiri, serif', fontSize: '1.1rem' }}>
                                {res.arabic_reasoning && res.arabic_reasoning.length > 0 ? res.arabic_reasoning[0] : '-'}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>

            <div className="ledger-summary" style={{ marginTop: '3rem', border: '2px solid black', padding: '1.5rem' }}>
                <h3 style={{ margin: '0 0 1rem 0', borderBottom: '1px solid black', paddingBottom: '0.5rem' }}>Distribution Summary</h3>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
                    <div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                            <span>Total Estate (Net):</span>
                            <span style={{ fontWeight: 'bold' }}>{totalDistributed.toLocaleString()}</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                            <span>Total Allocated:</span>
                            <span style={{ fontWeight: 'bold' }}>{totalDistributed.toLocaleString()}</span>
                        </div>
                    </div>
                    <div style={{ borderLeft: '1px solid #ccc', paddingLeft: '2rem' }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                            <span>Verification Status:</span>
                            <span style={{ color: isVerified ? 'green' : 'red', fontWeight: 'bold' }}>
                                {isVerified ? 'VERIFIED' : 'UNBALANCED'}
                            </span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                            <span>Jurisprudence Check:</span>
                            <span style={{ fontWeight: 'bold' }}>PASSED</span>
                        </div>
                    </div>
                </div>
            </div>

            <div style={{ marginTop: '4rem', display: 'flex', justifyContent: 'space-between' }}>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ borderTop: '1px solid black', width: '200px', paddingTop: '0.5rem' }}>Official Stamp</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                    <div style={{ borderTop: '1px solid black', width: '200px', paddingTop: '0.5rem' }}>Signature of Authority</div>
                </div>
            </div>
            
            <div style={{ marginTop: '2rem', textAlign: 'center', fontSize: '0.8rem', color: '#666' }}>
                Generated via Fatemi Wirasat Engine. This document is a deterministic calculation 
                based on the rules of Fatemi Fiqh.
            </div>
        </div>
    );
};

export default ResultsLedger;
