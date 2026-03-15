import React, { useState, useMemo } from 'react';
import { BookOpen, ArrowLeft, Calculator, Search, Filter, Hash, Quote, ShieldAlert, Award, Replace, AlertTriangle, PlayCircle } from 'lucide-react';

interface Props {
    rules: any[];
    onBack: () => void;
    onStartCalculation: () => void;
}

const CategoryIcons: Record<string, React.ReactNode> = {
    'exclusion': <ShieldAlert size={18} className="text-error" />,
    'allocation': <Award size={18} className="text-gold" />,
    'substitution': <Replace size={18} className="text-accent" />,
    'eligibility': <Filter size={18} className="text-primary" />,
    'blocking': <AlertTriangle size={18} className="text-error" />,
    'mode_activation': <PlayCircle size={18} className="text-secondary" />,
    'final': <BookOpen size={18} className="text-main" />,
};

const CategoryLabels: Record<string, string> = {
    'exclusion': 'Al-Hajb (Exclusion Rules)',
    'allocation': 'Al-Fara\'id (Fixed Shares)',
    'substitution': 'Al-Tanzeel (Substitution)',
    'eligibility': 'General Eligibility',
    'blocking': 'Condition Blocks',
    'mode_activation': 'Case Type Triggers',
    'final': 'Final Resolution (Radd/Awal)',
};

