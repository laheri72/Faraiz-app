import React, { useState } from 'react';
import HeirSelection from './pages/HeirSelection';
import EstateInput from './pages/EstateInput';
import ResultsView from './pages/ResultsView';
import { calculateInheritance } from './api/client';
import type { HeirInput, CalculationResult, VerificationData } from './types';
import './styles/App.css';

type Screen = 'HEIRS' | 'ESTATE' | 'RESULTS' | 'LOADING';

const App: React.FC = () => {
  const [screen, setScreen] = useState<Screen>('HEIRS');
  const [heirs, setHeirs] = useState<HeirInput[]>([]);
  const [results, setResults] = useState<CalculationResult[]>([]);
  const [verification, setVerification] = useState<VerificationData | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleHeirsSelected = (selectedHeirs: HeirInput[]) => {
    setHeirs(selectedHeirs);
    setScreen('ESTATE');
  };

  const handleCalculate = async (estateValue: number, debts: number, wasiyyah: number) => {
    setScreen('LOADING');
    setError(null);
    try {
      const response = await calculateInheritance({
        estate_value: estateValue,
        debts: debts,
        wasiyyah: wasiyyah,
        heirs: heirs
      });
      
      if (!response || !response.results) {
        throw new Error('Invalid response received from server.');
      }

      setResults(response.results);
      setVerification(response.verification || null);
      setScreen('RESULTS');
    } catch (err: any) {
      console.error('Calculation Error:', err);
      const detail = err.response?.data?.detail || err.message || 'An error occurred during calculation.';
      setError(detail);
      setScreen('ESTATE');
    }
  };

  const reset = () => {
    setHeirs([]);
    setResults([]);
    setVerification(null);
    setError(null);
    setScreen('HEIRS');
  };

  return (
    <div className="app-container">
      {error && <div className="error-banner">{error}</div>}
      
      {screen === 'HEIRS' && (
        <HeirSelection onNext={handleHeirsSelected} />
      )}
      
      {screen === 'ESTATE' && (
        <EstateInput 
          onBack={() => setScreen('HEIRS')} 
          onCalculate={handleCalculate} 
        />
      )}
      
      {screen === 'LOADING' && (
        <div className="container loading-view">
          <div className="loader">Calculating Jurisprudence...</div>
        </div>
      )}
      
      {screen === 'RESULTS' && (
        <ResultsView 
          results={results} 
          verification={verification}
          onBack={reset} 
        />
      )}
    </div>
  );
};

export default App;
