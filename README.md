# AI Benchmarking Framework

This framework evaluates various generative AI models, referred to as "coding solution generators," across multiple coding benchmarks, referred to as "measures of coding". The purpose is to assess the capability of these models in generating coding solutions.

## Table of Contents
- [Getting Started](#getting-started)
- [Adding New Benchmarks](#adding-new-benchmarks)
- [Adding New Models](#adding-new-models)
- [Benchmark Assumptions](#benchmark-assumptions)
- [Results Format](#results-format)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

1. Clone the repository:

`git clone <repository_url>`

2. Navigate to the repository root and install the required packages:

`cd ai_benchmark_framework`
`pip install -r requirements.txt`

3. Run the evaluation script for a particular model:

`python evaluate_all.py <model_name>`

This will evaluate the model across all benchmarks and save the results in a CSV file in the `results` folder.

## Adding New Benchmarks

To add a new measure of coding:

1. Create a new directory under the `benchmarks/` directory. This will be the name of your benchmark.

2. Inside your benchmark directory, create an `__init__.py` file (it can be empty). This is required to treat the directory as a Python package.

3. Create a `run.py` file. Implement the `run_benchmark(model_wrapper)` method inside this file. This method should:
- Use the `model_wrapper.generate_solution(test_case)` to get solutions for test cases.
- Evaluate these solutions.
- Return a score out of 100.

4. If your benchmark has specific dependencies, add a `requirements.txt` file in the benchmark directory. Users can install these dependencies before running the benchmark.

## Adding New Models

To add a new coding solution generator:

1. Create a subclass of `ModelWrapper` in the `wrappers/model_wrapper.py` file. This subclass should:
- Implement the `load_model` method to initialize the model and any associated tools (e.g., tokenizers).
- Implement the `generate_solution(test_case)` method to produce solutions for given test cases.

2. In the `load_model` function of `evaluate_all.py`, add a condition to return an instance of your new wrapper subclass based on a specific `model_name`.

3. If your model has specific dependencies, update the main `requirements.txt` file or provide instructions for users to install these dependencies.

## Benchmark Assumptions

Each benchmark, or measure of coding, should adhere to the following assumptions:

1. **Directory Structure**: Each benchmark must have its own directory under the `benchmarks/` directory.

2. **`run.py` File**: Each benchmark directory must contain a `run.py` file with a `run_benchmark(model_wrapper)` method. This method is the entry point for the benchmark.

3. **Score**: The `run_benchmark(model_wrapper)` method should return a score out of 100 based on the model's performance on that benchmark.

4. **Dependencies**: If the benchmark has specific Python library dependencies, they should be listed in a `requirements.txt` file within the benchmark's directory.

## Results Format

After running the evaluation script, the results are saved in a CSV file within the `results` folder. The filename follows the format `results_MODELNAME.csv`, where `MODELNAME` is the name of the AI model used.

The CSV file has two columns:
1. `Benchmark`: The name of the benchmark.
2. `Score out of 100`: The score achieved by the model on that benchmark.

## Contributing

Contributions to enhance this framework are welcome. Whether it's adding new benchmarks, improving existing ones, adding new models, or improving the documentation, your efforts are appreciated. Please ensure that any added benchmarks or models adhere to the guidelines mentioned above.
