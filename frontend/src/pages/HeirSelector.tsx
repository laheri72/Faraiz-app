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
    generation_level: number;
}

const AVAILABLE_RELATIONS: RelationInfo[] = [
    // --- DIRECT ---
    { relation: 'Father', relation_type: 'Father', lineage: 'direct', gender: 'M', max: 1, category: 'Parents', generation_level: 1 },
    { relation: 'Mother', relation_type: 'Mother', lineage: 'direct', gender: 'F', max: 1, category: 'Parents', generation_level: 1 },
    { relation: 'Husband', relation_type: 'Husband', lineage: 'direct', gender: 'M', max: 1, category: 'Spouse', generation_level: 1 },
    { relation: 'Wife', relation_type: 'Wife', lineage: 'direct', gender: 'F', max: 4, category: 'Spouse', generation_level: 1 },
    { relation: 'Son', relation_type: 'Son', lineage: 'direct', gender: 'M', max: 20, category: 'Children', generation_level: 1 },
    { relation: 'Daughter', relation_type: 'Daughter', lineage: 'direct', gender: 'F', max: 20, category: 'Children', generation_level: 1 },

    // --- GRANDPARENTS (New Module) ---
    { relation: 'PGF (Jad) [Father Side]', relation_type: 'grandfather_paternal', lineage: 'paternal', gender: 'M', max: 1, category: 'Grandparents', generation_level: 2 },
    { relation: 'PGM (Jaddah) [Father Side]', relation_type: 'grandmother_paternal', lineage: 'paternal', gender: 'F', max: 3, category: 'Grandparents', generation_level: 2 },
    { relation: 'MGF (Jad) [Mother Side]', relation_type: 'grandfather_maternal', lineage: 'maternal', gender: 'M', max: 1, category: 'Grandparents', generation_level: 2 },
    { relation: 'MGM (Jaddah) [Mother Side]', relation_type: 'grandmother_maternal', lineage: 'maternal', gender: 'F', max: 3, category: 'Grandparents', generation_level: 2 },

    // --- DESCENDANTS (Substitution) ---
    { relation: 'Son of Son', relation_type: 'Son_of_Son', lineage: 'paternal_descendant', gender: 'M', max: 20, category: 'Grandchildren', generation_level: 2 },
    { relation: 'Daughter of Son', relation_type: 'Daughter_of_Son', lineage: 'paternal_descendant', gender: 'F', max: 20, category: 'Grandchildren', generation_level: 2 },
    { relation: 'Son of Daughter', relation_type: 'Son_of_Daughter', lineage: 'maternal_descendant', gender: 'M', max: 20, category: 'Grandchildren', generation_level: 2 },
    { relation: 'Daughter of Daughter', relation_type: 'Daughter_of_Daughter', lineage: 'maternal_descendant', gender: 'F', max: 20, category: 'Grandchildren', generation_level: 2 },

    // --- SIBLINGS ---
    { relation: 'Brother', relation_type: 'Brother', lineage: 'paternal', gender: 'M', max: 20, category: 'Siblings', generation_level: 1 },
    { relation: 'Sister', relation_type: 'Sister', lineage: 'paternal', gender: 'F', max: 20, category: 'Siblings', generation_level: 1 },
    { relation: 'Son of Brother', relation_type: 'Son_of_Brother', lineage: 'paternal', gender: 'M', max: 20, category: 'Nephews', generation_level: 2 },
    { relation: 'Son of Sister', relation_type: 'Son_of_Sister', lineage: 'maternal', gender: 'M', max: 20, category: 'Nephews', generation_level: 2 },

    // --- EXTENDED ---
    { relation: 'Paternal Uncle', relation_type: 'Paternal_Uncle', lineage: 'paternal', gender: 'M', max: 20, category: 'Uncles/Aunts', generation_level: 2 },
    { relation: 'Paternal Aunt', relation_type: 'Paternal_Aunt', lineage: 'paternal', gender: 'F', max: 20, category: 'Uncles/Aunts', generation_level: 2 },
    { relation: 'Maternal Uncle', relation_type: 'Maternal_Uncle', lineage: 'maternal', gender: 'M', max: 20, category: 'Uncles/Aunts', generation_level: 2 },
    { relation: 'Maternal Aunt', relation_type: 'Maternal_Aunt', lineage: 'maternal', gender: 'F', max: 20, category: 'Uncles/Aunts', generation_level: 2 }
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

    const [activeTab, setActiveTab] = useState<string>(categories[0] || '');

    const handleAdd = (item: RelationInfo) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation_type === item.relation_type && h.generation_level === item.generation_level);
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
                count: 1,
                generation_level: item.generation_level
            }]);
        }
    };

    const handleRemove = (relType: string, genLevel: number) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation_type === relType && h.generation_level === genLevel);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            if (newHeirs[existingIndex].count > 1) {
                newHeirs[existingIndex].count -= 1;
                setSelectedHeirs(newHeirs);
            } else {
                setSelectedHeirs(newHeirs.filter((_, idx) => idx !== existingIndex));
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

            <div className="tabs-container">
                {categories.map(cat => (
                    <button 
                        key={cat} 
                        className={`tab-btn ${activeTab === cat ? 'active' : ''}`}
                        onClick={() => setActiveTab(cat)}
                    >
                        {cat}
                    </button>
                ))}
            </div>

            <div className="heir-selection-grid">
                <div style={{ maxHeight: '60vh', overflowY: 'auto', paddingRight: '1rem' }}>
                    <div className="heir-list">
                        {filteredRelations.filter(r => r.category === activeTab).map(item => {
                            const selected = selectedHeirs.find(h => h.relation_type === item.relation_type && h.generation_level === item.generation_level);
                            return (
                                <RelationCard 
                                    key={`${item.relation_type}_${item.generation_level}`}
                                    relation={item.relation}
                                    count={selected ? selected.count : 0}
                                    max={item.max}
                                    onAdd={() => handleAdd(item)}
                                    onRemove={() => handleRemove(item.relation_type, item.generation_level)}
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
