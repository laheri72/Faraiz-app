import React from 'react';
import { HelpCircle } from 'lucide-react';
import type { HeirInput } from '../types';

interface Props {
    heirs: HeirInput[];
}

const SelectionAudit: React.FC<Props> = ({ heirs }) => {
    return (
        <div style={{ background: 'var(--bg)', padding: '1.5rem', border: '1px dashed var(--gold)', borderRadius: '0.25rem' }}>
            <h4 className="serif flex items-center gap-2" style={{ color: 'var(--secondary)' }}>
                <HelpCircle size={18} /> Note on Identification
            </h4>
            <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                Ensure all surviving relatives are entered, even if they may be excluded (Mahjub). 
                The engine will apply layer-by-layer exclusionary logic.
            </p>
            <hr style={{ border: 'none', borderTop: '1px solid var(--gold)', margin: '1rem 0' }} />
            <h4 className="serif" style={{ fontSize: '1rem', color: 'var(--primary)' }}>Currently Entered</h4>
            {heirs.length === 0 ? (
                <p style={{ fontSize: '0.9rem', fontStyle: 'italic' }}>No heirs identified yet.</p>
            ) : (
                <ul style={{ fontSize: '0.9rem', paddingLeft: '1.2rem' }}>
                    {heirs.map(h => (
                        <li key={h.relation}>{h.count} {h.relation}{h.count > 1 ? 's' : ''}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default SelectionAudit;
