import time
import json
import random

# Quiz data with multiple categories
quiz_categories = {
    "General Knowledge": [
        {
            "question": "What is the capital of France?",
            "options": ["A) London", "B) Berlin", "C) Paris", "D) Madrid"],
            "answer": "C",
            "difficulty": 1
        },
        {
            "question": "Which planet is known as the Red Planet?",
            "options": ["A) Earth", "B) Mars", "C) Jupiter", "D) Venus"],
            "answer": "B",
            "difficulty": 2
        }
    ],
    "Science": [
        {
            "question": "What is the chemical symbol for water?",
            "options": ["A) O2", "B) CO2", "C) H2O", "D) NaCl"],
            "answer": "C",
            "difficulty": 1
        },
        {
            "question": "What planet is known as the Earth's twin?",
            "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Saturn"],
            "answer": "A",
            "difficulty": 2
        }
    ],
    "History": [
        {
            "question": "Who was the first president of the United States?",
            "options": ["A) Abraham Lincoln", "B) Thomas Jefferson", "C) John Adams", "D) George Washington"],
            "answer": "D",
            "difficulty": 1
        },
        {
            "question": "In what year did World War II end?",
            "options": ["A) 1945", "B) 1939", "C) 1941", "D) 1950"],
            "answer": "A",
            "difficulty": 2
        }
    ]
}

# File paths for storing data
HIGH_SCORE_FILE = "high_score.json"
LEADERBOARD_FILE = "leaderboard.json"

# Load high score
def load_high_score():
    try:
        with open(HIGH_SCORE_FILE, "r") as file:
            return json.load(file)["high_score"]
    except FileNotFoundError:
        return 0

# Save high score
def save_high_score(score):
    with open(HIGH_SCORE_FILE, "w") as file:
        json.dump({"high_score": score}, file)

# Load leaderboard
def load_leaderboard():
    try:
        with open(LEADERBOARD_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save leaderboard
def save_leaderboard(leaderboard):
    with open(LEADERBOARD_FILE, "w") as file:
        json.dump(leaderboard, file)

# Update leaderboard with new score
def update_leaderboard(name, score):
    leaderboard = load_leaderboard()
    leaderboard.append({"name": name, "score": score})
    leaderboard = sorted(leaderboard, key=lambda x: x["score"], reverse=True)[:5]  # Top 5 scores
    save_leaderboard(leaderboard)

# Provide a hint by removing one incorrect option
def provide_hint(options, correct_answer):
    incorrect_options = [opt for opt in options if not opt.startswith(correct_answer)]
    options.remove(incorrect_options[0])
    print(f"Hint: One incorrect option has been removed.")
    for option in options:
        print(option)

# Run the quiz
def run_quiz():
    name = input("Enter your name: ")
    score = 0
    high_score = load_high_score()

    print("Choose a category: General Knowledge, Science, History")
    category = input().strip()

    if category not in quiz_categories:
        print("Invalid category. Exiting quiz.")
        return

    quiz = quiz_categories[category]
    random.shuffle(quiz)  # Shuffle questions

    time_limit = 10  # seconds

    for question in quiz:
        print("\n" + question["question"])
        for option in question["options"]:
            print(option)

        # Ask if user wants a hint
        hint = input("Do you want a hint? (yes/no): ").strip().lower()
        if hint == "yes":
            provide_hint(question["options"], question["answer"])

        start_time = time.time()
        answer = input(f"Enter your answer (A, B, C, D) within {time_limit} seconds: ").upper()
        end_time = time.time()

        if end_time - start_time > time_limit:
            print("Time's up! No points awarded.")
        elif answer == question["answer"]:
            print("Correct!")
            score += question["difficulty"]
        else:
            print(f"Wrong! The correct answer is {question['answer']}.")

    print(f"\nYour final score is {score}/{len(quiz)}.")

    if score > high_score:
        print(f"New high score! Your score: {score}")
        save_high_score(score)
    else:
        print(f"The high score is still {high_score}.")

    update_leaderboard(name, score)

    print("\nTop 5 Leaderboard:")
    leaderboard = load_leaderboard()
    for idx, entry in enumerate(leaderboard):
        print(f"{idx + 1}. {entry['name']} - {entry['score']}")

if __name__ == "__main__":
    run_quiz()
