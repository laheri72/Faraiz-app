import React, { useState, useMemo } from 'react';
import type { HeirInput } from '../types';
import { Plus, Minus, User, HelpCircle } from 'lucide-react';

interface Props {
    initialHeirs: HeirInput[];
    onBack: () => void;
    onNext: (heirs: HeirInput[]) => void;
}

const AVAILABLE_RELATIONS = [
    { relation: 'Father', gender: 'M', max: 1 },
    { relation: 'Mother', gender: 'F', max: 1 },
    { relation: 'Husband', gender: 'M', max: 1 },
    { relation: 'Wife', gender: 'F', max: 4 },
    { relation: 'Son', gender: 'M', max: 20 },
    { relation: 'Daughter', gender: 'F', max: 20 },
    { relation: 'Brother', gender: 'M', max: 20 },
    { relation: 'Sister', gender: 'F', max: 20 },
    { relation: 'Uncle', gender: 'M', max: 20 },
    { relation: 'Cousin', gender: 'M', max: 20 },
    { relation: 'Dhawu al-Arham', gender: 'M', max: 1 }
];

const HeirSelection: React.FC<Props> = ({ initialHeirs, onBack, onNext }) => {
    const [deceasedGender, setDeceasedGender] = useState<'M' | 'F' | null>(initialHeirs.length > 0 ? (initialHeirs.some(h => h.relation === 'Husband') ? 'F' : 'M') : null);
    const [selectedHeirs, setSelectedHeirs] = useState<HeirInput[]>(initialHeirs);

    const filteredRelations = useMemo(() => {
        if (!deceasedGender) return [];
        return AVAILABLE_RELATIONS.filter(item => {
            if (deceasedGender === 'M' && item.relation === 'Husband') return false;
            if (deceasedGender === 'F' && item.relation === 'Wife') return false;
            return true;
        });
    }, [deceasedGender]);

    const addHeir = (relation: string, gender: string, max: number) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation === relation);
        if (existingIndex !== -1) {
            if (selectedHeirs[existingIndex].count < max) {
                const newHeirs = [...selectedHeirs];
                newHeirs[existingIndex].count += 1;
                setSelectedHeirs(newHeirs);
            }
        } else {
            setSelectedHeirs([...selectedHeirs, { relation, gender, count: 1 }]);
        }
    };

    const removeHeir = (relation: string) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation === relation);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            if (newHeirs[existingIndex].count > 1) {
                newHeirs[existingIndex].count -= 1;
                setSelectedHeirs(newHeirs);
            } else {
                setSelectedHeirs(newHeirs.filter(h => h.relation !== relation));
            }
        }
    };

    if (!deceasedGender) {
        return (
            <div className="animate-fade">
                <h2 className="section-title serif">Initial Identification</h2>
                <p className="text-muted mb-4">Please identify the gender of the deceased (Marhum/Marhuma).</p>
                <div className="flex gap-2 justify-center mt-4">
                    <button className="btn-outline flex items-center gap-2" onClick={() => setDeceasedGender('M')}>
                        <User size={18} /> Male deceased
                    </button>
                    <button className="btn-outline flex items-center gap-2" onClick={() => setDeceasedGender('F')}>
                        <User size={18} /> Female deceased
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="animate-fade">
            <h2 className="section-title serif">Step 2: Heir Selection</h2>
            <p className="text-muted mb-4">
                Define the surviving family members of the deceased <strong>({deceasedGender === 'M' ? 'Marhum' : 'Marhuma'})</strong>.
                The engine will apply exclusion rules automatically.
                <button className="text-link" style={{ marginLeft: '1rem', color: 'var(--secondary)' }} onClick={() => {setDeceasedGender(null); setSelectedHeirs([]);}}>Change gender</button>
            </p>

            <div className="heir-selection-grid">
                <div>
                    <h3 className="serif" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Relational Heir List</h3>
                    <div className="heir-list">
                        {filteredRelations.map(item => {
                            const selected = selectedHeirs.find(h => h.relation === item.relation);
                            const count = selected ? selected.count : 0;
                            const isMax = count >= item.max;

                            return (
                                <div key={item.relation} className="heir-card">
                                    <div className="info">
                                        <span className="name">{item.relation}</span>
                                        <small className="text-muted">{item.max > 1 ? `Up to ${item.max}` : 'Unique relation'}</small>
                                    </div>
                                    <div className="count-actions">
                                        <button 
                                            className="btn-icon" 
                                            disabled={count === 0} 
                                            onClick={() => removeHeir(item.relation)}
                                        >
                                            <Minus size={14} />
                                        </button>
                                        <span style={{ fontWeight: '800', minWidth: '1.5rem', textAlign: 'center' }}>{count}</span>
                                        <button 
                                            className="btn-icon" 
                                            disabled={isMax} 
                                            onClick={() => addHeir(item.relation, item.gender, item.max)}
                                        >
                                            <Plus size={14} />
                                        </button>
                                    </div>
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div>
                    <div style={{ background: 'var(--bg)', padding: '1.5rem', border: '1px dashed var(--gold)', borderRadius: '0.25rem' }}>
                        <h4 className="serif flex items-center gap-2" style={{ color: 'var(--secondary)' }}>
                            <HelpCircle size={18} /> Note on Identification
                        </h4>
                        <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)' }}>
                            Ensure all surviving relatives are entered, even if they may be excluded (Mahjub). 
                            The engine will apply layer-by-layer exclusionary logic according to the 
                            jurisprudence rules.
                        </p>
                        <hr style={{ border: 'none', borderTop: '1px solid var(--gold)', margin: '1rem 0' }} />
                        <h4 className="serif" style={{ fontSize: '1rem', color: 'var(--primary)' }}>Currently Entered</h4>
                        {selectedHeirs.length === 0 ? (
                            <p style={{ fontSize: '0.9rem', fontStyle: 'italic' }}>No heirs identified yet.</p>
                        ) : (
                            <ul style={{ fontSize: '0.9rem', paddingLeft: '1.2rem' }}>
                                {selectedHeirs.map(h => (
                                    <li key={h.relation}>{h.count} {h.relation}{h.count > 1 ? 's' : ''}</li>
                                ))}
                            </ul>
                        )}
                    </div>
                </div>
            </div>

            <div className="flex justify-between mt-4">
                <button className="btn-outline" onClick={onBack}>Back: Estate</button>
                <button 
                    className="btn-primary" 
                    disabled={selectedHeirs.length === 0}
                    onClick={() => onNext(selectedHeirs)}
                >
                    Next: Case Summary
                </button>
            </div>
        </div>
    );
};

export default HeirSelection;
