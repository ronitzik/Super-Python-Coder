# superpythoncoder.py file

import time
import random
import openai
import os
import subprocess
from dotenv import load_dotenv
from colorama import Fore, init
from tqdm import tqdm

init(autoreset=True)  # Initialize colorama for auto-resetting colors

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
    """A program as if you are Given a string containing just the characters '(' and ')',
return the length of the longest valid (well-formed) parentheses substring.""",
]


def chat_with_gpt(conversation):
    """Sends a conversation to the OpenAI API and returns the assistant's response."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=conversation,
            seed=42,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error: {str(e)}"


def run_unit_tests(file_path):
    """Runs unit tests using Python's unittest module for a given file."""
    try:
        with tqdm(total=100) as progress:
            for i in range(10):
                time.sleep(0.1)  # Simulating progress
                progress.update(10)
        result = subprocess.run(
            ["python", "-m", "unittest", file_path],
            text=True,
            capture_output=True,
        )
        if result.returncode == 0:
            print(Fore.GREEN + "All unit tests passed successfully!")
            return True, None
        else:
            print(Fore.RED + "Some unit tests failed:")
            return False, result.stderr
    except Exception as e:
        print(Fore.RED + f"Error while running unit tests: {e}")
        return False, str


def validate_code(code):
    """Validates the generated Python code for syntax correctness."""
    try:
        code = code.strip()
        compile(code, "<string>", "exec")
        return True, None
    except SyntaxError as e:
        return False, f"SyntaxError: {e}"


def check_lint(file_path):
    """Runs pylint on the file and checks for warnings/errors."""
    print(Fore.YELLOW + "Checking for lint issues using pylint...")
    try:
        result = subprocess.run(
            ["pylint", file_path],
            text=True,
            capture_output=True,
        )
        lint_output = result.stdout + result.stderr
        lint_score_line = next(
            (
                line
                for line in lint_output.splitlines()
                if "Your code has been rated at" in line
            ),
            None,
        )
        if lint_score_line:
            lint_score = float(lint_score_line.split("/")[0].split()[-1])
            print(Fore.CYAN + f"Lint score: {lint_score}/10.00")
            if lint_score == 10.0:
                print(Fore.GREEN + "Amazing. No lint errors/warnings.")
                return True, None
        print(Fore.RED + "Lint issues found:")
        print(Fore.LIGHTRED_EX + lint_output)
        return False, lint_output
    except Exception as e:
        print(Fore.RED + f"Error while checking lint: {e}")
        return False, str(e)


def fix_lint_issues(prompt, code, lint_errors):
    """Uses the OpenAI API to fix lint issues in the given Python code."""
    conversation = [
        {
            "role": "system",
            "content": "You are a helpful assistant who fixes Python code lint issues.",
        },
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code},
        {
            "role": "user",
            "content": f"""
The above code has the following lint errors/warnings:
{lint_errors}
Fix the code while preserving functionality, ensuring it meets the following:
Pylint score: 10/10.
Adherence to PEP8:
Indentation.
Max line length: 100 characters.
Consistent naming.
Include a module docstring summarizing the script.
Remove unused imports/variables.
Add concise docstrings for functions.
Remove redundancy.
File ends with a newline and no trailing blank lines.
Return only the corrected Python code as plain text.
""",
        },
    ]

    return chat_with_gpt(conversation)


def process_lint(file_path, prompt, code, max_attempts=3):
    """Attempts to fix lint issues in the given code up to the specified number of attempts."""
    for attempt in range(max_attempts):
        print(Fore.YELLOW + f"Attempt {attempt + 1} to fix lint issues...")
        lint_success, lint_errors = check_lint(file_path)
        if lint_success:
            print(Fore.GREEN + "Lint issues resolved successfully!")
            return True

        fixed_code = fix_lint_issues(prompt, code, lint_errors)
        is_valid, validation_error = validate_code(fixed_code)
        if not is_valid:
            print(Fore.RED + f"Fixed code failed validation: {validation_error}")
            continue

        with open(file_path, "w") as f:
            f.write(fixed_code)
        code = fixed_code

    print(Fore.RED + "Maximum attempts reached. Lint issues remain.")
    return False


def time_code_execution(file_path):
    """Measures the execution time of the code in the given file."""
    try:
        with tqdm(total=100) as progress:
            for i in range(10):
                time.sleep(0.1)
                progress.update(10)
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
            print(
                Fore.GREEN + f"Code executed successfully in {execution_time:.2f} ms."
            )
            return execution_time, None
        else:
            print(Fore.RED + "Code execution failed.")
            return None, result.stderr
    except Exception as e:
        return None, str(e)


