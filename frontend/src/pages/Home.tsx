import React from 'react';

interface Props {
    onStart: () => void;
}

const Home: React.FC<Props> = ({ onStart }) => {
    return (
        <div className="home-hero">
            <h1 className="serif">An Expert System for Fatemi Jurisprudence</h1>
            <p>
                The <strong>Fatemi Wirasat Engine</strong> provides precise, deterministic inheritance 
                calculations based on the established jurisprudence of the Fatemi school of thought. 
                Navigate through the structured steps to determine legal shares with absolute clarity.
            </p>
            <button className="btn-primary" onClick={onStart}>
                Begin Calculation
            </button>
            <div className="mt-4">
                <small className="text-muted">Structured • Precise • Verified</small>
            </div>
        </div>
    );
};

export default Home;
