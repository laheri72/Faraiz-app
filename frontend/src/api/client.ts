import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export interface HeirInput {
    relation: string;
    gender: string;
    count: number;
}

export interface CalculationRequest {
    estate_value: number;
    heirs: HeirInput[];
}

export interface CalculationResult {
    heir: string;
    share: string;
    amount: number;
    rules_used: string[];
    arabic_reasoning: string[];
}

export interface CalculationResponse {
    case_id: number;
    results: CalculationResult[];
}

export const calculateInheritance = async (data: CalculationRequest): Promise<CalculationResponse> => {
    const response = await axios.post(`${API_URL}/calculate`, data);
    return response.data;
};

export const getCase = async (caseId: number): Promise<CalculationResponse> => {
    const response = await axios.get(`${API_URL}/cases/${caseId}`);
    return response.data;
};
