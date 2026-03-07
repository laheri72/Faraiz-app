import React, { useState } from 'react';

interface Props {
    initialData: { value: number, debts: number, wasiyyah: number };
    onNext: (value: number, debts: number, wasiyyah: number) => void;
}

const EstateInput: React.FC<Props> = ({ initialData, onNext }) => {
    const [value, setValue] = useState<string>(initialData.value ? initialData.value.toString() : '');
    const [debts, setDebts] = useState<string>(initialData.debts ? initialData.debts.toString() : '');
    const [wasiyyah, setWasiyyah] = useState<string>(initialData.wasiyyah ? initialData.wasiyyah.toString() : '');

    return (
        <div className="animate-fade">
            <h2 className="section-title serif">Step 1: Estate Information</h2>
            <p className="text-muted mb-4">
                Define the total value of the estate and any necessary legal deductions according to Layer 4 
                of the engine's jurisprudence model.
            </p>

            <div className="form-group">
                <label htmlFor="estate">Total Estate Amount</label>
                <input 
                    type="number" 
                    id="estate" 
                    placeholder="Enter total amount (e.g., 240,000)" 
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    onWheel={(e) => e.currentTarget.blur()}
                />
            </div>

            <div className="form-group">
                <label htmlFor="debts">Outstanding Debts & Funeral Expenses</label>
                <input 
                    type="number" 
                    id="debts" 
                    placeholder="Enter debts to be paid (e.g., 10,000)" 
                    value={debts}
                    onChange={(e) => setDebts(e.target.value)}
                    onWheel={(e) => e.currentTarget.blur()}
                />
            </div>

            <div className="form-group">
                <label htmlFor="wasiyyah">Wasiyyah (Valid Will — Max 1/3)</label>
                <input 
                    type="number" 
                    id="wasiyyah" 
                    placeholder="Enter will amount if applicable (e.g., 20,000)" 
                    value={wasiyyah}
                    onChange={(e) => setWasiyyah(e.target.value)}
                    onWheel={(e) => e.currentTarget.blur()}
                />
            </div>

            <div className="flex justify-between mt-4">
                <div />
                <button 
                    className="btn-primary" 
                    disabled={!value || parseFloat(value) <= 0}
                    onClick={() => onNext(parseFloat(value), parseFloat(debts || '0'), parseFloat(wasiyyah || '0'))}
                >
                    Next: Define Heirs
                </button>
            </div>
        </div>
    );
};

export default EstateInput;
