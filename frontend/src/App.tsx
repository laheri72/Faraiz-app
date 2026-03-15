import React, { useState, useEffect } from 'react';
import Home from './pages/Home';
import HeirSelector from './pages/HeirSelector';
import EstateForm from './pages/EstateForm';
import CaseSummary from './pages/CaseSummary';
import ResultsDisplay from './pages/ResultsDisplay';
import HistoryPage from './pages/HistoryPage';
import RuleBook from './pages/RuleBook';
import JurisprudenceHeader from './components/JurisprudenceHeader';
import JurisprudenceFooter from './components/JurisprudenceFooter';
import { calculateInheritance, getRules } from './api/client';
import type { HeirInput, CalculationResult, VerificationData, CalculationStep } from './types';
import './styles/App.css';

type Step = 'HOME' | 'ESTATE' | 'HEIRS' | 'SUMMARY' | 'RESULTS' | 'LOADING' | 'HISTORY' | 'RULEBOOK';

interface SavedCase {
  id: string;
  timestamp: number;
  currency?: string;
  estate: { value: number; debts: number; wasiyyah: number };
  heirs: HeirInput[];
  results: CalculationResult[];
  calculation_steps?: CalculationStep[];
}

interface CaseState {
  step: Step;
  currency: string;
  estate: { value: number; debts: number; wasiyyah: number };
  heirs: HeirInput[];
  results: CalculationResult[];
  calculation_steps: CalculationStep[];
  verification: VerificationData | null;
  error: string | null;
  history: SavedCase[];
  engineRules: any[];
}

const INITIAL_STATE: CaseState = {
  step: 'HOME',
  currency: '₹',
  estate: { value: 0, debts: 0, wasiyyah: 0 },
  heirs: [],
  results: [],
  calculation_steps: [],
  verification: null,
  error: null,
  history: [],
  engineRules: []
};

