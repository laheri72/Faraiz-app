import React, { useState } from 'react';
import { BookOpen, ArrowLeft, Calculator, Search, Filter, Hash, Quote } from 'lucide-react';

interface Props {
    rules: any[];
    onBack: () => void;
    onStartCalculation: () => void;
}

const RuleBook: React.FC<Props> = ({ rules, onBack, onStartCalculation }) => {
    const [searchTerm, setSearchTerm] = useState('');

    const filteredRules = rules.filter(rule => 
        rule.rule_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
        rule.meaning.toLowerCase().includes(searchTerm.toLowerCase()) ||
        rule.arabic_text.includes(searchTerm)
    );

    const renderConditions = (conditions: any) => {
        if (!conditions) return null;
        return (
            <div className="flex flex-wrap gap-1.5 mt-2">
                {Object.entries(conditions).map(([key, value]) => (
                    <div key={key} className="flex items-center px-2 py-0.5 bg-light border border-elegant rounded text-[10px] text-muted font-mono whitespace-nowrap overflow-hidden max-w-full">
                        <span className="font-bold text-primary mr-1">{key}:</span>
                        <span className="truncate">{typeof value === 'object' ? JSON.stringify(value) : String(value)}</span>
                    </div>
                ))}
            </div>
        );
    };

    return (
        <div className="rule-book animate-fade">
            {/* Header Actions - Optimized for Mobile */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 no-print">
                <button className="btn-outline flex items-center justify-center gap-2 py-2" onClick={onBack}>
                    <ArrowLeft size={18} /> Back to Home
                </button>
                <button className="btn-primary flex items-center justify-center gap-2 py-2" onClick={onStartCalculation}>
                    <Calculator size={18} /> Try a Calculation
                </button>
            </div>

            <div className="page-statement mb-8" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                <div className="flex items-center gap-3 mb-2" style={{ flexDirection: 'row-reverse' }}>
                    <div className="p-2 bg-primary rounded-lg text-white">
                        <BookOpen size={24} />
                    </div>
                    <h1 className="serif mb-0 text-3xl sm:text-4xl" style={{ fontFamily: "'Amiri', serif", margin: 0 }} dir="rtl">
                        أحكام الفرائض
                    </h1>
                </div>
                <h2 className="serif text-primary" style={{ fontSize: '1.2rem', margin: 0, opacity: 0.9 }}>
                    Engine Rule Book
                </h2>
                <p className="text-center opacity-80" style={{ fontSize: '0.9rem', marginTop: '0.3rem' }}>
                    Fatemi Inheritance Logic (Daʿāʾim al-Islām)
                </p>
            </div>

            {/* Search and Filter - Stacked on Mobile */}
            <div className="card p-4 mb-6 bg-light border-elegant flex flex-col gap-4">
                <div className="relative w-full">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" size={18} />
                    <input 
                        type="text" 
                        placeholder="Search rules..." 
                        className="w-full pl-10 pr-4 py-3 rounded-lg border border-elegant focus:border-primary outline-none text-base"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="flex items-center justify-between text-sm text-muted px-1">
                    <div className="flex items-center gap-2">
                        <Filter size={14} />
                        <span>{filteredRules.length} rules found</span>
                    </div>
                    {searchTerm && (
                        <button onClick={() => setSearchTerm('')} className="text-primary font-bold">Clear</button>
                    )}
                </div>
            </div>

            {/* Desktop Table View - Hidden on Mobile */}
            <div className="hidden-mobile overflow-x-auto rounded-xl border border-elegant shadow-sm">
                <table className="w-full border-collapse bg-white">
                    <thead>
                        <tr className="bg-primary text-white text-left">
                            <th className="p-4 serif font-medium">ID</th>
                            <th className="p-4 serif font-medium">Legal Meaning</th>
                            <th className="p-4 serif font-medium text-right">Arabic Source</th>
                            <th className="p-4 serif font-medium">Ref</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filteredRules.map((rule, index) => (
                            <tr key={index} className="border-b border-elegant hover:bg-light transition-colors">
                                <td className="p-4 font-mono text-sm font-bold text-primary">{rule.rule_id}</td>
                                <td className="p-4">
                                    <div className="text-sm font-bold text-main mb-1">{rule.meaning}</div>
                                    {renderConditions(rule.conditions)}
                                </td>
                                <td className="p-4 arabic-text text-xl" style={{ minWidth: '220px' }}>
                                    {rule.arabic_text}
                                </td>
                                <td className="p-4 text-xs font-bold text-secondary italic">
                                    {rule.source || 'Da\'aim'}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            {/* Mobile Card View - Hidden on Desktop */}
            <div className="show-mobile space-y-4">
                {filteredRules.length > 0 ? (
                    filteredRules.map((rule, index) => (
                        <div key={index} className="card p-5 bg-white border-elegant shadow-sm hover:border-gold transition-all">
                            <div className="flex justify-between items-start mb-3">
                                <span className="bg-primary-light text-white text-[10px] font-mono font-bold px-2 py-0.5 rounded flex items-center gap-1">
                                    <Hash size={10} /> {rule.rule_id}
                                </span>
                                <span className="text-[10px] font-bold text-gold uppercase tracking-wider">
                                    {rule.source || 'Da\'aim al-Islam'}
                                </span>
                            </div>
                            
                            <div className="arabic-text text-2xl text-right mb-4 leading-relaxed border-r-4 border-gold pr-3">
                                {rule.arabic_text}
                            </div>
                            
                            <div className="flex gap-2 items-start">
                                <Quote size={14} className="text-primary flex-shrink-0 mt-1" />
                                <div className="text-sm font-medium text-main leading-snug">
                                    {rule.meaning}
                                </div>
                            </div>

                            {rule.conditions && (
                                <div className="mt-4 pt-3 border-t border-dashed border-elegant">
                                    <div className="text-[10px] text-muted uppercase font-bold mb-1 opacity-60">Logic Conditions:</div>
                                    {renderConditions(rule.conditions)}
                                </div>
                            )}
                        </div>
                    ))
                ) : (
                    <div className="p-12 text-center text-muted italic bg-light rounded-xl border-2 border-dashed border-elegant flex flex-col items-center gap-2">
                        <span style={{ fontFamily: "'Amiri', serif", fontSize: '1.2rem' }}>لا توجد أحكام مطابقة</span>
                        <span>No rules match your search.</span>
                    </div>
                )}
            </div>

            {/* Footer Call to Action */}
            <div className="mt-10 mb-6 p-6 sm:p-10 bg-primary rounded-2xl text-white text-center shadow-xl relative overflow-hidden">
                {/* Decorative background element */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-white opacity-5 -mr-10 -mt-10 rounded-full"></div>
                
                <h3 className="serif text-xl sm:text-2xl mb-3 relative z-10">Verify a Distribution</h3>
                <p className="mb-6 opacity-90 text-sm sm:text-base max-w-md mx-auto relative z-10">
                    Apply these rules dynamically to any inheritance case using our expert system.
                </p>
                <button 
                    className="bg-gold hover:bg-white text-primary font-bold px-8 py-3 rounded-full transition-all flex items-center gap-3 mx-auto shadow-lg hover:scale-105 active:scale-95" 
                    onClick={onStartCalculation}
                >
                    <Calculator size={20} /> Begin Now
                </button>
            </div>
        </div>
    );
};

export default RuleBook;
