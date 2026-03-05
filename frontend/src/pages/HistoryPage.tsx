import React from 'react';
import { Clock, ChevronRight, Trash2, Home } from 'lucide-react';
import { formatCurrencyIndian } from '../api/utils';

interface SavedCase {
  id: string;
  timestamp: number;
  estate: { value: number; debts: number; wasiyyah: number };
  heirs: any[];
  results: any[];
}

interface Props {
  history: SavedCase[];
  onSelect: (saved: SavedCase) => void;
  onDelete: (id: string) => void;
  onBack: () => void;
}

const HistoryPage: React.FC<Props> = ({ history, onSelect, onDelete, onBack }) => {
  return (
    <div className="animate-fade">
      <div className="page-statement">
        <h2 className="serif flex items-center gap-2">
          <Clock size={24} color="var(--primary)" />
          Calculation History
        </h2>
        <p>Access and review your previously performed jurisprudence calculations stored locally.</p>
      </div>

      {history.length === 0 ? (
        <div className="text-center" style={{ padding: '4rem 0', background: '#f9fafb', borderRadius: '0.5rem', border: '1px dashed var(--border)' }}>
          <Clock size={48} style={{ margin: '0 auto 1rem', color: 'var(--text-muted)', opacity: 0.5 }} />
          <p className="text-muted">No saved calculations found.</p>
          <button className="btn-primary mt-4" onClick={onBack}>Start New Calculation</button>
        </div>
      ) : (
        <div className="history-list" style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {history.map((item) => (
            <div 
              key={item.id} 
              className="history-card"
              style={{ 
                background: 'white', 
                border: '1px solid var(--border-elegant)', 
                borderRadius: '0.5rem',
                padding: '1rem',
                display: 'flex',
                justifyContent: 'between',
                alignItems: 'center',
                cursor: 'pointer',
                transition: 'transform 0.2s',
              }}
              onClick={() => onSelect(item)}
            >
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                  {new Date(item.timestamp).toLocaleString()}
                </div>
                <div style={{ fontWeight: '700', fontSize: '1.1rem', color: 'var(--primary)' }}>
                  Net Estate: ₹ {formatCurrencyIndian(item.estate.value - item.estate.debts - item.estate.wasiyyah)}
                </div>
                <div style={{ fontSize: '0.9rem', color: 'var(--secondary)' }}>
                  {item.heirs.length} Heir(s) identified
                </div>
              </div>
              
              <div className="flex gap-3 items-center">
                <button 
                  className="p-2 text-error hover:bg-red-50 rounded-full"
                  onClick={(e) => {
                    e.stopPropagation();
                    if(window.confirm('Delete this record?')) onDelete(item.id);
                  }}
                  title="Delete"
                >
                  <Trash2 size={18} />
                </button>
                <ChevronRight size={20} color="var(--border)" />
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="action-area" style={{ justifyContent: 'center', marginTop: '2rem' }}>
        <button className="btn-outline flex items-center gap-2" onClick={onBack}>
          <Home size={18} /> Back to Home
        </button>
      </div>
    </div>
  );
};

export default HistoryPage;
