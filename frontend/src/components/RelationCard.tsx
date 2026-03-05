import React from 'react';
import { Plus, Minus } from 'lucide-react';

interface Props {
    relation: string;
    arabic?: string;
    count: number;
    max: number;
    onAdd: () => void;
    onRemove: () => void;
}

const RelationCard: React.FC<Props> = ({ relation, arabic, count, max, onAdd, onRemove }) => {
    return (
        <div className="heir-card">
            <div className="info">
                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.1rem' }}>
                    <span className="name">{relation}</span>
                    {arabic && <span className="arabic-tiny" style={{ 
                        fontSize: '0.85rem', 
                        color: 'var(--secondary)', 
                        fontWeight: '600',
                        opacity: 0.9,
                        fontFamily: 'Amiri, serif',
                        marginTop: '-2px'
                    }}>{arabic}</span>}
                </div>
                <small className="text-muted" style={{ marginTop: '0.2rem' }}>{max > 1 ? `Up to ${max}` : 'Unique relation'}</small>
            </div>
            <div className="count-actions">
                <button className="btn-icon" disabled={count === 0} onClick={onRemove}><Minus size={14} /></button>
                <span style={{ fontWeight: '800', minWidth: '1.5rem', textAlign: 'center' }}>{count}</span>
                <button className="btn-icon" disabled={count >= max} onClick={onAdd}><Plus size={14} /></button>
            </div>
        </div>
    );
};

export default RelationCard;
