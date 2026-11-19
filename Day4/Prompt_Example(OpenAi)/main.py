import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")


def ask_openai(prompt, system_message=None):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OPENAI_API_KEY in your environment or .env file.")

    messages = []
    if system_message:
        messages.append({"role": "system", "content": system_message})
    messages.append({"role": "user", "content": prompt})

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0,
        max_completion_tokens=2000,
    )
    return response.choices[0].message.content


def zero_shot():
    print("\n--- ZERO-SHOT PROMPTING ---")
    prompt = """
    Classify the sentiment of the following customer review as Positive,
    Neutral, or Negative. Output only the category name.

    Review: "The delivery arrived ahead of schedule, but the setup manual was confusing."
    Sentiment:
    """
    print("\nAI Response:\n")
    print(ask_openai(prompt))


def few_shot():
    print("\n--- FEW-SHOT PROMPTING ---")
    prompt = """
    Classify employee performance based on the following examples.

    Example 1:
    Rating: 9
    Output: Excellent

    Example 2:
    Rating: 7
    Output: Good

    Example 3:
    Rating: 4
    Output: Average

    Now classify:
    Rating: 10
    Return only the classification.
    """
    print("\nAI Response:\n")
    print(ask_openai(prompt))


def chain_of_thought():
    print("\n--- CHAIN-OF-THOUGHT PROMPTING ---")
    prompt = """
    An employee has the following salary:
    Basic Salary = 40000
    HRA = 20% of Basic Salary
    Bonus = 10% of Basic Salary

    Calculate the total salary. Provide a concise step-by-step calculation
    and final answer.
    """
    print("\nAI Response:\n")
    print(ask_openai(prompt))


def role_based():
    print("\n--- ROLE-BASED PROMPTING ---")
    system_message = """
    You are a Senior Python Developer with 10 years of experience.
    You write clean, reusable and well-commented Python code.
    Explain concepts in simple language.
    """
    prompt = """
    Create a Python program using Pandas.

    Requirements:
    1. Read employee.xlsx.
    2. Display employee records.
    3. Calculate average salary.
    4. Display employees earning above 50000.
    5. Handle file-not-found exceptions.

    Provide complete code with comments.
    """
    print("\nAI Response:\n")
    print(ask_openai(prompt, system_message))


def self_consistency():
    print("\n--- SELF-CONSISTENCY PROMPTING ---")
    prompt = """
    Calculate 15% of 80000. Solve this problem independently.
    Show the calculation and final answer.
    Return the final answer in this format:
    FINAL ANSWER: <number>
    """
    answers = []
    for attempt in range(3):
        print(f"\nAttempt {attempt + 1}:")
        result = ask_openai(prompt)
        print(result)
        answers.append(result)

    comparison_prompt = f"""
    Compare these three independently generated solutions.

    Solution 1: {answers[0]}
    Solution 2: {answers[1]}
    Solution 3: {answers[2]}

    Identify the correct numerical answer. Recalculate independently to verify it.
    Explain whether the answers agree.
    """
    print("\n--- CONSISTENCY VALIDATION ---")
    print(ask_openai(comparison_prompt))


def main():
    while True:
        print("\n================================")
        print(" OPENAI PROMPT ENGINEERING LAB")
        print("================================")
        print("1. Zero-Shot Prompting")
        print("2. Few-Shot Prompting")
        print("3. Chain-of-Thought Prompting")
        print("4. Role-Based Prompting")
        print("5. Self-Consistency Prompting")
        print("6. Exit")

        choice = input("\nEnter your choice: ")
        try:
            if choice == "1":
                zero_shot()
            elif choice == "2":
                few_shot()
            elif choice == "3":
                chain_of_thought()
            elif choice == "4":
                role_based()
            elif choice == "5":
                self_consistency()
            elif choice == "6":
                print("Thank you for using OpenAI!")
                break
            else:
                print("Invalid choice. Try again.")
        except Exception as error:
            print("\nError occurred:", error)


if __name__ == "__main__":
    main()