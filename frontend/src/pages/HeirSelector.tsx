import React, { useState, useMemo, useEffect } from 'react';
import { createPortal } from 'react-dom';
import type { HeirInput } from '../types';
import { User } from 'lucide-react';
import RelationCard from '../components/RelationCard';
import SelectionAudit from '../components/SelectionAudit';

interface Props {
    currentHeirs: HeirInput[];
    onBack: () => void;
    onHeirChange: (heirs: HeirInput[]) => void;
}

interface RelationInfo {
    relation: string;
    arabic?: string;
    relation_type: string;
    lineage: string;
    gender: string;
    max: number;
    category: string;
    generation_level: number;
}

const AVAILABLE_RELATIONS: RelationInfo[] = [
    // --- DIRECT ---
    { relation: 'Father', arabic: 'الاب', relation_type: 'Father', lineage: 'direct', gender: 'M', max: 1, category: 'Parents', generation_level: 1 },
    { relation: 'Mother', arabic: 'الام', relation_type: 'Mother', lineage: 'direct', gender: 'F', max: 1, category: 'Parents', generation_level: 1 },
    { relation: 'Husband', arabic: 'الزوج', relation_type: 'Husband', lineage: 'direct', gender: 'M', max: 1, category: 'Spouse', generation_level: 1 },
    { relation: 'Wife', arabic: 'الزوجة', relation_type: 'Wife', lineage: 'direct', gender: 'F', max: 4, category: 'Spouse', generation_level: 1 },
    { relation: 'Son', arabic: 'الابن', relation_type: 'Son', lineage: 'direct', gender: 'M', max: 20, category: 'Children', generation_level: 1 },
    { relation: 'Daughter', arabic: 'البنت', relation_type: 'Daughter', lineage: 'direct', gender: 'F', max: 20, category: 'Children', generation_level: 1 },

    // --- GRANDPARENTS ---
    { relation: 'PGF (Jad) [Father Side]', arabic: 'الجد للأب', relation_type: 'grandfather_paternal', lineage: 'paternal', gender: 'M', max: 1, category: 'Grandparents', generation_level: 2 },
    { relation: 'PGM (Jaddah) [Father Side]', arabic: 'الجدة للأب', relation_type: 'grandmother_paternal', lineage: 'paternal', gender: 'F', max: 3, category: 'Grandparents', generation_level: 2 },
    { relation: 'MGF (Jad) [Mother Side]', arabic: 'الجد للأم', relation_type: 'grandfather_maternal', lineage: 'maternal', gender: 'M', max: 1, category: 'Grandparents', generation_level: 2 },
    { relation: 'MGM (Jaddah) [Mother Side]', arabic: 'الجدة للأم', relation_type: 'grandmother_maternal', lineage: 'maternal', gender: 'F', max: 3, category: 'Grandparents', generation_level: 2 },

    // --- DESCENDANTS ---
    { relation: 'Son of Son', arabic: 'ابن الابن', relation_type: 'Son_of_Son', lineage: 'paternal_descendant', gender: 'M', max: 20, category: 'Grandchildren', generation_level: 2 },
    { relation: 'Daughter of Son', arabic: 'بنت الابن', relation_type: 'Daughter_of_Son', lineage: 'paternal_descendant', gender: 'F', max: 20, category: 'Grandchildren', generation_level: 2 },
    { relation: 'Son of Daughter', arabic: 'ابن البنت', relation_type: 'Son_of_Daughter', lineage: 'maternal_descendant', gender: 'M', max: 20, category: 'Grandchildren', generation_level: 2 },
    { relation: 'Daughter of Daughter', arabic: 'بنت البنت', relation_type: 'Daughter_of_Daughter', lineage: 'maternal_descendant', gender: 'F', max: 20, category: 'Grandchildren', generation_level: 2 },

    // --- SIBLINGS (PATERNAL/FULL) ---
    { relation: 'Brother', arabic: 'الأخ', relation_type: 'Brother', lineage: 'paternal', gender: 'M', max: 20, category: 'Siblings', generation_level: 1 },
    { relation: 'Sister', arabic: 'الأخت', relation_type: 'Sister', lineage: 'paternal', gender: 'F', max: 20, category: 'Siblings', generation_level: 1 },

    // --- SIBLINGS (MATERNAL) ---
    { relation: 'Maternal Brother', arabic: 'الأخ للأم', relation_type: 'Brother_Maternal', lineage: 'maternal', gender: 'M', max: 20, category: 'Maternal Sibs', generation_level: 1 },
    { relation: 'Maternal Sister', arabic: 'الأخت للأم', relation_type: 'Sister_Maternal', lineage: 'maternal', gender: 'F', max: 20, category: 'Maternal Sibs', generation_level: 1 },

    // --- NEPHEWS ---
    { relation: 'Son of Brother', arabic: 'ابن الأخ', relation_type: 'Son_of_Brother', lineage: 'paternal', gender: 'M', max: 20, category: 'Nephews', generation_level: 2 },
    { relation: 'Son of Sister', arabic: 'ابن الأخت', relation_type: 'Son_of_Sister', lineage: 'maternal', gender: 'M', max: 20, category: 'Nephews', generation_level: 2 },

    // --- EXTENDED ---
    { relation: 'Paternal Uncle', arabic: 'العم', relation_type: 'Paternal_Uncle', lineage: 'paternal', gender: 'M', max: 20, category: 'Uncles/Aunts', generation_level: 2 },
    { relation: 'Paternal Aunt', arabic: 'العمة', relation_type: 'Paternal_Aunt', lineage: 'paternal', gender: 'F', max: 20, category: 'Uncles/Aunts', generation_level: 2 },
    { relation: 'Maternal Uncle', arabic: 'الخال', relation_type: 'Maternal_Uncle', lineage: 'maternal', gender: 'M', max: 20, category: 'Uncles/Aunts', generation_level: 2 },
    { relation: 'Maternal Aunt', arabic: 'الخالة', relation_type: 'Maternal_Aunt', lineage: 'maternal', gender: 'F', max: 20, category: 'Uncles/Aunts', generation_level: 2 }
];

