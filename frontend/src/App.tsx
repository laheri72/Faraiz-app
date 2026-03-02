import React, { useState } from 'react';
import HeirSelection from './pages/HeirSelection';
import EstateInput from './pages/EstateInput';
import ResultsView from './pages/ResultsView';
import { calculateInheritance } from './api/client';
import type { HeirInput, CalculationResult } from './types';
import './styles/App.css';

type Screen = 'HEIRS' | 'ESTATE' | 'RESULTS' | 'LOADING';

const App: React.FC = () => {
  const [screen, setScreen] = useState<Screen>('HEIRS');
  const [heirs, setHeirs] = useState<HeirInput[]>([]);
  const [results, setResults] = useState<CalculationResult[]>([]);
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
      setResults(response.results);
      setScreen('RESULTS');
    } catch (err: any) {
      console.error(err);
      setError(err.response?.data?.detail || 'An error occurred during calculation.');
      setScreen('ESTATE');
    }
  };

  const reset = () => {
    setHeirs([]);
    setResults([]);
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
          onBack={reset} 
        />
      )}
    </div>
  );
};

export default App;
