from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM

import time

def generate_solution(prompt, model_checkpoint):
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForCausalLM.from_pretrained(model_checkpoint)

    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=150, top_k=50)

    return tokenizer.decode(outputs[0], skip_special_tokens=True).strip()


def post_process_generated_code(code):
    # Split the code into lines and remove duplicates
    lines = code.split('\n')
    seen = set()
    unique_lines = [line for line in lines if not (line in seen or seen.add(line))]

    # Trim the code to a maximum number of lines
    max_lines = 10
    processed_code = '\n'.join(unique_lines[:max_lines])

    return processed_code.strip()

def evaluate_solution(self, generated_code, test_cases):
        # Evaluate the solutions based on correctness, efficiency, and best practices
        correctness = evaluate_correctness(generated_code, test_cases)
        efficiency = evaluate_efficiency(generated_code)
        best_practices = evaluate_best_practices(generated_code)

        return {
            'correctness': correctness,
            'efficiency': efficiency,
            'best_practices': best_practices
        }
def evaluate_correctness(generated_code, test_cases):
    # This is a safer way to execute code using the 'exec' function.
    # In production, consider using a restricted execution environment.
    if test_cases is None:
        # Handle the case where test_cases is None
        return False

    for test_case in test_cases:
        try:
            input_data = test_case.get('input')
            expected_output = test_case.get('expected_output')

            if input_data is None or expected_output is None:
                # Handle the case where input_data or expected_output is missing
                return False

            # Use 'exec' instead of 'eval'
            namespace = {'input_data': input_data}
            exec(generated_code, namespace)
            output = namespace.get('output')

            if output != expected_output:
                return False
        except Exception as e:
            return False
    return True

def evaluate_efficiency(generated_code):
    start_time = time.time()
    try:
        # Execute the code using 'exec'
        namespace = {}
        exec(generated_code, namespace)
    except Exception as e:
        return False
    finally:
        # Calculate the time taken
        end_time = time.time()
        execution_time = end_time - start_time

    # Define a threshold value (adjust as needed)
    some_threshold = 0.5

    # Compare execution_time with a benchmark
    # Return True if it's within acceptable limits
    return execution_time < some_threshold

def evaluate_best_practices(generated_code):
    # In reality, use tools like Pylint or Flake8
    # Here we just check for some basic Python best practices

    if "import os" in generated_code and "os.system" in generated_code:
        # Check for potentially dangerous operations
        return False

    # Define a length threshold value (adjust as needed)
    some_length_threshold = 1000

    if len(generated_code) > some_length_threshold:
        # Check for overly long solutions
        return False

    # Add more checks as needed
    return True
