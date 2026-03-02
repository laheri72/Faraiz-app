import React, { useState } from 'react';

interface Props {
    onCalculate: (value: number) => void;
    onBack: () => void;
}

const EstateInput: React.FC<Props> = ({ onCalculate, onBack }) => {
    const [value, setValue] = useState<string>('');

    return (
        <div className="container estate-input-view">
            <h1 className="title">Estate Value</h1>
            <p className="subtitle">Enter the total value of the estate to be distributed.</p>
            
            <div className="input-card">
                <div className="input-group">
                    <label htmlFor="estate">Total Amount</label>
                    <input 
                        type="number" 
                        id="estate" 
                        placeholder="e.g. 240000" 
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                    />
                </div>
            </div>

            <div className="footer-actions">
                <button className="secondary-btn" onClick={onBack}>Back</button>
                <button 
                    className="primary-btn" 
                    disabled={!value || parseFloat(value) <= 0}
                    onClick={() => onCalculate(parseFloat(value))}
                >
                    Calculate Inheritance
                </button>
            </div>
        </div>
    );
};

export default EstateInput;
