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
            <h1 className="serif">An Expert System for Fatemi Jurisprudence</h1>
            <p>
                The <strong>Fatemi Wirasat Engine</strong> provides precise, deterministic inheritance 
                calculations based on the established jurisprudence of the Fatemi school of thought. 
                Navigate through the structured steps to determine legal shares with absolute clarity.
            </p>
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
