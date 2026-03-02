import React, { useState } from 'react';
import { HeirInput } from '../api/client';
import { UserPlus, UserMinus, PlusCircle, MinusCircle } from 'lucide-react';

interface Props {
    onNext: (heirs: HeirInput[]) => void;
}

const AVAILABLE_RELATIONS = [
    { relation: 'Son', gender: 'M' },
    { relation: 'Daughter', gender: 'F' },
    { relation: 'Father', gender: 'M' },
    { relation: 'Mother', gender: 'F' },
    { relation: 'Husband', gender: 'M' },
    { relation: 'Wife', gender: 'F' },
    { relation: 'Brother', gender: 'M' },
    { relation: 'Sister', gender: 'F' },
    { relation: 'Uncle', gender: 'M' },
    { relation: 'Cousin', gender: 'M' }
];

const HeirSelection: React.FC<Props> = ({ onNext }) => {
    const [selectedHeirs, setSelectedHeirs] = useState<HeirInput[]>([]);

    const addHeir = (relation: string, gender: string) => {
        const existingIndex = selectedHeirs.findIndex(h => h.relation === relation);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            newHeirs[existingIndex].count += 1;
            setSelectedHeirs(newHeirs);
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

    return (
        <div className="container">
            <h1 className="title">Select Heirs</h1>
            <p className="subtitle">Choose the surviving relatives of the deceased.</p>
            
            <div className="selection-grid">
                <div className="available-heirs">
                    <h3>Available Heirs</h3>
                    <div className="list">
                        {AVAILABLE_RELATIONS.map(item => (
                            <div key={item.relation} className="heir-item" onClick={() => addHeir(item.relation, item.gender)}>
                                <span>{item.relation}</span>
                                <PlusCircle className="icon" size={20} />
                            </div>
                        ))}
                    </div>
                </div>

                <div className="selected-heirs">
                    <h3>Selected Heirs</h3>
                    <div className="list">
                        {selectedHeirs.length === 0 ? (
                            <p className="empty-msg">No heirs selected yet.</p>
                        ) : (
                            selectedHeirs.map(heir => (
                                <div key={heir.relation} className="selected-item">
                                    <span className="count-badge">{heir.count}x</span>
                                    <span className="name">{heir.relation}</span>
                                    <div className="actions">
                                        <PlusCircle className="action-icon" size={20} onClick={() => addHeir(heir.relation, heir.gender)} />
                                        <MinusCircle className="action-icon remove" size={20} onClick={() => removeHeir(heir.relation)} />
                                    </div>
                                </div>
                            ))
                        )}
                    </div>
                </div>
            </div>

            <div className="footer-actions">
                <button 
                    className="primary-btn" 
                    disabled={selectedHeirs.length === 0}
                    onClick={() => onNext(selectedHeirs)}
                >
                    Next: Estate Value
                </button>
            </div>
        </div>
    );
};

export default HeirSelection;
