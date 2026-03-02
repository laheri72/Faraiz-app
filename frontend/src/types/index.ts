export interface HeirInput {
    relation: string;
    gender: string;
    count: number;
    is_killer?: boolean;
    is_different_religion?: boolean;
    is_illegitimate?: boolean;
    is_missing?: boolean;
}

export interface CalculationRequest {
    estate_value: number;
    debts?: number;
    wasiyyah?: number;
    heirs: HeirInput[];
}

export interface CalculationResult {
    heir_id: string;
    relation: string;
    share: string;
    amount: number;
    rules_used: string[];
    arabic_reasoning: string[];
}

export interface VerificationData {
    estate_total: number;
    total_distributed: number;
    fraction_sum: string;
    status: 'VALID' | 'INVALID';
}

export interface CalculationResponse {
    case_id: number;
    results: CalculationResult[];
    verification: VerificationData;
}
