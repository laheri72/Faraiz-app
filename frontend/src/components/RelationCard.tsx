import { memo } from 'react';
import { Plus, Minus } from 'lucide-react';

interface Props {
    relation: string;
    arabic?: string;
    relation_type: string;
    generation_level: number;
    count: number;
    max: number;
    onAdd: (relType: string, genLevel: number) => void;
    onRemove: (relType: string, genLevel: number) => void;
}

// ⚡ Bolt: Wrapped in React.memo to prevent unnecessary re-renders when parent HeirSelector state changes
// Added stable onAdd/onRemove handlers to prevent reference changes
// Impact: Reduces re-renders of all ~20 RelationCards when a single relation count is updated
const RelationCard = memo(({ relation, arabic, relation_type, generation_level, count, max, onAdd, onRemove }: Props) => {
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
                <button className="btn-icon" disabled={count === 0} onClick={() => onRemove(relation_type, generation_level)}><Minus size={14} /></button>
                <span style={{ fontWeight: '800', minWidth: '1.5rem', textAlign: 'center' }}>{count}</span>
                <button className="btn-icon" disabled={count >= max} onClick={() => onAdd(relation_type, generation_level)}><Plus size={14} /></button>
            </div>
        </div>
    );
});

export default RelationCard;
