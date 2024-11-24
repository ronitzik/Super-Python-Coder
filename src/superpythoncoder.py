import time
import random
import openai
import os
import subprocess
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

PROGRAMS_LIST = [
    """A program as if you are given two strings str1 and str2,
prints all interleavings of the given two strings. You may assume
that all characters in both strings are different. As example:
for the Input: str1 = "AB", str2 = "CD" the Output should be:
ABCD, ACBD, ACDB, CABD, CADB, CDAB
another example: Input: str1 = "AB", str2 = "C"
Output: ABC, ACB, CAB
""",
    "A program that checks if a number is a palindrome",
    "A program that finds the kth smallest element in a given BST.",
    """A program as if You are given an array of k linked-lists lists,
each linked-list is sorted in ascending order, Merge all the linked-lists
into one sorted linked-list and return it.""",
    """A program as if you are Given a string containing just the characters
    '(' and ')',
return the length of the longest valid (well-formed) parentheses substring
.""",
]


def chat_with_gpt(conversation):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"


def run_unit_tests(file_path):
    try:
        # Run the unit tests using unittest in a subprocess
        result = subprocess.run(
            ["python", "-m", "unittest", file_path],
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            print("All unit tests passed successfully!")
            return True, None
        else:
            print("Some unit tests failed:")
            return False, result.stderr
    except Exception as e:
        print(f"Error while running unit tests: {e}")
        return False, str


def validate_code(code):
    """Validates the generated Python code for syntax correctness."""
    try:
        # Remove leading/trailing whitespace
        code = code.strip()
        # Compile the code to check for syntax errors
        compile(code, "<string>", "exec")
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"


def time_code_execution(file_path):
    try:
        start_time = time.time()
        result = subprocess.run(
            ["python", file_path],
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            execution_time = (
                time.time() - start_time
            ) * 1000  # Convert to milliseconds
            return execution_time, None
        else:
            return None, result.stderr
    except Exception as e:
        return None, str(e)


def optimize_code(prompt, original_code, unit_tests, original_time):
    conversation = [
        {
            "role": "system",
            "content": """You are a helpful assistant who optimizes
        Python code for performance.""",
        },
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": original_code},
        {
            "role": "user",
            "content": """Please optimize the above Python code for better
            performance while ensuring the provided unit tests remain valid.
            Do not modify the tests but focus on making the function
            itself faster.The response should contain only the
            optimized code.""",
        },
    ]

    gpt_response = chat_with_gpt(conversation)

    is_valid, validation_error = validate_code(gpt_response)
    if not is_valid:
        print(f"Optimized code validation failed: {validation_error}")
        return None, None, validation_error

    optimized_program_path = "./src/optimized_program.py"
    with open(optimized_program_path, "w") as f:
        f.write(gpt_response)

    optimized_time, error_message = time_code_execution(optimized_program_path)
    if error_message:
        return None, None, error_message

    if optimized_time < original_time:
        print(
            f"""Code running time optimized! It now runs in
{optimized_time:.2f} ms, """
            f"while before it was {original_time:.2f} ms."
        )
    else:
        print(
            f"""Optimization did not improve runtime.
Original: {original_time:.2f} ms,
Optimized: {optimized_time:.2f} ms."""
        )

    return gpt_response, optimized_time, None


def generate_code(prompt):
    conversation = [
        {
            "role": "system",
            "content": """You are a helpful assistant
            that generates Python programs.""",
        },
        {"role": "user", "content": prompt},
    ]
    for attempt in range(5):
        print(f"Attempt {attempt + 1} to generate code...")
        gpt_response = chat_with_gpt(conversation)

        os.makedirs("./src", exist_ok=True)
        new_program_path = os.path.abspath("./src/generated_program_byTheCoder.py")

        # Validate GPT response
        is_valid, validation_error = validate_code(gpt_response)
        if not is_valid:
            print(f"Invalid code generated: {validation_error}.")
            conversation.append(
                {
                    "role": "user",
                    "content": f"""The previous code had a syntax error:
                    {validation_error}. Please fix it and try again. Ensure
                    the response is valid Python code.""",
                }
            )
            continue

        # Write the GPT response to a file
        with open(new_program_path, "w") as f:
            f.write(gpt_response)

        # Run the unit tests
        success, error_message = run_unit_tests(new_program_path)
        if success:
            print("Code creation completed successfully!")
            original_time, error = time_code_execution(new_program_path)
            if error:
                print(f"Error measuring execution time: {error}")
                return False
            print(f"Original code execution time: {original_time:.2f} ms.")
            optimization_prompt = f"""The following Python program solves the
            task: {prompt}. Optimize it for better performance."""
            optimize_code(
                optimization_prompt, gpt_response, "unit_tests", original_time
            )
            os.startfile(new_program_path)
            return True
        else:
            print(f"Unit tests failed: {error_message}. Retrying...")
            conversation.append({"role": "assistant", "content": gpt_response})
            conversation.append(
                {
                    "role": "user",
                    "content": f"""The previous code you provided:
                    \n\n{gpt_response}\n\n
                    for this task: {prompt}, encountered issues when executed.
                    It resulted in the following error(s):
                    \n\n{error_message}\n\n
                    Please carefully review and regenerate the code.
                    Ensure that:
                    1. The function is complete, error-free,
                    and handles all possible edge cases.
                    2. The logic is correct and tested thoroughly with
                    valid unit tests.
                    3. The response only contains the corrected Python code
                    without explanations or additional text.
                    4. At least 10 unit tests are included, covering
                    edge cases, normal cases, and boundary conditions.
                    5. The function and tests are self-contained and can be
                    directly executed without further modifications.
                    Regenerate the code with these requirements strictly
                    followed. Begin the response with the function definition
                    (e.g., `def <function_name>:`).""",
                }
            )

    print("Code generation FAILED after 5 attempts.")
    return False


def main():
    print("""I’m Super Python Coder. Tell me, which program would you
like me to code for you? If you don't have an idea,just
press enter and I will choose a random program to code.
Type 'exit' to quit.""")
    while True:
        user_input = input("Your program idea: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        if not user_input.strip():
            chosen_program = random.choice(PROGRAMS_LIST)
            print(f"The chosen function is: {chosen_program}")
            user_input = chosen_program
        prompt = f"""
        please write a Python program (in plain text only, without using code
        blocks) to accomplish the following task:
        {user_input}
        Ensure the following requirements are met:
        1. The program is complete, error-free, and fully functional.
        2. Include a minimum of 10 unit tests using assertions (`assert`)
        to validate the logic of the program.
        3. The unit tests should cover:
        - Standard use cases.
        - Edge cases and boundary conditions.
        - Any special cases that could arise from the problem's constraints.
        4. Provide the Python code only, without explanations, comments,
        or examples.
        5. Begin the response with the function definition (e.g.,
        `def <function_name>:`), and ensure the function works as described.
        """
        generate_code(prompt)


if __name__ == "__main__":
    main()
