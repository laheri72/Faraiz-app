import React, { useState, useMemo } from 'react';
import type { HeirInput } from '../types';
import { User } from 'lucide-react';
import RelationCard from '../components/RelationCard';
import SelectionAudit from '../components/SelectionAudit';

interface Props {
    currentHeirs: HeirInput[];
    onBack: () => void;
    onHeirChange: (heirs: HeirInput[]) => void;
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

const HeirSelector: React.FC<Props> = ({ currentHeirs, onBack, onHeirChange }) => {
    const [deceasedGender, setDeceasedGender] = useState<'M' | 'F' | null>(currentHeirs.length > 0 ? (currentHeirs.some(h => h.relation === 'Husband') ? 'F' : 'M') : null);
    const [selectedHeirs, setSelectedHeirs] = useState<HeirInput[]>(currentHeirs);

    const filteredRelations = useMemo(() => {
        if (!deceasedGender) return [];
        return AVAILABLE_RELATIONS.filter(item => {
            if (deceasedGender === 'M' && item.relation === 'Husband') return false;
            if (deceasedGender === 'F' && item.relation === 'Wife') return false;
            return true;
        });
    }, [deceasedGender]);

    const handleAdd = (item: typeof AVAILABLE_RELATIONS[0]) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation === item.relation);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            newHeirs[existingIndex].count += 1;
            setSelectedHeirs(newHeirs);
        } else {
            setSelectedHeirs([...selectedHeirs, { relation: item.relation, gender: item.gender, count: 1 }]);
        }
    };

    const handleRemove = (relation: string) => {
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
                <div className="page-statement">
                    <h2 className="serif">Initial Identification</h2>
                    <p>Please identify the gender of the deceased (Marhum/Marhuma) to determine eligible heirs.</p>
                </div>
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
            <div className="page-statement">
                <h2 className="serif">Step 2: Heir Selection</h2>
                <p>Define the surviving family members of the deceased <strong>({deceasedGender === 'M' ? 'Marhum' : 'Marhuma'})</strong>.</p>
                <button className="text-link" style={{ fontSize: '0.85rem', color: 'var(--secondary)' }} onClick={() => {setDeceasedGender(null); setSelectedHeirs([]);}}>Change deceased gender</button>
            </div>

            <div className="heir-selection-grid">
                <div>
                    <h3 className="serif" style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>Relational Heir List</h3>
                    <div className="heir-list">
                        {filteredRelations.map(item => {
                            const selected = selectedHeirs.find(h => h.relation === item.relation);
                            return (
                                <RelationCard 
                                    key={item.relation}
                                    relation={item.relation}
                                    count={selected ? selected.count : 0}
                                    max={item.max}
                                    onAdd={() => handleAdd(item)}
                                    onRemove={() => handleRemove(item.relation)}
                                />
                            );
                        })}
                    </div>
                </div>

                <SelectionAudit heirs={selectedHeirs} />
            </div>

            <div className="action-area">
                <button className="btn-outline" onClick={onBack}>Back: Estate</button>
                <button className="btn-primary" disabled={selectedHeirs.length === 0} onClick={() => onHeirChange(selectedHeirs)}>
                    Next: Case Summary
                </button>
            </div>
        </div>
    );
};

export default HeirSelector;
