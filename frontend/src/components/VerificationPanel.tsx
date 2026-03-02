import React from 'react';
import { CheckCircle } from 'lucide-react';
import type { VerificationData } from '../types';

interface Props {
    verification: VerificationData;
}

const VerificationPanel: React.FC<Props> = ({ verification }) => {
    return (
        <div className="verification-panel">
            <h3 className="serif flex items-center justify-center gap-2">
                <CheckCircle size={20} color="var(--success)" />
                Verification Audit
            </h3>
            <div className="verification-grid">
                <div className="v-item">
                    <span className="v-label">Net Estate</span>
                    <span className="v-value">{verification.estate_total.toLocaleString()}</span>
                </div>
                <div className="v-item">
                    <span className="v-label">Distributed</span>
                    <span className="v-value">{verification.total_distributed.toLocaleString()}</span>
                </div>
                <div className="v-item">
                    <span className="v-label">Fraction Sum</span>
                    <span className="v-value">{verification.fraction_sum}</span>
                </div>
            </div>
            <div style={{ marginTop: '1.5rem', fontWeight: '800', color: verification.status === 'VALID' ? 'var(--success)' : 'var(--error)' }}>
                SYSTEM STATUS: {verification.status}
            </div>
        </div>
    );
};

export default VerificationPanel;
