import json
import operator
from typing import Any, Dict, List, Optional, Tuple

class RulesEngine:
    """
    A lightweight Python rules engine that evaluates data against JSON-defined rules.
    Supports basic comparisons, nested branching, and default actions.
    """

    # Mapping string operators to Python operator functions for safe evaluation
    OPERATORS = {
        "<": operator.lt,
        ">": operator.gt,
        "==": operator.eq,
        "!=": operator.ne,
        "<=": operator.le,
        ">=": operator.ge
    }

    def __init__(self, config_path: str):
        """
        Initialize the engine by loading rules from a JSON file.
        """
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.rules = self.config.get("rules", [])
        self.default_action = self.config.get("default_action", "none")

    def evaluate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate the provided data against the ruleset.
        Returns a dictionary containing the action and any associated metadata.
        """
        result = self._evaluate_rules(self.rules, data)
        
        if result:
            return result
        
        # Return default action if no rules matched
        return {"action": self.default_action, "reason": "Default action triggered"}

    def _evaluate_rules(self, rules: List[Dict], data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Recursively evaluates a list of rules.
        """
        for rule in rules:
            field = rule.get("field")
            op_str = rule.get("operator")
            value = rule.get("value")
            
            # Skip rule if required fields are missing
            if not all([field, op_str]):
                continue

            # Get the actual value from data, default to None if missing
            data_value = data.get(field)
            if data_value is None:
                continue

            # Perform comparison
            op_func = self.OPERATORS.get(op_str)
            if not op_func:
                print(f"Warning: Unsupported operator '{op_str}'")
                continue

            if op_func(data_value, value):
                # Condition matched!
                
                # Check for branching (nested rules)
                if "then" in rule:
                    nested_result = self._evaluate_rules(rule["then"], data)
                    if nested_result:
                        return nested_result
                
                # If no nested rules matched or exist, return this rule's action
                if "action" in rule:
                    return {
                        "action": rule["action"],
                        "reason": rule.get("reason", "Rule condition met"),
                        "matched_field": field
                    }
        
        return None

# --- Demonstration ---
if __name__ == "__main__":
    # 1. Initialize engine
    engine = RulesEngine("rules_config.json")

    # 2. Define test cases
    test_cases = [
        {
            "name": "Low Credit Score",
            "data": {"credit_score": 550, "income": 70000, "employment_years": 5}
        },
        {
            "name": "High Income, Long Employment",
            "data": {"credit_score": 700, "income": 80000, "employment_years": 4}
        },
        {
            "name": "High Income, Short Employment",
            "data": {"credit_score": 700, "income": 80000, "employment_years": 1}
        },
        {
            "name": "Low Income",
            "data": {"credit_score": 700, "income": 30000, "employment_years": 10}
        }
    ]

    print(f"{'Test Case':<30} | {'Action':<15} | {'Reason'}")
    print("-" * 80)

    for case in test_cases:
        result = engine.evaluate(case["data"])
        print(f"{case['name']:<30} | {result['action']:<15} | {result['reason']}")
