import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_with_gpt(messages):
    """
    Function to interact with ChatGPT via OpenAI API.

    Args:
        messages (list): A list of dictionaries
        representing the conversation history. Each dictionary should have
        'role' and 'content' keys.

    Returns:
        str: The response from ChatGPT.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=100,
        )
        # Extract and return the assistant's reply
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {str(e)}"


def sanitize_code(code):
    """
    Cleans the code response to remove invalid headers, footers, or extra text.
    Args:
        code (str): The raw response from the API.
    Returns:
        str: Sanitized Python code ready to run.
    """
    lines = code.splitlines()
    sanitized_lines = []

    for line in lines:
        # Ignore any lines starting with "```" or "python"
        if line.strip().startswith("```") or line.strip().startswith("python"):
            continue
        sanitized_lines.append(line)

    # Return the cleaned code
    return "\n".join(sanitized_lines).strip()


if __name__ == "__main__":
    print("Welcome to the GPT Chat App! Type 'exit' to end the conversation.")

    # Initialize conversation history
    conversation = [{"role": "system", "content": "Helpful assistant."}]

    while True:
        # Get user input
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add user message to conversation
        conversation.append({"role": "user", "content": user_input})

        # Get GPT's response
        gpt_response = chat_with_gpt(conversation)

        # Add GPT's response to conversation
        conversation.append({"role": "assistant", "content": gpt_response})

        # Sanitize the code and write it to a file
        sanitized_code = sanitize_code(gpt_response)
        try:
            with open("generatedcode.py", "w") as file:
                file.write(sanitized_code)

            print("\nGenerated code has been saved to 'generatedcode.py'.")
        except Exception as e:
            print(f"Error while running the generated code: {e}")
