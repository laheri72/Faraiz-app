import React from 'react';
import { Play, History, BookOpen } from 'lucide-react';

interface Props {
    onStart: () => void;
    onViewHistory: () => void;
    onViewRuleBook: () => void;
}

const Home: React.FC<Props> = ({ onStart, onViewHistory, onViewRuleBook }) => {
    return (
        <div className="home-hero">
            <div className="text-center mb-6" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
                <h1 className="serif mb-0" style={{ fontFamily: "'Amiri', serif", fontSize: '2.5rem', lineHeight: '1.2', margin: 0 }} dir="rtl">
                    حاسبة الفرائض الفاطمية
                </h1>
                <h2 className="serif text-primary" style={{ fontSize: '1.5rem', margin: 0, opacity: 0.9 }}>
                    Fatemi Wirasat Calculator
                </h2>
            </div>

            <div className="mb-8 max-w-2xl mx-auto" style={{ gap: '1.5rem', display: 'flex', flexDirection: 'column' }}>
                <p className="text-center" style={{ fontFamily: "'Amiri', serif", fontSize: '1.4rem', lineHeight: '1.8', margin: 0 }} dir="rtl">
                    نظام يعين على استخراج سهام الميراث<br />
                    بحسب فقه الدعوة الفاطمية<br />
                    كما ورد في كتاب دعائم الإسلام.<br />
                    <br />

                </p>

                <p className="text-center text-sm" style={{ opacity: 0.7, margin: 0, padding: '0 1rem', fontStyle: 'italic', lineHeight: '1.5' }}>
                    An expert system to help extract inheritance shares according to Fatemi jurisprudence as stated in Da'a'im al-Islam.<br />
                    Follow the outlined steps to show the share of each heir with complete clarity.
                </p>
            </div>
            <div className="flex flex-wrap gap-4 justify-center mt-6">
                <button className="btn-primary flex items-center gap-2" onClick={onStart}>
                    <Play size={18} /> Begin Calculation
                </button>
                <button className="btn-outline flex items-center gap-2" onClick={onViewRuleBook}>
                    <BookOpen size={18} /> Rule Book
                </button>
                <button className="btn-outline flex items-center gap-2" onClick={onViewHistory}>
                    <History size={18} /> View History
                </button>
            </div>
            <div className="mt-8">
                <small className="text-muted">Structured • Precise • Verified</small>
            </div>
        </div>
    );
};

export default Home;
