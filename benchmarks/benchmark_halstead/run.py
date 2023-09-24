import openai
import json
import os
import inspect
from tqdm import tqdm  # Import the tqdm module

# Replace 'YOUR_OPENAI_API_KEY_HERE' with your actual API key
openai.api_key = 'YOUR_OPENAI_API_KEY_HERE'

def get_openai_solution(prompt):
    messages=[
        {"role": "user", "content": f"{prompt} Respond only with your python solution in proper python formatting. Omit all explanations. Omit all descriptions. Don't say \"here is your code\" or similar remarks."},
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=messages,
        )

        solution = response['choices'][0]['message']['content']

        if "```python" in solution:
            solution = solution[len("```python"):]
        if "```" in solution:
            solution = solution[:solution.find("```")]
        return solution
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def halstead_difficulty(code):
    operators = {'+', '-', '*', '/', '%', '//', '**', '<<', '>>', '&', '|', '^', '~', '<', '>', '<=', '>=', '==', '!=', 
                 'and', 'or', 'not', 'is', 'in', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '//=', '**=',
                 '(', ')', '[', ']', '{', '}', '@', ',', ':', '.', '=', '->', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '//=', '**=', ';'}
    
    words = code.replace('\n', ' ').replace('\t', ' ').split(' ')
    operands = [word for word in words if not any(op in word for op in operators) and word]
    
    operator_count = sum(code.count(op) for op in operators)
    operand_count = len(operands)
    
    unique_operators = len(set(op for op in code.split() if op in operators))
    unique_operands = len(set(operands))
    
    difficulty = (unique_operators / 2) * (operand_count / unique_operands)
    
    return difficulty

def run_test_cases(solution_code, test_cases):
    # Create a list to store the results of each test case (True for passed, False for failed)
    results = []

    # Define a namespace dictionary to execute the solution_code in
    namespace = {}
    try:
        # Dynamically execute the solution_code
        exec(solution_code, namespace)
    except Exception as e:
        print(f"An error occurred while executing the solution code: {e}")
        # If the solution_code fails to execute, return 0 (indicating all test cases failed)
        return [0, None]
    
    # Get the solve function from the namespace
    solve = namespace.get('solve')
    if not solve:
        print("No 'solve' function found in the solution code.")
        # If no 'solve' function is found, return 0 (indicating all test cases failed)
        return [0, None]

    difficulty = halstead_difficulty(solution_code)

    # Run each test case and check if the output of the 'solve' function matches the expected output
    for test_case in test_cases:
        input_data = test_case['input']
        expected_output = test_case['output']
        
        try:
            # Call the 'solve' function with the input data and check if the output matches the expected output
            output = solve(input_data)
            results.append(output == expected_output)
        except Exception as e:
            print(f"An error occurred while running a test case: {e}")
            results.append(False)

    # Return the number of passed test cases
    return [sum(results), difficulty]


def run_benchmark(model_wrapper):
    # Load the problems from the JSON file
    with open('problems_halstead.json') as f:
        problems = json.load(f)
    
    total_test_cases = 0
    passed_test_cases = 0
    total_difficulty = 0

    # Iterate over each problem and generate a solution using OpenAI's API
    for problem in tqdm(problems):  # Wrap your loop with tqdm() to display a progress bar
        problem_id = problem['problem_id']
        problem_description = problem['description']
        
        # Step 1: Get a solution from OpenAI
        solution = model_wrapper.generate_solution(problem_description)
        
        # Step 2: Load the test cases for this problem
        with open(f'test_cases/test_cases_{problem_id}.json') as f:
            test_cases = json.load(f)
        
        # Step 3: Run the test cases on the generated solution
        result = run_test_cases(solution, test_cases)
        
        # Step 4: Update the test case counters
        total_test_cases += len(test_cases)
        passed_test_cases += result[0]
        if result[1]:
            total_difficulty += result[1]
    
    # Report the total percentage of tests passed
    if total_test_cases > 0:
        success_rate = (passed_test_cases / total_test_cases) * 100
        print(f"Total percentage of tests passed: {success_rate:.2f}%")
        average_difficulty = (total_difficulty / total_test_cases)
        print(f"Average difficulty score: {average_difficulty:.2f}")
    else:
        print("No test cases to run.")

