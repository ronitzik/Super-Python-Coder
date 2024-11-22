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
            temperature=0.7,  # Adjust creativity level
            max_tokens=100,  # Adjust response length
        )
        # Extract and return the assistant's reply
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {str(e)}"


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

        # Print GPT's response
        print(f"GPT: {gpt_response}")
