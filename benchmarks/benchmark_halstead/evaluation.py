import importlib
import json

def evaluate_program(program, problem_id):
    try:
        module = importlib.import_module(program)
    except Exception as e:
        return f"Error importing module: {e}"

    try:
        with open(f"test_cases/test_cases_{problem_id}.json", "r") as f:
            test_cases = json.load(f)
    except Exception as e:
        return f"Error loading test cases: {e}"

    num_correct = 0
    total_tests = len(test_cases)

    for test_case in test_cases:
        input_data = test_case["input"]
        expected_output = test_case["output"]

        try:
            actual_output = module.solve(input_data)
        except Exception as e:
            return f"Error running function: {e}"

        if actual_output == expected_output:
            num_correct += 1

    accuracy_percentage = (num_correct / total_tests) * 100
    return accuracy_percentage

