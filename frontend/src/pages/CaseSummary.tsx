import React from 'react';
import type { HeirInput } from '../types';
import { Landmark, Users, ClipboardCheck } from 'lucide-react';

interface CaseState {
    estate: { value: number, debts: number, wasiyyah: number };
    heirs: HeirInput[];
}

interface Props {
    caseState: CaseState;
    onBack: () => void;
    onCalculate: () => void;
}

const CaseSummary: React.FC<Props> = ({ caseState, onBack, onCalculate }) => {
    const { estate, heirs } = caseState;
    const netEstate = estate.value - estate.debts - estate.wasiyyah;
    
    // Percentages for visual bar
    const debtPct = (estate.debts / estate.value) * 100;
    const wasiyyahPct = (estate.wasiyyah / estate.value) * 100;
    const netPct = 100 - debtPct - wasiyyahPct;

    return (
        <div className="animate-fade">
            <div className="page-statement">
                <h2 className="serif">Step 3: Case Summary</h2>
                <p>Please verify the case details below before initiating the formal jurisprudence calculation.</p>
            </div>

            {/* Visual Distributable Bar */}
            <div style={{ marginBottom: '2.5rem' }}>
                <div className="flex justify-between items-center mb-2" style={{ fontSize: '0.85rem', fontWeight: '600' }}>
                    <span className="serif">Estate Allocation Overview</span>
                    <span className="text-muted">Net: {Math.round(netPct)}%</span>
                </div>
                <div style={{ 
                    width: '100%', 
                    height: '24px', 
                    display: 'flex', 
                    borderRadius: '12px', 
                    overflow: 'hidden', 
                    boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1)',
                    background: '#e5e7eb'
                }}>
                    {estate.debts > 0 && (
                        <div style={{ width: `${debtPct}%`, background: 'var(--error)', transition: 'width 0.5s ease' }} title="Debts" />
                    )}
                    {estate.wasiyyah > 0 && (
                        <div style={{ width: `${wasiyyahPct}%`, background: 'var(--accent)', transition: 'width 0.5s ease' }} title="Wasiyyah" />
                    )}
                    <div style={{ width: `${netPct}%`, background: 'var(--primary)', transition: 'width 0.5s ease' }} title="Net Distributable" />
                </div>
                <div className="flex gap-4 mt-2 justify-center" style={{ fontSize: '0.75rem' }}>
                    <div className="flex items-center gap-1"><div style={{ width: '10px', height: '10px', background: 'var(--primary)', borderRadius: '2px' }} /> Net Distributable</div>
                    {estate.wasiyyah > 0 && <div className="flex items-center gap-1"><div style={{ width: '10px', height: '10px', background: 'var(--accent)', borderRadius: '2px' }} /> Wasiyyah</div>}
                    {estate.debts > 0 && <div className="flex items-center gap-1"><div style={{ width: '10px', height: '10px', background: 'var(--error)', borderRadius: '2px' }} /> Debts</div>}
                </div>
            </div>

            <div className="grid-2">
                <div style={{ background: '#f9fafb', padding: '1.5rem', borderRadius: '0.25rem', border: '1px solid var(--border-elegant)' }}>
                    <h3 className="serif flex items-center gap-2" style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>
                        <Landmark size={18} /> Financials
                    </h3>
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                        <div className="flex justify-between">
                            <span className="text-muted">Total Estate:</span>
                            <span style={{ fontWeight: '700' }}>{estate.value.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-muted">Total Debts:</span>
                            <span style={{ color: 'var(--error)' }}>- {estate.debts.toLocaleString()}</span>
                        </div>
                        <div className="flex justify-between">
                            <span className="text-muted">Wasiyyah:</span>
                            <span style={{ color: 'var(--error)' }}>- {estate.wasiyyah.toLocaleString()}</span>
                        </div>
                        <hr style={{ border: 'none', borderTop: '1px solid var(--border)', margin: '0.5rem 0' }} />
                        <div className="flex justify-between" style={{ fontSize: '1.1rem' }}>
                            <span style={{ fontWeight: '700' }}>Net Distributable:</span>
                            <span style={{ fontWeight: '800', color: 'var(--primary)' }}>{netEstate.toLocaleString()}</span>
                        </div>
                    </div>
                </div>

                <div style={{ background: '#f9fafb', padding: '1.5rem', borderRadius: '0.25rem', border: '1px solid var(--border-elegant)' }}>
                    <h3 className="serif flex items-center gap-2" style={{ fontSize: '1.1rem', marginBottom: '1rem' }}>
                        <Users size={18} /> Surviving Heirs
                    </h3>
                    <ul style={{ paddingLeft: '1.2rem', margin: 0 }}>
                        {heirs.map((h, i) => (
                            <li key={i} style={{ marginBottom: '0.25rem' }}>
                                <strong>{h.count}</strong> {h.relation}{h.count > 1 ? 's' : ''}
                            </li>
                        ))}
                    </ul>
                </div>
            </div>

            <div style={{ marginTop: '2rem', textAlign: 'center', padding: '1.5rem', background: 'var(--bg)', border: '1px solid var(--gold)' }}>
                <p style={{ margin: 0, fontStyle: 'italic', color: 'var(--secondary)', fontSize: '0.95rem' }}>
                    By clicking "Run Engine", you initiate a multi-layer deterministic calculation 
                    based on the Fatemi Fiqh Wirasat rules.
                </p>
            </div>

            <div className="action-area">
                <button className="btn-outline" onClick={onBack}>Back: Edit Heirs</button>
                <button 
                    className="btn-primary flex items-center gap-2" 
                    onClick={onCalculate}
                >
                    <ClipboardCheck size={18} /> Run Engine
                </button>
            </div>
        </div>
    );
};

export default CaseSummary;
