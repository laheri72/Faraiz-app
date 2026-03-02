import React from 'react';
import { BookOpen } from 'lucide-react';

interface Props {
    rules: string[];     // Rule names/meanings (e.g., "Mother receives 1/6...")
    reasoning: string[]; // Arabic script
}

const RuleExplanation: React.FC<Props> = ({ rules, reasoning }) => {
    if (!reasoning || reasoning.length === 0) return null;

    return (
        <div className="rule-box">
            <h5 className="flex items-center gap-2">
                <BookOpen size={14} /> Jurisprudence Basis
            </h5>
            {reasoning.map((text, idx) => (
                <div key={idx} className="rule-item" style={{ marginBottom: '1.25rem' }}>
                    <p className="arabic-text" style={{ marginBottom: '0.25rem' }}>{text}</p>
                    <p style={{ 
                        fontSize: '0.9rem', 
                        color: 'var(--accent)', 
                        borderLeft: '2px solid var(--gold)', 
                        paddingLeft: '0.75rem',
                        margin: 0,
                        fontStyle: 'italic'
                    }}>
                        {rules[idx] || "Constitutional Jurisprudence Rule"}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default RuleExplanation;
