"""Simple command-line chatbot using the OpenAI API.

Setup:
    pip install openai
    export OPENAI_API_KEY="your-key-here"   # Windows: set OPENAI_API_KEY=your-key-here
    python chatbot.py

Commands while chatting:
    /reset  - clear the conversation memory
    /quit   - exit
"""

import os
import sys

from openai import OpenAI

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # change to any chat model you have access to
SYSTEM_PROMPT = "You are a helpful, friendly assistant. Keep answers clear and concise."


def main():
    if not os.getenv("OPENAI_API_KEY"):
        sys.exit("Please set the OPENAI_API_KEY environment variable first.")

    client = OpenAI()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print(f"Chatbot ready (model: {MODEL}). Type /reset to clear memory, /quit to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input == "/quit":
            print("Goodbye!")
            break
        if user_input == "/reset":
            messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            print("Memory cleared.\n")
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            print("Bot: ", end="", flush=True)
            stream = client.chat.completions.create(
                model=MODEL, messages=messages, stream=True
            )
            reply = ""
            for chunk in stream:
                delta = chunk.choices[0].delta.content or ""
                reply += delta
                print(delta, end="", flush=True)
            print("\n")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"\n[Error] {e}\n")
            messages.pop()  # drop the failed user message


if __name__ == "__main__":
    main()
