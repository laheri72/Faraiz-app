import React from 'react';
import { BookOpen } from 'lucide-react';

interface Props {
    rules: string[];
    arabicReasoning: string[];
}

const RuleExplanationPanel: React.FC<Props> = ({ rules, arabicReasoning }) => {
    if (!arabicReasoning || arabicReasoning.length === 0) return null;

    return (
        <div className="rule-box">
            <h5 className="flex items-center gap-2">
                <BookOpen size={14} /> Jurisprudence Rule
            </h5>
            {arabicReasoning.map((text, idx) => (
                <div key={idx} className="rule-item" style={{ marginBottom: '1rem' }}>
                    <p className="arabic-text">{text}</p>
                    <p style={{ fontSize: '0.85rem', color: 'var(--accent)', marginTop: '0.25rem' }}>
                        {rules[idx] || "Constitutional Rule"}
                    </p>
                </div>
            ))}
        </div>
    );
};

export default RuleExplanationPanel;
