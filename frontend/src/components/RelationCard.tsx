import React from 'react';
import { Plus, Minus } from 'lucide-react';

interface Props {
    relation: string;
    count: number;
    max: number;
    onAdd: () => void;
    onRemove: () => void;
}

const RelationCard: React.FC<Props> = ({ relation, count, max, onAdd, onRemove }) => {
    return (
        <div className="heir-card">
            <div className="info">
                <span className="name">{relation}</span>
                <small className="text-muted">{max > 1 ? `Up to ${max}` : 'Unique relation'}</small>
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
