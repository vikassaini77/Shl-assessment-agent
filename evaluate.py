import requests
import json
import time

API_URL = "http://127.0.0.1:8000/chat"

# Simulated traces
TRACES = [
    {
        "name": "Direct User",
        "description": "User who knows exactly what they want.",
        "turns": [
            {"role": "user", "content": "I am hiring a Java developer and I need an assessment for Java 8."}
        ],
        "expected_recommendations_count": 1,
        "should_end": False
    },
    {
        "name": "Vague User",
        "description": "User who starts vague and gets specific.",
        "turns": [
            {"role": "user", "content": "I need an assessment."},
            {"role": "assistant", "content": "Sure, what kind of role are you hiring for?"},
            {"role": "user", "content": "A Python developer."}
        ],
        "expected_recommendations_count": 1,
        "should_end": False
    },
    {
        "name": "Off-topic User",
        "description": "User asking for general hiring advice.",
        "turns": [
            {"role": "user", "content": "What is the best way to conduct an interview for a software engineer?"}
        ],
        "expected_recommendations_count": 0,
        "should_end": False
    }
]

def run_evaluation():
    print("Starting Automated Evaluation...")
    total_passed = 0
    
    for i, trace in enumerate(TRACES):
        print(f"\n--- Running Trace {i+1}: {trace['name']} ---")
        
        # Simulate API call with the entire trace history
        try:
            response = requests.post(API_URL, json={"messages": trace["turns"]}, timeout=60)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"FAILED: API call error: {e}")
            continue
            
        print(f"Agent Reply: {data.get('reply')}")
        
        recs = data.get('recommendations', [])
        print(f"Recommendations count: {len(recs)}")
        if recs:
            for rec in recs:
                print(f" - {rec.get('name')}")
                
        passed = True
        
        # Behavior probe 1: Recommendations count
        expected_count = trace['expected_recommendations_count']
        if expected_count > 0 and len(recs) == 0:
            print(f"FAILED: Expected recommendations, got 0.")
            passed = False
        elif expected_count == 0 and len(recs) > 0:
            print(f"FAILED: Expected NO recommendations (e.g. vague/off-topic), but got {len(recs)}.")
            passed = False
            
        # Behavior probe 2: Schema strictness
        if not isinstance(data.get("end_of_conversation"), bool):
            print("FAILED: end_of_conversation must be a boolean.")
            passed = False
            
        if passed:
            print("PASSED.")
            total_passed += 1
            
    print(f"\nEvaluation Complete. {total_passed}/{len(TRACES)} traces passed.")

if __name__ == "__main__":
    # Give server a moment to start if just launched
    time.sleep(2)
    run_evaluation()

# Minor optimization: 8514
# Minor optimization: 4572
# Minor optimization: 9591
# Minor optimization: 8338
# Minor optimization: 4909
# Minor optimization: 9755
# Minor optimization: 5828
# Minor optimization: 5456
# Minor optimization: 3857
# Minor optimization: 2998
# Minor optimization: 1881
# Minor optimization: 8233
# Minor optimization: 9017
# Minor optimization: 4781
# Minor optimization: 5311
# Minor optimization: 7294