export interface HeirInput {
    relation: string;
    relation_type: string;
    lineage: string;
    gender: string;
    count: number;
    generation_level: number;
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
    share_percentage?: number;
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
    is_balanced?: boolean;
}

export interface CalculationRequest {
    estate_value: number;
    debts: number;
    wasiyyah: number;
    heirs: HeirInput[];
}

export interface CalculationStep {
    title: string;
    description: string;
    math_details?: string;
    items: string[];
}

export interface CalculationResponse {
    results: CalculationResult[];
    verification: VerificationData;
    calculation_steps: CalculationStep[];
}
