import React from 'react';

const JurisprudenceFooter: React.FC = () => {
    return (
        <footer className="mt-4 text-muted" style={{ fontSize: '0.8rem', textAlign: 'center', padding: '2rem' }}>
            <p>&copy; {new Date().getFullYear()} Fatemi Fiqh Research. All Rights Reserved.</p>
            <p style={{ fontStyle: 'italic' }}>Verified Jurisprudence Implementation • Layer 1-5 Engine</p>
        </footer>
    );
};

export default JurisprudenceFooter;
