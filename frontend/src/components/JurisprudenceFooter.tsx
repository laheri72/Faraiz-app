import React from 'react';

const JurisprudenceFooter: React.FC = () => {
    return (
        <footer className="mt-4 text-muted" style={{ fontSize: '0.8rem', textAlign: 'center', padding: '2rem' }}>
            <p>&copy; {new Date().getFullYear()} <a href="https://github.com/laheri72" target="_blank" rel="noopener noreferrer" style={{ color: 'inherit' }}>Laheri72</a>. All Rights Reserved.</p>
            <p style={{ fontStyle: 'italic' }}>Verified Jurisprudence Implementation • Layer 1-5 Engine</p>
        </footer>
    );
};

export default JurisprudenceFooter;