const RuleBook: React.FC<Props> = ({ rules, onBack, onStartCalculation }) => {
    const [searchTerm, setSearchTerm] = useState('');
    const [activeCategory, setActiveCategory] = useState<string | null>(null);

    // Humanize technical conditions
    const humanizeCondition = (cond: any): string => {
        const target = cond.relation || cond.target_class || 'System';
        const val = cond.value;
        const op = cond.operator;

        switch (cond.fact) {
            case 'exists':
                return op === '==' && val === true ? `${target} must exist` : `${target} must NOT exist`;
            case 'count':
                if (op === '>') return `More than ${val} ${target}s must exist`;
                if (op === '==') return `Exactly ${val} ${target}(s) must exist`;
                if (op === '>=') return `At least ${val} ${target}(s) must exist`;
                return `${target} count ${op} ${val}`;
            case 'has_male':
                return op === '==' && val === true ? `${target} must have a male counterpart` : `${target} must NOT have a male counterpart`;
            case 'has_female':
                return op === '==' && val === true ? `${target} must have a female counterpart` : `${target} must NOT have a female`;
            case 'is_killer':
                return `${target} is designated as a killer`;
            case 'is_different_religion':
                return `${target} follows a different religion`;
            case 'active_mode':
                return op === '!=' ? `Case type is NOT ${val}` : `Case type is ${val}`;
            default:
                return `${cond.fact} ${op} ${val}`;
        }
    };

    const renderConditions = (conditions: any) => {
        if (!conditions || Object.keys(conditions).length === 0) return null;
        
        return (
            <div className="flex flex-col gap-2 mt-3 pt-3 border-t border-dashed border-elegant">
                <div className="text-[11px] text-muted uppercase font-bold tracking-wider">Engine Application Conditions:</div>
                <div className="flex flex-wrap gap-2">
                    {Object.entries(conditions).map(([logicalOp, condList]: [string, any], idx) => {
                        const logicalLabel = logicalOp.toUpperCase(); // ALL, ANY, NONE
                        
                        return (
                            <div key={idx} className="flex items-start gap-1 w-full">
                                {logicalLabel !== 'ALL' && <span className="text-[10px] font-bold text-accent px-1 py-0.5 bg-accent-light rounded">{logicalLabel}</span>}
                                <div className="flex flex-col gap-1 w-full">
                                    {(condList as any[]).map((cond: any, i: number) => (
                                        <div key={i} className="flex items-center px-2 py-1 bg-light border border-elegant rounded text-xs text-main w-full">
                                            <div className="w-1.5 h-1.5 rounded-full bg-gold mr-2 flex-shrink-0"></div>
                                            <span>{humanizeCondition(cond)}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    };

    const renderActions = (actions: any[]) => {
        if (!actions || actions.length === 0) return null;
        
        return (
            <div className="flex flex-col gap-2 mt-3 pt-3 border-t border-dashed border-elegant">
                <div className="text-[11px] text-muted uppercase font-bold tracking-wider">Legal Decree (Effect):</div>
                <div className="flex flex-col gap-1.5">
                    {actions.map((act: any, i: number) => {
                        let text = '';
                        let colorClass = 'text-main bg-white border-elegant';
                        
                        if (act.type === 'assign_fraction') {
                            text = `Allocate fixed share of ${act.value} to ${act.target}`;
                            colorClass = 'text-primary bg-primary-light border-primary bg-opacity-10';
                        } else if (act.type === 'exclude_heir') {
                            text = `Exclude ${act.target} from inheritance (Mahjub)`;
                            colorClass = 'text-error bg-red-50 border-error';
                        } else if (act.type === 'assign_remainder') {
                            text = `Allocate entire remainder to ${act.target}`;
                            colorClass = 'text-gold-dark bg-yellow-50 border-gold';
                        } else if (act.type === 'substitute_relation') {
                            text = `Elevate ${act.source} to inherit the share of ${act.target} (as ${act.as_relation})`;
                            colorClass = 'text-accent bg-accent-light border-accent bg-opacity-10';
                        } else if (act.type === 'set_mode') {
                            text = `Trigger special jurisprudence mode: ${act.target}`;
                            colorClass = 'text-secondary bg-gray-50 border-secondary';
                        } else {
                            text = `${act.type}: ${act.target || ''} ${act.value || ''}`;
                        }

                        return (
                            <div key={i} className={`px-2 py-1.5 border rounded text-xs font-medium flex items-center gap-2 ${colorClass}`}>
                                <div className="h-1.5 w-1.5 rounded-sm bg-current opacity-70"></div>
                                {text}
                            </div>
                        );
                    })}
                </div>
            </div>
        );
    };

    // Filter and group rules
    const filteredAndGroupedRules = useMemo(() => {
        const filtered = rules.filter(rule => {
            const matchesSearch = 
                rule.rule_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                rule.meaning.toLowerCase().includes(searchTerm.toLowerCase()) ||
                rule.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                rule.arabic_text.includes(searchTerm);
            
            const matchesCategory = activeCategory ? rule.category === activeCategory : true;
            
            return matchesSearch && matchesCategory;
        });

        // Group by category
        const groups: Record<string, any[]> = {};
        for (const rule of filtered) {
            const cat = rule.category || 'other';
            if (!groups[cat]) groups[cat] = [];
            groups[cat].push(rule);
        }

        // Sort groups by priority of first rule
        const sortedCategories = Object.keys(groups).sort((a, b) => {
            return groups[a][0].priority - groups[b][0].priority;
        });

        return { groups, sortedCategories, count: filtered.length };
    }, [rules, searchTerm, activeCategory]);

    // Extract unique categories for the filter chips
    const allCategories = useMemo(() => {
        return Array.from(new Set(rules.map(r => r.category || 'other')));
    }, [rules]);

    return (
        <div className="rule-book animate-fade pb-10">
            {/* Header Actions */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 no-print">
                <button className="btn-outline flex items-center justify-center gap-2 py-2" onClick={onBack}>
                    <ArrowLeft size={18} /> Exit RuleBook
                </button>
                <button className="btn-primary flex items-center justify-center gap-2 py-2" onClick={onStartCalculation}>
                    <Calculator size={18} /> Try a Calculation
                </button>
            </div>

            <div className="page-statement mb-8">
                <div className="flex flex-col items-center gap-3">
                    <div className="p-3 bg-primary rounded-2xl text-white shadow-lg shadow-primary/30">
                        <BookOpen size={28} />
                    </div>
                    <h1 className="serif mb-0 text-3xl sm:text-4xl text-center" style={{ fontFamily: "'Amiri', serif" }} dir="rtl">
                        دليل أحكام الفرائض
                    </h1>
                    <h2 className="serif text-primary text-xl m-0">Fatemi Jurisprudence Logic</h2>
                    <p className="text-center opacity-80 text-sm max-w-lg mt-1">
                        A transparent guide to how the system engine applies the deterministic inheritance rules documented in Daʿāʾim al-Islām.
                    </p>
                </div>
            </div>

            {/* Smart Filters & Search */}
            <div className="card p-4 sm:p-5 mb-8 bg-white border-elegant shadow-sm sticky top-0 z-10">
                <div className="relative w-full mb-4">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-muted" size={18} />
                    <input 
                        type="text" 
                        placeholder="Search by ID, meaning, or Arabic text..." 
                        className="w-full pl-10 pr-4 py-3 rounded-xl border-2 border-elegant focus:border-primary outline-none transition-colors"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                
                <div className="flex flex-wrap items-center gap-2">
                    <button 
                        className={`text-xs px-3 py-1.5 rounded-full border transition-all ${activeCategory === null ? 'bg-primary text-white border-primary font-bold shadow-sm' : 'bg-light text-muted border-elegant hover:border-primary'}`}
                        onClick={() => setActiveCategory(null)}
                    >
                        All Categories
                    </button>
                    {allCategories.map(cat => (
                        <button 
                            key={cat}
                            className={`text-xs px-3 py-1.5 rounded-full border transition-all flex items-center gap-1.5
                                ${activeCategory === cat ? 'bg-primary text-white border-primary font-bold shadow-sm' : 'bg-light text-muted border-elegant hover:border-primary'}`}
                            onClick={() => setActiveCategory(cat)}
                        >
                            {CategoryIcons[cat]} {CategoryLabels[cat] || cat}
                        </button>
                    ))}
                </div>
            </div>

            {/* Rule Categories Loop */}
            {filteredAndGroupedRules.count > 0 ? (
                <div className="space-y-10">
                    {filteredAndGroupedRules.sortedCategories.map(cat => (
                        <div key={cat} className="space-y-4">
                            <div className="flex items-center gap-3 border-b-2 border-elegant pb-2 mb-4 px-2">
                                <span className="p-2 bg-light rounded-lg">
                                    {CategoryIcons[cat] || <BookOpen size={20} />}
                                </span>
                                <h3 className="serif text-xl font-bold text-main m-0">
                                    {CategoryLabels[cat] || (cat.charAt(0).toUpperCase() + cat.slice(1))}
                                </h3>
                                <span className="ml-auto text-xs font-bold text-muted bg-elegant px-2 py-0.5 rounded-full">
                                    {filteredAndGroupedRules.groups[cat].length} rules
                                </span>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-4">
                                {filteredAndGroupedRules.groups[cat].map((rule, index) => (
                                    <div key={index} className="card bg-white border-elegant hover:border-gold hover:shadow-md transition-all h-full flex flex-col">
                                        <div className="p-4 sm:p-5 flex-1">
                                            {/* Header */}
                                            <div className="flex justify-between items-start mb-4">
                                                <div className="flex flex-col gap-1">
                                                    <span className="bg-primary hover:bg-gold text-white text-[10px] font-mono font-bold px-2 py-0.5 rounded flex items-center gap-1 w-max transition-colors">
                                                        <Hash size={10} /> {rule.rule_id}
                                                    </span>
                                                    <span className="text-[10px] font-medium text-muted">Priority: {rule.priority}</span>
                                                </div>
                                                <span className="text-[10px] font-bold text-gold uppercase tracking-wider bg-gold bg-opacity-10 px-2 py-0.5 rounded">
                                                    {rule.source || 'Da\'aim'}
                                                </span>
                                            </div>
                                            
                                            {/* Arabic Fiqh Text */}
                                            {rule.arabic_text && rule.arabic_text !== '-' && (
                                                <div className="arabic-text text-xl sm:text-2xl text-right mb-5 leading-[1.8] border-r-4 border-primary pr-3 opacity-90">
                                                    {rule.arabic_text}
                                                </div>
                                            )}
                                            
                                            {/* Meaning/Translation */}
                                            <div className="flex gap-2 items-start mb-4 bg-light p-3 rounded-lg border border-border-elegant">
                                                <Quote size={14} className="text-secondary flex-shrink-0 mt-0.5" />
                                                <div className="text-sm font-medium text-main leading-snug">
                                                    {rule.meaning}
                                                </div>
                                            </div>

                                            <div className="mt-auto space-y-0.5">
                                                {/* Engine Triggers (Conditions) */}
                                                {renderConditions(rule.conditions)}
                                                
                                                {/* Engine Effects (Actions) */}
                                                {renderActions(rule.actions)}
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            ) : (
                <div className="p-16 text-center text-muted italic bg-white rounded-2xl shadow-sm border border-elegant flex flex-col items-center gap-3">
                    <Search size={40} className="text-border opacity-50 mb-2" />
                    <span style={{ fontFamily: "'Amiri', serif", fontSize: '1.4rem' }}>لا توجد أحكام مطابقة لكحثك</span>
                    <span className="text-lg">No Fiqh rules match your current filters.</span>
                    <button onClick={() => { setSearchTerm(''); setActiveCategory(null); }} className="mt-2 text-primary font-bold hover:underline">
                        Clear all filters
                    </button>
                </div>
            )}
        </div>
    );
};

export default RuleBook;
