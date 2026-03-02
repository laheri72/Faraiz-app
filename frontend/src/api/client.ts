import axios from 'axios';
import type { CalculationRequest, CalculationResponse } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api';

export const calculateInheritance = async (data: CalculationRequest): Promise<CalculationResponse> => {
    const response = await axios.post(`${API_URL}/calculate`, data);
    return response.data;
};

export const getCase = async (caseId: number): Promise<CalculationResponse> => {
    const response = await axios.get(`${API_URL}/cases/${caseId}`);
    return response.data;
};