const App: React.FC = () => {
  const [state, setState] = useState<CaseState>(() => {
    const saved = localStorage.getItem('fatemi_wirasat_case');
    if (saved) {
      const parsed = JSON.parse(saved);
      return { 
        ...INITIAL_STATE, 
        ...parsed,
        engineRules: parsed.engineRules || [] // Ensure it exists
      };
    }
    return INITIAL_STATE;
  });

  useEffect(() => {
    // Persist state to localStorage on every change (except loading/results resets)
    localStorage.setItem('fatemi_wirasat_case', JSON.stringify(state));
  }, [state]);

  const updateState = (updates: Partial<CaseState>) => {
    setState(prev => ({ ...prev, ...updates }));
  };

  const handleEstateSubmit = (value: number, debts: number, wasiyyah: number, currency: string) => {
    updateState({
      estate: { value, debts, wasiyyah },
      currency,
      step: 'HEIRS'
    });
  };

  const handleHeirsSubmit = (selectedHeirs: HeirInput[]) => {
    updateState({
      heirs: selectedHeirs,
      step: 'SUMMARY'
    });
  };

  const saveToHistory = (results: CalculationResult[], steps: CalculationStep[]) => {
    const newCase: SavedCase = {
      id: Math.random().toString(36).substr(2, 9),
      timestamp: Date.now(),
      currency: state.currency,
      estate: state.estate,
      heirs: state.heirs,
      results: results,
      calculation_steps: steps
    };
    updateState({ history: [newCase, ...state.history] });
  };

  const handleCalculate = async () => {
    updateState({ step: 'LOADING', error: null });
    try {
      const response = await calculateInheritance({
        estate_value: state.estate.value,
        debts: state.estate.debts,
        wasiyyah: state.estate.wasiyyah,
        heirs: state.heirs
      });

      if (!response || !response.results) {
        throw new Error('Invalid response received from server.');
      }

      saveToHistory(response.results, response.calculation_steps || []);

      updateState({
        results: response.results,
        calculation_steps: response.calculation_steps || [],
        verification: response.verification || null,
        step: 'RESULTS'
      });
    } catch (err: any) {
      console.error('Calculation Error:', err);
      const detail = err.response?.data?.detail || err.message || 'An error occurred during calculation.';
      updateState({ error: detail, step: 'SUMMARY' });
    }
  };

  const fetchRules = async () => {
    updateState({ step: 'LOADING', error: null });
    try {
        const rules = await getRules();
        updateState({ engineRules: rules, step: 'RULEBOOK' });
    } catch (err: any) {
        updateState({ error: err.message, step: 'HOME' });
    }
  };

  const loadFromHistory = (saved: SavedCase) => {
    updateState({
      currency: saved.currency || '₹',
      estate: saved.estate,
      heirs: saved.heirs,
      results: saved.results,
      calculation_steps: saved.calculation_steps || [],
      step: 'RESULTS',
      verification: null
    });
  };

  const reset = () => {
    updateState({
      step: 'HOME',
      currency: '₹',
      estate: { value: 0, debts: 0, wasiyyah: 0 },
      heirs: [],
      results: [],
      verification: null,
      error: null
    });
  };

  const getStepNumber = (): number => {
    switch (state.step) {
      case 'ESTATE': return 1;
      case 'HEIRS': return 2;
      case 'SUMMARY': return 3;
      case 'LOADING': return 3;
      case 'RESULTS': return 4;
      case 'HISTORY': return 0;
      default: return 0;
    }
  };

  return (
    <div className="app-container">
      <JurisprudenceHeader
        step={getStepNumber()}
        onHome={() => updateState({ step: 'HOME' })}
        onHistory={() => updateState({ step: 'HISTORY' })}
      />

      {state.error && (
        <div className="error-banner" style={{ color: 'var(--error)', margin: '1rem', fontWeight: 'bold', background: '#fee2e2', padding: '1rem', borderRadius: '0.25rem' }}>
          {state.error}
        </div>
      )}

      <main className="container animate-fade">
        {state.step === 'HOME' && (
          <Home 
            onStart={() => updateState({ step: 'ESTATE' })} 
            onViewHistory={() => updateState({ step: 'HISTORY' })}
            onViewRuleBook={fetchRules}
          />
        )}

        {state.step === 'RULEBOOK' && (
          <RuleBook 
            rules={state.engineRules}
            onBack={() => updateState({ step: 'HOME' })}
            onStartCalculation={() => updateState({ step: 'ESTATE' })}
          />
        )}
        {state.step === 'HISTORY' && (
          <HistoryPage
            history={state.history}
            onSelect={loadFromHistory}
            onDelete={(id) => updateState({ history: state.history.filter(h => h.id !== id) })}
            onBack={() => updateState({ step: 'HOME' })}
          />
        )}

        {state.step === 'ESTATE' && (
          <EstateForm
            initialData={state.estate}
            initialCurrency={state.currency}
            onNext={handleEstateSubmit}
            onBack={() => updateState({ step: 'HOME' })}
          />
        )}

        {state.step === 'HEIRS' && (
          <HeirSelector
            currentHeirs={state.heirs}
            onBack={() => updateState({ step: 'ESTATE' })}
            onHeirChange={handleHeirsSubmit}
          />
        )}

        {state.step === 'SUMMARY' && (
          <CaseSummary
            caseState={{ estate: state.estate, heirs: state.heirs, currency: state.currency }}
            onBack={() => updateState({ step: 'HEIRS' })}
            onCalculate={handleCalculate}
          />
        )}

        {state.step === 'LOADING' && (
          <div className="text-center" style={{ padding: '4rem 0' }}>
            <h2 className="serif">Processing Jurisprudence...</h2>
            <p>Applying the rules of Fatemi Fiqh to the provided case.</p>
            <div className="loader mt-4" style={{ fontSize: '2rem' }}>⏳</div>
          </div>
        )}

        {state.step === 'RESULTS' && (
          <ResultsDisplay
            results={state.results}
            calculation_steps={state.calculation_steps}
            verification={state.verification}
            currency={state.currency}
            onBack={reset}
          />
        )}
      </main>

      <JurisprudenceFooter />
    </div>
  );
};

export default App;
