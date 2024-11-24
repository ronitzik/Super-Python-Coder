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
for the Input: str1 = "AB", str2 = "CD"
the Output should be:
ABCD
ACBD
ACDB
CABD
CADB
CDAB
another example: Input: str1 = "AB", str2 = "C"
Output:
ABC
ACB
CAB """,
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
            temperature=0.7,
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
            os.startfile(new_program_path)
            return True
        else:
            print(f"Unit tests failed: {error_message}. Retrying...")
            conversation.append({"role": "assistant", "content": gpt_response})
            conversation.append(
                {
                    "role": "user",
                    "content": f"""I tried to run the code:
                    \n\n{gpt_response}\n\n
                    for this task: {prompt}, but got this error:
                    \n\n{error_message}.
                    Please fix the code and respond with the corrected
                    version in plain text.
                    Ensure there are at least 10 unit tests
                    covering edge cases.""",
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
        prompt = f"""Please write a Python (in plain text all the time and not
                    with code block) program for the following task:
                {user_input} Also include running unit tests with
                    asserts that check the logic of the program.
                        Make sure to also check interesting edge
                            cases. There should be at least
                            10 different unit tests. Show only the code
                            without explanations and examples.
                            start with: def (the name of
                            the chosen program).
                """
        generate_code(prompt)


if __name__ == "__main__":
    main()
