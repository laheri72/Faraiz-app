import React, { useState } from 'react';
import { formatCurrencyIndian, numberToWords } from '../api/utils';

interface Props {
    initialData: { value: number, debts: number, wasiyyah: number };
    onNext: (value: number, debts: number, wasiyyah: number) => void;
}

const AmountPreview: React.FC<{ value: string, currency: string }> = ({ value, currency }) => {
    const numValue = parseFloat(value);
    if (isNaN(numValue) || numValue <= 0) return null;

    return (
        <div className="amount-preview animate-fade" style={{ marginTop: '0.5rem', fontSize: '0.85rem', color: 'var(--text-muted)', fontStyle: 'italic' }}>
            <span style={{ fontWeight: '700', color: 'var(--gold)' }}>{currency} {formatCurrencyIndian(numValue)}</span>
            <span style={{ margin: '0 0.5rem' }}>•</span>
            <span>{numberToWords(Math.floor(numValue))}</span>
        </div>
    );
};

const EstateForm: React.FC<Props> = ({ initialData, onNext }) => {
    const [value, setValue] = useState<string>(initialData.value ? initialData.value.toString() : '');
    const [debts, setDebts] = useState<string>(initialData.debts ? initialData.debts.toString() : '');
    const [wasiyyah, setWasiyyah] = useState<string>(initialData.wasiyyah ? initialData.wasiyyah.toString() : '');
    const [currency, setCurrency] = useState<string>('₹');

    const estateNum = parseFloat(value) || 0;
    const wasiyyahNum = parseFloat(wasiyyah) || 0;
    const maxWasiyyah = estateNum / 3;
    const isWasiyyahOverLimit = wasiyyahNum > maxWasiyyah;

    return (
        <div className="animate-fade">
            <div className="page-statement">
                <h2 className="serif">Step 1: Estate Information</h2>
                <p>Define the total value of the estate and any necessary legal deductions according to Fatemi Fiqh.</p>
            </div>

            <div className="form-content">
                <div className="form-group" style={{ position: 'relative' }}>
                    <div className="flex justify-between items-center mb-2">
                        <label htmlFor="estate" style={{ margin: 0 }}>Total Estate Amount</label>
                        <select 
                            value={currency} 
                            onChange={(e) => setCurrency(e.target.value)}
                            style={{ 
                                padding: '0.2rem 0.5rem', 
                                borderRadius: '0.25rem', 
                                border: '1px solid var(--border)',
                                background: 'white',
                                fontSize: '0.85rem'
                            }}
                        >
                            <option value="₹">₹ INR</option>
                            <option value="$">$ USD</option>
                            <option value="£">£ GBP</option>
                            <option value="د.ك">د.ك KWD</option>
                        </select>
                    </div>
                    <input 
                        type="number" 
                        id="estate" 
                        inputMode="decimal"
                        placeholder="Enter total amount (e.g., 240000)" 
                        value={value}
                        onChange={(e) => setValue(e.target.value)}
                    />
                    <AmountPreview value={value} currency={currency} />
                </div>

                <div className="form-group">
                    <label htmlFor="debts">Outstanding Debts & Funeral Expenses</label>
                    <input 
                        type="number" 
                        id="debts" 
                        inputMode="decimal"
                        placeholder="Enter debts (e.g., 10000)" 
                        value={debts}
                        onChange={(e) => setDebts(e.target.value)}
                    />
                    <AmountPreview value={debts} currency={currency} />
                </div>

                <div className="form-group">
                    <label htmlFor="wasiyyah">Wasiyyah (Valid Will — Max 1/3)</label>
                    <input 
                        type="number" 
                        id="wasiyyah" 
                        inputMode="decimal"
                        placeholder="Enter will amount (e.g., 20000)" 
                        value={wasiyyah}
                        onChange={(e) => setWasiyyah(e.target.value)}
                        style={{ borderColor: isWasiyyahOverLimit ? 'var(--error)' : 'var(--border)' }}
                    />
                    {isWasiyyahOverLimit && (
                        <p style={{ color: 'var(--error)', fontSize: '0.8rem', marginTop: '0.4rem', fontWeight: '600' }}>
                            ⚠ Wasiyyah is capped at 1/3 ({currency} {formatCurrencyIndian(Math.floor(maxWasiyyah))}). The engine will auto-adjust this.
                        </p>
                    )}
                    <AmountPreview value={wasiyyah} currency={currency} />
                </div>
            </div>

            <div className="action-area">
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

export default EstateForm;
