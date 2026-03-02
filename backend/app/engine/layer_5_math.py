from fractions import Fraction
from typing import Dict, List, Any
import math
from .models import CaseState, Heir

class MathEngine:
    @staticmethod
    def get_lcm(numbers: List[int]) -> int:
        if not numbers:
            return 1
        lcm = numbers[0]
        for i in range(1, len(numbers)):
            lcm = abs(lcm * numbers[i]) // math.gcd(lcm, numbers[i])
        return lcm

    @staticmethod
    def resolve_fractions(state: CaseState, estate_value: float) -> Dict[str, Any]:
        """
        Unifies all assigned fractions, calculates LCM, handles Radd,
        and converts to final currency amounts.
        """
        results = {}
        assignments = state.assignments # relation -> Fraction
        
        if not assignments:
            # If no fixed shares, we might need to handle priority-only distribution
            # For now, assume at least one assignment or remainder exists
            pass

        # 1. Identify all denominators for LCM
        denominators = [f.denominator for f in assignments.values()]
        base_lcm = MathEngine.get_lcm(denominators) if denominators else 1
        
        # 2. Calculate initial shares in terms of LCM
        shares_in_lcm = {rel: (frac.numerator * (base_lcm // frac.denominator)) 
                         for rel, frac in assignments.items()}
        
        total_shares_assigned = sum(shares_in_lcm.values())
        remainder_shares = base_lcm - total_shares_assigned
        
        # 3. Handle Radd (Return) if remainder exists
        # Principle 4: الرد بالرحم
        if remainder_shares > 0 and state.radd_eligible:
            # Radd is distributed among eligible heirs (usually those with fixed shares 
            # except Husband/Wife, but the specific rulebook says 'return by kinship')
            # For this engine, we'll distribute the remainder proportionally 
            # among Radd-eligible heirs based on their original shares.
            
            eligible_shares_sum = sum(shares_in_lcm[rel] for rel in state.radd_eligible if rel in shares_in_lcm)
            
            if eligible_shares_sum > 0:
                for rel in state.radd_eligible:
                    if rel in shares_in_lcm:
                        # Add proportional part of remainder
                        added_shares = (shares_in_lcm[rel] * remainder_shares) / eligible_shares_sum
                        shares_in_lcm[rel] += added_shares
                
                # Update total and denominator to reflect full distribution
                total_shares_assigned = base_lcm
                remainder_shares = 0

        # 4. Handle Ratio Distribution ( للذكر مثل حظ الأنثيين - V1/V15)
        # If specific ratios were flagged, we split the assigned share for that group
        final_results = []
        
        # Calculate the value of a single share
        # Total shares now equals the denominator (base_lcm) because of Radd or full assignment
        share_unit_value = estate_value / total_shares_assigned if total_shares_assigned > 0 else 0
        
        for heir in state.heirs:
            if heir.relation in state.excluded_heirs:
                continue
                
            # If relation has a direct assignment
            if heir.relation in shares_in_lcm:
                share_count = shares_in_lcm[heir.relation]
                
                # Check for male/female ratio within this group (e.g. Children)
                # This is a simplified version; real rules might split the group share
                if "V1" in state.applied_rules and heir.relation in ["Son", "Daughter"]:
                    # V1 applies to Children group
                    # We need the total ratio units: sons*2 + daughters*1
                    sons = sum(h.count for h in state.heirs if h.relation == "Son")
                    daughters = sum(h.count for h in state.heirs if h.relation == "Daughter")
                    total_units = (sons * 2) + daughters
                    
                    # Each unit value within the Children group share
                    # We treat the entire children share as one block to be split
                    # Note: In Daim al-Islam, children usually take the whole remainder.
                    # If V1 is applied, it usually means children are the primary heirs.
                    
                    unit_ratio_value = (share_count * share_unit_value) / total_units
                    heir_amount = unit_ratio_value * (2 if heir.relation == "Son" else 1)
                    heir_share_frac = f"{(2 if heir.relation == 'Son' else 1)}/{total_units} of Children Share"
                else:
                    heir_amount = share_count * share_unit_value
                    heir_share_frac = str(Fraction(int(share_count), int(total_shares_assigned)).limit_denominator())

                final_results.append({
                    "heir": heir.relation,
                    "count": heir.count,
                    "share": heir_share_frac,
                    "amount": round(heir_amount, 2)
                })

        return final_results
