import React, { useState } from 'react';

interface Props {
    onCalculate: (value: number, debts: number, wasiyyah: number) => void;
    onBack: () => void;
}

const EstateInput: React.FC<Props> = ({ onCalculate, onBack }) => {
    const [value, setValue] = useState<string>('');
    const [debts, setDebts] = useState<string>('');
    const [wasiyyah, setWasiyyah] = useState<string>('');

    return (
        <div className="container estate-input-view">
            <h1 className="title">Estate Value & Deductions</h1>
            <p className="subtitle">Enter the total estate value and any legal deductions (Layer 4).</p>
            
            <div className="input-card">
                <div className="input-group">
                    <label htmlFor="estate">Total Estate Amount</label>
                    <input 
                        type="number" 
                        id="estate" 
                        placeholder="e.g. 240000" 
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="debts">Outstanding Debts (Paid First)</label>
                    <input 
                        type="number" 
                        id="debts" 
                        placeholder="e.g. 10000" 
                        value={debts}
                        onChange={(e) => setDebts(e.target.value)}
                    />
                </div>
                <div className="input-group">
                    <label htmlFor="wasiyyah">Wasiyyah (Will - Max 1/3)</label>
                    <input 
                        type="number" 
                        id="wasiyyah" 
                        placeholder="e.g. 20000" 
                        value={wasiyyah}
                        onChange={(e) => setWasiyyah(e.target.value)}
                    />
                </div>
            </div>

            <div className="footer-actions">
                <button className="secondary-btn" onClick={onBack}>Back</button>
                <button 
                    className="primary-btn" 
                    disabled={!value || parseFloat(value) <= 0}
                    onClick={() => onCalculate(parseFloat(value), parseFloat(debts || '0'), parseFloat(wasiyyah || '0'))}
                >
                    Calculate Inheritance
                </button>
            </div>
        </div>
    );
};

export default EstateInput;
