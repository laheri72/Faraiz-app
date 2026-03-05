import React from 'react';
import { HelpCircle, Plus, Minus, Trash2 } from 'lucide-react';
import type { HeirInput } from '../types';

interface Props {
    heirs: HeirInput[];
    onAdd: (relType: string, genLevel: number) => void;
    onRemove: (relType: string, genLevel: number) => void;
    onClear: (relType: string, genLevel: number) => void;
}

const SelectionAudit: React.FC<Props> = ({ heirs, onAdd, onRemove, onClear }) => {
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
            <h4 className="serif" style={{ fontSize: '1rem', color: 'var(--primary)', marginBottom: '1rem' }}>Currently Entered</h4>
            {heirs.length === 0 ? (
                <p style={{ fontSize: '0.9rem', fontStyle: 'italic' }}>No heirs identified yet.</p>
            ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    {heirs.map(h => (
                        <div key={`${h.relation_type}_${h.generation_level}`} className="flex justify-between items-center" style={{ 
                            fontSize: '0.9rem', 
                            padding: '0.5rem', 
                            background: 'white', 
                            borderRadius: '0.25rem',
                            border: '1px solid var(--border-elegant)'
                        }}>
                            <div style={{ display: 'flex', flexDirection: 'column' }}>
                                <span style={{ fontWeight: '700' }}>{h.relation}</span>
                                <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Count: {h.count}</span>
                            </div>
                            <div className="flex items-center gap-1">
                                <button 
                                    onClick={() => onRemove(h.relation_type, h.generation_level)}
                                    style={{ padding: '0.25rem', minWidth: 'auto', minHeight: 'auto', border: '1px solid var(--border)', borderRadius: '0.25rem', background: 'none' }}
                                >
                                    <Minus size={12} />
                                </button>
                                <button 
                                    onClick={() => onAdd(h.relation_type, h.generation_level)}
                                    style={{ padding: '0.25rem', minWidth: 'auto', minHeight: 'auto', border: '1px solid var(--border)', borderRadius: '0.25rem', background: 'none' }}
                                >
                                    <Plus size={12} />
                                </button>
                                <button 
                                    onClick={() => onClear(h.relation_type, h.generation_level)}
                                    style={{ padding: '0.25rem', minWidth: 'auto', minHeight: 'auto', border: '1px solid var(--error)', borderRadius: '0.25rem', background: 'none', color: 'var(--error)', marginLeft: '0.25rem' }}
                                >
                                    <Trash2 size={12} />
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SelectionAudit;
