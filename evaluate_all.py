import os
import argparse
import csv
import importlib
from wrappers.model_wrapper import ModelWrapper, GPT2Wrapper, GPT4Wrapper  # Assuming these are the available wrappers

def load_model(model_name):
    """
    Return an instance of the appropriate ModelWrapper subclass based on the model name.
    """
    if model_name.startswith("gpt2"):
        return GPT2Wrapper(model_name)
    elif model_name.startswith("gpt4"):  # Hypothetical support for GPT-4
        return GPT4Wrapper(model_name)
    else:
        raise ValueError(f"Unsupported model: {model_name}")

def main(model_name):
    model_wrapper = load_model(model_name)
    
    results = []  # To store scores for each benchmark
    
    for benchmark in os.listdir("benchmarks"):
        print(benchmark)
        # Dynamically import the run_benchmark function from the benchmark's module
        module_name = f"benchmarks.{benchmark}.run"
        benchmark_module = importlib.import_module(module_name)
        score = benchmark_module.run_benchmark(model_wrapper)
        
        results.append((benchmark, score))
    
    # Save results to a CSV file
    with open(f"results/results_{model_name}.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Benchmark", "Score out of 100"])
        writer.writerows(results)
    
    print(f"Results saved to results_{model_name}.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluate solutions using a specified AI model.')
    parser.add_argument('model_name', type=str, help='Name of the AI model to use for generating solutions.')
    
    args = parser.parse_args()
    main(args.model_name)
