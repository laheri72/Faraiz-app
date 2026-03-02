import axios from 'axios';
import type { CalculationRequest, CalculationResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const client = axios.create({
    baseURL: `${API_BASE_URL}/api`,
    headers: {
        'Content-Type': 'application/json',
    },
});

export const calculateInheritance = async (data: CalculationRequest): Promise<CalculationResponse> => {
    try {
        const response = await client.post<CalculationResponse>('/calculate', data);
        return response.data;
    } catch (error) {
        console.error('Full error response:', error);
        throw new Error('Calculation service unavailable');
    }
};

export const getCase = async (caseId: number): Promise<CalculationResponse> => {
    try {
        const response = await client.get<CalculationResponse>(`/cases/${caseId}`);
        return response.data;
    } catch (error) {
        console.error('Full error response:', error);
        throw new Error('Calculation service unavailable');
    }
};