const HeirSelector: React.FC<Props> = ({ currentHeirs, onBack, onHeirChange }) => {
    const [deceasedGender, setDeceasedGender] = useState<'M' | 'F' | null>(currentHeirs.length > 0 ? (currentHeirs.some(h => h.relation_type === 'Husband') ? 'F' : 'M') : null);
    const [selectedHeirs, setSelectedHeirs] = useState<HeirInput[]>(currentHeirs);
    const [toast, setToast] = useState<{ relation: string, arabic?: string, count: number, id: number } | null>(null);

    useEffect(() => {
        if (toast) {
            const timer = setTimeout(() => setToast(null), 2000);
            return () => clearTimeout(timer);
        }
    }, [toast]);

    useEffect(() => {
        const topElement = document.getElementById('heir-selector-top');
        if (topElement) {
            topElement.scrollIntoView({ behavior: 'smooth' });
        }
    }, [deceasedGender]);

    const filteredRelations = useMemo(() => {
        if (!deceasedGender) return [];
        return AVAILABLE_RELATIONS.filter(item => {
            if (deceasedGender === 'M' && item.relation_type === 'Husband') return false;
            if (deceasedGender === 'F' && item.relation_type === 'Wife') return false;
            return true;
        });
    }, [deceasedGender]);

    const categories = useMemo(() => {
        const cats = Array.from(new Set(filteredRelations.map(r => r.category)));
        return cats;
    }, [filteredRelations]);

    const triggerHaptic = () => {
        if (window.navigator.vibrate) {
            window.navigator.vibrate(10);
        }
    };

    const handleAdd = (item: RelationInfo) => {
        triggerHaptic();
        const existingIndex = selectedHeirs.findIndex(h => h.relation_type === item.relation_type && h.generation_level === item.generation_level);
        let currentCount = 1;

        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            if (newHeirs[existingIndex].count < item.max) {
                newHeirs[existingIndex].count += 1;
                setSelectedHeirs(newHeirs);
                currentCount = newHeirs[existingIndex].count;
            } else {
                currentCount = item.max;
            }
        } else {
            setSelectedHeirs([...selectedHeirs, {
                relation: item.relation,
                relation_type: item.relation_type,
                lineage: item.lineage,
                gender: item.gender,
                count: 1,
                generation_level: item.generation_level
            }]);
        }
        setToast({ relation: item.relation, arabic: item.arabic, count: currentCount, id: Date.now() });
    };

    const handleRemove = (relType: string, genLevel: number) => {
        triggerHaptic();
        const existingIndex = selectedHeirs.findIndex(h => h.relation_type === relType && h.generation_level === genLevel);
        if (existingIndex !== -1) {
            const newHeirs = [...selectedHeirs];
            let currentCount = 0;
            if (newHeirs[existingIndex].count > 1) {
                newHeirs[existingIndex].count -= 1;
                setSelectedHeirs(newHeirs);
                currentCount = newHeirs[existingIndex].count;
            } else {
                setSelectedHeirs(newHeirs.filter((_, idx) => idx !== existingIndex));
            }
            const item = AVAILABLE_RELATIONS.find(r => r.relation_type === relType && r.generation_level === genLevel);
            if (item) {
                setToast({ relation: item.relation, arabic: item.arabic, count: currentCount, id: Date.now() });
            }
        }
    };

    const handleClear = (relType: string, genLevel: number) => {
        triggerHaptic();
        setSelectedHeirs(prev => prev.filter(h => !(h.relation_type === relType && h.generation_level === genLevel)));
    };

    const handleNext = () => {
        if (selectedHeirs.length === 0) {
            const confirmNone = window.confirm("Caution: You haven't added any heirs. This will send all money to 'Bayt al-Maal'. Are you sure you want to proceed?");
            if (!confirmNone) return;
        }
        onHeirChange(selectedHeirs);
    };

    const handleAuditAdd = (relType: string, genLevel: number) => {
        const relInfo = AVAILABLE_RELATIONS.find(r => r.relation_type === relType && r.generation_level === genLevel);
        if (relInfo) handleAdd(relInfo);
    };


    if (!deceasedGender) {
        return (
            <div className="animate-fade">
                <div className="page-statement" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
                    <h2 className="serif mb-0" style={{ fontFamily: "'Amiri', serif", fontSize: '2rem', margin: 0 }} dir="rtl">
                        تحديد المتوفى
                    </h2>
                    <h3 className="serif text-primary" style={{ fontSize: '1.2rem', margin: 0, opacity: 0.9 }}>
                        Initial Identification
                    </h3>
                    <p style={{ textAlign: 'center', opacity: 0.8, fontSize: '0.9rem', marginTop: '0.5rem' }}>
                        Please identify the gender of the deceased (Marhum/Marhuma) to determine eligible heirs.
                    </p>
                </div>
                <div className="flex gap-2 justify-center mt-4">
                    <button className="btn-outline flex items-center gap-2" onClick={() => setDeceasedGender('M')}>
                        <User size={18} /> Male deceased
                    </button>
                    <button className="btn-outline flex items-center gap-2" onClick={() => setDeceasedGender('F')}>
                        <User size={18} /> Female deceased
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="animate-fade">
            <div className="page-statement" id="heir-selector-top" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', marginBottom: '2rem' }}>
                <h2 className="serif mb-0" style={{ fontFamily: "'Amiri', serif", fontSize: '2rem', margin: 0 }} dir="rtl">
                    الخطوة ٢: تحديد الورثة
                </h2>
                <h3 className="serif text-primary" style={{ fontSize: '1.2rem', margin: 0, opacity: 0.9 }}>
                    Step 2: Heir Selection
                </h3>
                <div style={{ textAlign: 'center', marginTop: '0.5rem', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.3rem' }}>
                    <p style={{ opacity: 0.8, fontSize: '0.85rem', margin: 0 }}>
                        Define the surviving family members of the deceased <strong>({deceasedGender === 'M' ? 'Marhum' : 'Marhuma'})</strong>.
                    </p>
                </div>
                <button className="text-link" style={{ fontSize: '0.85rem', color: 'var(--secondary)', marginTop: '0.5rem' }} onClick={() => { setDeceasedGender(null); setSelectedHeirs([]); }}>Change deceased gender</button>
            </div>

            <div className="heir-selection-grid">
                <div className="mobile-scroll-container" style={{ maxHeight: '70vh', overflowY: 'auto', paddingRight: '0.5rem' }}>
                    <div className="heir-list-grouped">
                        {categories.map(cat => (
                            <div key={cat} className="category-section mb-6">
                                <h3 className="serif text-gold mb-3" style={{ fontSize: '1.1rem', borderBottom: '1px solid var(--border-elegant)', paddingBottom: '0.3rem' }}>{cat}</h3>
                                <div className="grid gap-3">
                                    {filteredRelations.filter(r => r.category === cat).map(item => {
                                        const selected = selectedHeirs.find(h => h.relation_type === item.relation_type && h.generation_level === item.generation_level);
                                        return (
                                            <RelationCard
                                                key={`${item.relation_type}_${item.generation_level}`}
                                                relation={item.relation}
                                                arabic={item.arabic}
                                                count={selected ? selected.count : 0}
                                                max={item.max}
                                                onAdd={() => handleAdd(item)}
                                                onRemove={() => handleRemove(item.relation_type, item.generation_level)}
                                            />
                                        );
                                    })}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="audit-sidebar">
                    <SelectionAudit
                        heirs={selectedHeirs}
                        onAdd={handleAuditAdd}
                        onRemove={handleRemove}
                        onClear={handleClear}
                    />
                </div>
            </div>

            <div className="action-area">
                <button className="btn-outline" onClick={onBack}>Back: Estate</button>
                <button className="btn-primary" onClick={handleNext}>
                    Next: Case Summary
                </button>
            </div>

            {toast && createPortal(
                <div 
                    key={toast.id}
                    className="toast-fade"
                    style={{ 
                        position: 'fixed',
                        bottom: '5.5rem',
                        left: 0,
                        right: 0,
                        marginLeft: 'auto',
                        marginRight: 'auto',
                        width: 'max-content',
                        maxWidth: '90%',
                        backgroundColor: 'var(--text-main)',
                        color: 'white',
                        padding: '0.75rem 1.5rem',
                        borderRadius: '9999px',
                        boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.3)',
                        zIndex: 9999,
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        pointerEvents: 'none',
                        border: '1px solid var(--gold)',
                        animation: 'fadeIn 0.2s ease-out forwards'
                    }}
                >
                    <div className="flex items-center gap-3">
                        <span className="font-bold text-gold text-lg">{toast.count}</span>
                        <span className="text-sm opacity-90">x</span>
                        <span className="text-sm font-medium">{toast.relation}</span>
                        {toast.arabic && (
                            <>
                                <span className="opacity-50 mx-1">|</span>
                                <span style={{ fontFamily: "'Amiri', serif", fontSize: '1.2rem', color: 'var(--gold)', marginBottom: '-0.3rem' }} dir="rtl">{toast.arabic}</span>
                            </>
                        )}
                    </div>
                </div>,
                document.body
            )}
        </div>
    );
};

export default HeirSelector;
