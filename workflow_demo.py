import asyncio
from workflow_engine import WorkflowEngine
from workflow_models import WorkflowRequest

async def main():
    engine = WorkflowEngine()

    # Define various test scenarios
    scenarios = [
        {
            "name": "Valid Small Transaction",
            "request": WorkflowRequest(request_id="REQ-001", payload={"amount": 500, "user_id": "user_123"})
        },
        {
            "name": "High Value Transaction",
            "request": WorkflowRequest(request_id="REQ-002", payload={"amount": 50000, "user_id": "user_456"})
        },
        {
            "name": "Invalid Payload (Missing User)",
            "request": WorkflowRequest(request_id="REQ-003", payload={"amount": 100})
        },
        {
            "name": "Retry Scenario",
            "request": WorkflowRequest(request_id="REQ-004", payload={"amount": 404, "user_id": "user_789"})
        },
        {
            "name": "Negative Amount (Reject)",
            "request": WorkflowRequest(request_id="REQ-005", payload={"amount": -50, "user_id": "user_000"})
        }
    ]

    print("\n" + "="*80)
    print(f"{'Request ID':<12} | {'Scenario':<30} | {'Outcome':<15} | {'Status'}")
    print("="*80)

    for scenario in scenarios:
        result = await engine.run(scenario["request"])
        
        outcome_str = result.outcome.value if result.outcome else "N/A"
        print(f"{result.request_id:<12} | {scenario['name']:<30} | {outcome_str:<15} | {result.status.value}")
        
        # Print audit trail for the first failed or manual review case as example
        if result.outcome == "manual_review" or result.status == "failed":
            print(f"\n  [Audit Trail for {result.request_id}]:")
            for log in result.audit_trail:
                print(f"    - {log.stage}: {log.details}")
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(main())
