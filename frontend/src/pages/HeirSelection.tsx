import React, { useState, useMemo } from 'react';
import type { HeirInput } from '../types';
import { PlusCircle, MinusCircle, User, Users } from 'lucide-react';

interface Props {
    onNext: (heirs: HeirInput[]) => void;
}

const AVAILABLE_RELATIONS = [
    { relation: 'Son', gender: 'M', max: 20 },
    { relation: 'Daughter', gender: 'F', max: 20 },
    { relation: 'Father', gender: 'M', max: 1 },
    { relation: 'Mother', gender: 'F', max: 1 },
    { relation: 'Husband', gender: 'M', max: 1 },
    { relation: 'Wife', gender: 'F', max: 4 },
    { relation: 'Brother', gender: 'M', max: 20 },
    { relation: 'Sister', gender: 'F', max: 20 },
    { relation: 'Grandson', gender: 'M', max: 20 },
    { relation: 'Granddaughter', gender: 'F', max: 20 },
    { relation: 'Uncle', gender: 'M', max: 20 },
    { relation: 'Cousin', gender: 'M', max: 20 },
    { relation: 'Nephew', gender: 'M', max: 20 },
    { relation: 'Dhawu_Arham', gender: 'M', max: 20 }
];

const HeirSelection: React.FC<Props> = ({ onNext }) => {
    const [deceasedGender, setDeceasedGender] = useState<'M' | 'F' | null>(null);
    const [selectedHeirs, setSelectedHeirs] = useState<HeirInput[]>([]);

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
            } else {
                newHeirs.splice(existingIndex, 1);
            }
            setSelectedHeirs(newHeirs);
        }
    };

    const toggleSpecialFlag = (relation: string, flag: keyof HeirInput) => {
        const newHeirs = selectedHeirs.map(h => {
            if (h.relation === relation) {
                return { ...h, [flag]: !h[flag] };
            }
            return h;
        });
        setSelectedHeirs(newHeirs);
    };

    if (!deceasedGender) {
        return (
            <div className="container center">
                <h1 className="title">Whose Inheritance?</h1>
                <p className="subtitle">Select the gender of the deceased to begin.</p>
                <div className="gender-selector">
                    <button className="gender-btn male" onClick={() => setDeceasedGender('M')}>
                        <User size={48} />
                        <span>Male (Marhum)</span>
                    </button>
                    <button className="gender-btn female" onClick={() => setDeceasedGender('F')}>
                        <User size={48} />
                        <span>Female (Marhuma)</span>
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="container">
            <h1 className="title">Select Heirs</h1>
            <p className="subtitle">
                Adding heirs for a <strong>{deceasedGender === 'M' ? 'Male' : 'Female'}</strong> deceased.
                <button className="text-link" onClick={() => {setDeceasedGender(null); setSelectedHeirs([]);}}>Change</button>
            </p>
            
            <div className="selection-grid">
                <div className="available-heirs">
                    <div className="section-header">
                        <PlusCircle size={20} />
                        <h3>Potential Heirs</h3>
                    </div>
                    <div className="list scrollable">
                        {filteredRelations.map(item => {
                            const selected = selectedHeirs.find(h => h.relation === item.relation);
                            const isMax = selected && selected.count >= item.max;
                            return (
                                <div 
                                    key={item.relation} 
                                    className={`heir-item ${isMax ? 'disabled' : ''}`}
                                    onClick={() => !isMax && addHeir(item.relation, item.gender, item.max)}
                                >
                                    <div className="relation-info">
                                        <span className="relation-name">{item.relation}</span>
                                        <span className="relation-meta">{item.max === 1 ? 'Unique' : `Max ${item.max}`}</span>
                                    </div>
                                    <PlusCircle className="icon" size={20} />
                                </div>
                            );
                        })}
                    </div>
                </div>

                <div className="selected-heirs">
                    <div className="section-header">
                        <Users size={20} />
                        <h3>Surviving Family</h3>
                    </div>
                    <div className="list">
                        {selectedHeirs.length === 0 ? (
                            <div className="empty-state">
                                <p>No heirs selected. Click on potential heirs to add them.</p>
                            </div>
                        ) : (
                            selectedHeirs.map(heir => {
                                const relConfig = AVAILABLE_RELATIONS.find(r => r.relation === heir.relation);
                                return (
                                    <div key={heir.relation} className="selected-item-card">
                                        <div className="item-main">
                                            <div className="count-ctrl">
                                                <button onClick={() => removeHeir(heir.relation)}><MinusCircle size={18} /></button>
                                                <span className="count">{heir.count}</span>
                                                <button 
                                                    disabled={relConfig && heir.count >= relConfig.max}
                                                    onClick={() => relConfig && addHeir(heir.relation, heir.gender, relConfig.max)}
                                                >
                                                    <PlusCircle size={18} />
                                                </button>
                                            </div>
                                            <span className="name">{heir.relation}</span>
                                        </div>
                                        
                                        <div className="special-flags">
                                            <label className={`flag ${heir.is_killer ? 'active' : ''}`}>
                                                <input type="checkbox" checked={!!heir.is_killer} onChange={() => toggleSpecialFlag(heir.relation, 'is_killer')} />
                                                <span>Killer</span>
                                            </label>
                                            <label className={`flag ${heir.is_different_religion ? 'active' : ''}`}>
                                                <input type="checkbox" checked={!!heir.is_different_religion} onChange={() => toggleSpecialFlag(heir.relation, 'is_different_religion')} />
                                                <span>Non-Muslim</span>
                                            </label>
                                            <label className={`flag ${heir.is_missing ? 'active' : ''}`}>
                                                <input type="checkbox" checked={!!heir.is_missing} onChange={() => toggleSpecialFlag(heir.relation, 'is_missing')} />
                                                <span>Missing</span>
                                            </label>
                                            <label className={`flag ${heir.is_illegitimate ? 'active' : ''}`}>
                                                <input type="checkbox" checked={!!heir.is_illegitimate} onChange={() => toggleSpecialFlag(heir.relation, 'is_illegitimate')} />
                                                <span>Illegitimate</span>
                                            </label>
                                        </div>
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            </div>

            <div className="footer-actions">
                <button 
                    className="primary-btn big" 
                    disabled={selectedHeirs.length === 0}
                    onClick={() => onNext(selectedHeirs)}
                >
                    Continue to Financials
                </button>
            </div>
        </div>
    );
};

export default HeirSelection;
