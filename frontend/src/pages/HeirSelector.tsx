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

interface RelationInfo {
    relation: string;
    relation_type: string;
    lineage: string;
    gender: string;
    max: number;
    category: string;
}

const AVAILABLE_RELATIONS: RelationInfo[] = [
    // --- DIRECT ---
    { relation: 'Father', relation_type: 'Father', lineage: 'direct', gender: 'M', max: 1, category: 'Parents' },
    { relation: 'Mother', relation_type: 'Mother', lineage: 'direct', gender: 'F', max: 1, category: 'Parents' },
    { relation: 'Husband', relation_type: 'Husband', lineage: 'direct', gender: 'M', max: 1, category: 'Spouse' },
    { relation: 'Wife', relation_type: 'Wife', lineage: 'direct', gender: 'F', max: 4, category: 'Spouse' },
    { relation: 'Son', relation_type: 'Son', lineage: 'direct', gender: 'M', max: 20, category: 'Children' },
    { relation: 'Daughter', relation_type: 'Daughter', lineage: 'direct', gender: 'F', max: 20, category: 'Children' },

    // --- DESCENDANTS (Substitution) ---
    { relation: 'Son of Son', relation_type: 'Son_of_Son', lineage: 'paternal_descendant', gender: 'M', max: 20, category: 'Grandchildren' },
    { relation: 'Daughter of Son', relation_type: 'Daughter_of_Son', lineage: 'paternal_descendant', gender: 'F', max: 20, category: 'Grandchildren' },
    { relation: 'Son of Daughter', relation_type: 'Son_of_Daughter', lineage: 'maternal_descendant', gender: 'M', max: 20, category: 'Grandchildren' },
    { relation: 'Daughter of Daughter', relation_type: 'Daughter_of_Daughter', lineage: 'maternal_descendant', gender: 'F', max: 20, category: 'Grandchildren' },

    // --- SIBLINGS ---
    { relation: 'Brother', relation_type: 'Brother', lineage: 'paternal', gender: 'M', max: 20, category: 'Siblings' },
    { relation: 'Sister', relation_type: 'Sister', lineage: 'paternal', gender: 'F', max: 20, category: 'Siblings' },
    { relation: 'Son of Brother', relation_type: 'Son_of_Brother', lineage: 'paternal', gender: 'M', max: 20, category: 'Nephews' },
    { relation: 'Son of Sister', relation_type: 'Son_of_Sister', lineage: 'maternal', gender: 'M', max: 20, category: 'Nephews' },

    // --- EXTENDED ---
    { relation: 'Paternal Uncle', relation_type: 'Paternal_Uncle', lineage: 'paternal', gender: 'M', max: 20, category: 'Uncles/Aunts' },
    { relation: 'Paternal Aunt', relation_type: 'Paternal_Aunt', lineage: 'paternal', gender: 'F', max: 20, category: 'Uncles/Aunts' },
    { relation: 'Maternal Uncle', relation_type: 'Maternal_Uncle', lineage: 'maternal', gender: 'M', max: 20, category: 'Uncles/Aunts' },
    { relation: 'Maternal Aunt', relation_type: 'Maternal_Aunt', lineage: 'maternal', gender: 'F', max: 20, category: 'Uncles/Aunts' }
];

const HeirSelector: React.FC<Props> = ({ currentHeirs, onBack, onHeirChange }) => {
    const [deceasedGender, setDeceasedGender] = useState<'M' | 'F' | null>(currentHeirs.length > 0 ? (currentHeirs.some(h => h.relation_type === 'Husband') ? 'F' : 'M') : null);
    const [selectedHeirs, setSelectedHeirs] = useState<HeirInput[]>(currentHeirs);

    const filteredRelations = useMemo(() => {
        if (!deceasedGender) return [];
        return AVAILABLE_RELATIONS.filter(item => {
            if (deceasedGender === 'M' && item.relation_type === 'Husband') return false;
            if (deceasedGender === 'F' && item.relation_type === 'Wife') return false;
            return true;
        });
    }, [deceasedGender]);

    const categories = useMemo(() => {
        const cats = Array.from(new Set(filteredRelations.map(r => r.category)));
        return cats;
    }, [filteredRelations]);

    const handleAdd = (item: RelationInfo) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation_type === item.relation_type);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            newHeirs[existingIndex].count += 1;
            setSelectedHeirs(newHeirs);
        } else {
            setSelectedHeirs([...selectedHeirs, { 
                relation: item.relation, 
                relation_type: item.relation_type,
                lineage: item.lineage,
                gender: item.gender, 
                count: 1 
            }]);
        }
    };

    const handleRemove = (relType: string) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation_type === relType);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            if (newHeirs[existingIndex].count > 1) {
                newHeirs[existingIndex].count -= 1;
                setSelectedHeirs(newHeirs);
            } else {
                setSelectedHeirs(newHeirs.filter(h => h.relation_type !== relType));
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
                <div style={{ maxHeight: '60vh', overflowY: 'auto', paddingRight: '1rem' }}>
                    {categories.map(cat => (
                        <div key={cat} className="mb-4">
                            <h3 className="section-title serif" style={{ fontSize: '1.1rem', color: 'var(--secondary)' }}>{cat}</h3>
                            <div className="heir-list">
                                {filteredRelations.filter(r => r.category === cat).map(item => {
                                    const selected = selectedHeirs.find(h => h.relation_type === item.relation_type);
                                    return (
                                        <RelationCard 
                                            key={item.relation_type}
                                            relation={item.relation}
                                            count={selected ? selected.count : 0}
                                            max={item.max}
                                            onAdd={() => handleAdd(item)}
                                            onRemove={() => handleRemove(item.relation_type)}
                                        />
                                    );
                                })}
                            </div>
                        </div>
                    ))}
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