def optimize_code(prompt, original_code, original_time):
    """Uses the OpenAI API to optimize the given Python code for better performance."""
    print(Fore.YELLOW + "Optimizing code for better performance...")
    conversation = [
        {
            "role": "system",
            "content": """You are a helpful assistant who optimizes Python code for performance.""",
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
        print(Fore.RED + f"Optimized code validation failed: {validation_error}")
        return None, None, validation_error

    optimized_program_path = "./src/generated_program_bythecoder.py"
    with open(optimized_program_path, "w") as f:
        f.write(gpt_response)

    optimized_time, error_message = time_code_execution(optimized_program_path)
    if error_message:
        return None, None, error_message

    if optimized_time < original_time:
        print(
            Fore.GREEN + f"""Code running time optimized! It now runs in
{optimized_time:.2f} ms, """
            f"while before it was {original_time:.2f} ms."
        )
    else:
        print(
            Fore.RED
            + f"""Optimization did not improve runtime.
Original: {original_time:.2f} ms,
Optimized: {optimized_time:.2f} ms."""
        )

    return gpt_response, optimized_time, None


def generate_code(prompt):
    """Generates Python code based on the provided prompt using the OpenAI API."""
    conversation = [
        {
            "role": "system",
            "content": """You are a helpful assistant that generates Python programs.""",
        },
        {"role": "user", "content": prompt},
    ]
    
    game_opened = False # Flag to ensure the game is opened only once
     
    for attempt in range(5):
        print(Fore.YELLOW + f"Attempt {attempt + 1} to generate code...")
        gpt_response = chat_with_gpt(conversation)

        os.makedirs("./src", exist_ok=True)
        new_program_path = os.path.abspath("./src/generated_program_bythecoder.py")

        # Validate GPT response
        is_valid, validation_error = validate_code(gpt_response)
        if not is_valid:
            print(Fore.RED + f"Invalid code generated: {validation_error}.")
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
            print(Fore.GREEN + "Code creation completed successfully!")
            lint_prompt = f"The following Python program solves the task: {prompt}."
            if process_lint(new_program_path, lint_prompt, gpt_response):
                print(Fore.GREEN + "Amazing. No lint errors/warnings.")

            # Time the code execution
            original_time, error = time_code_execution(new_program_path)
            if error:
                print(Fore.RED + f"Error measuring execution time: {error}")
                return False

            # Optimize the generated code
            optimization_prompt = f"""The following Python program solves the
            task: {prompt}. Optimize it for better performance."""
            optimized_code, optimized_time, optimization_error = optimize_code(
                optimization_prompt, gpt_response, original_time
            )

            # Save the optimized code only if it was faster
            if optimized_code and optimized_time and optimized_time < original_time:
                with open(new_program_path, "w") as f:
                    f.write(optimized_code)
                    print(Fore.GREEN + f"Optimized code saved at {new_program_path}")
                if not game_opened:
                    print(Fore.YELLOW + "Running the optimized program locally...")
                    os.startfile(new_program_path)
                    game_opened = True
            elif optimization_error:
                print(Fore.RED + f"Optimization failed: {optimization_error}")
            else:
                print(Fore.YELLOW + "Optimization did not improve execution time.")
                if not game_opened:
                    print(Fore.YELLOW + "Running the original program locally...")
                    os.startfile(new_program_path)
                    game_opened = True

            return True
        else:
            print(f"Unit tests failed: {error_message}.")
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
Review and regenerate the code, ensuring:
The function is complete, error-free, and handles all edge cases.
Logic is correct, tested with 10+ unit tests covering:
Edge cases
Boundary conditions
Response includes only the Python code as a plain text.
The function and tests are self-contained and executable without modification.
Begin with def <function_name>:""",
                }
            )
    print("Code generation FAILED after 5 attempts.")
    return False


def main():
    """Main function that provides an interface to choose a coding task and generate a solution."""
    print(
        Fore.CYAN
        + """I’m Super Python Coder. Tell me, which program would you
like me to code for you? If you don't have an idea,just
press enter and I will choose a random program to code.
Type 'exit' to quit."""
    )
    while True:
        user_input = input(Fore.LIGHTYELLOW_EX + "program idea: ")
        if user_input.lower() == "exit":
            print(Fore.CYAN + "Goodbye!")
            break
        if not user_input.strip():
            chosen_program = random.choice(PROGRAMS_LIST)
            print(Fore.LIGHTBLUE_EX + f"The chosen function is: {chosen_program}")
            user_input = chosen_program
        prompt = f"""
        please write a Python program (in plain text only, without using code
        blocks) to accomplish the following task:
        {user_input}
Ensure the program meets the following:
Complete, error-free, fully functional.
10+ unit tests with assert to validate logic, covering:
Unique input/output for each test.
Standard, edge, boundary, and special cases.
Provide only Python code without explanations or comments.
Begin with def <function_name>:
        """
        generate_code(prompt)


if __name__ == "__main__":
    main()
