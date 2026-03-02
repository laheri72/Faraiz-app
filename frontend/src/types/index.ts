export interface HeirInput {
    relation: string;
    gender: string;
    count: number;
    is_killer?: boolean;
    is_different_religion?: boolean;
    is_illegitimate?: boolean;
    is_missing?: boolean;
}

export interface CalculationResult {
    heir_id: string;
    relation: string;
    share: string;
    amount: number;
    rules_used: string[];
    arabic_reasoning: string[];
    is_blocked: boolean;
    blocked_by?: string | null;
    blocking_rule_id?: string | null;
}

export interface VerificationData {
    estate_total: number;
    total_distributed: number;
    fraction_sum: string;
    status: 'VALID' | 'INVALID';
}

export interface CalculationRequest {
    estate_value: number;
    debts: number;
    wasiyyah: number;
    heirs: HeirInput[];
}

export interface CalculationResponse {
    results: CalculationResult[];
    verification: VerificationData;
}
