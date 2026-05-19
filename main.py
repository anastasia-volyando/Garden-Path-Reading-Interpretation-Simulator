import time
from database import create_tables, insert_sample_sentences, get_sentences, save_result
from analyzer import analyze_interpretation, calculate_score


def run_experiment():
    create_tables()
    insert_sample_sentences()

    sentences = get_sentences()

    print("Garden-Path Reading & Interpretation Simulator")
    print("----------------------------------------------")
    print("You will read sentences word by word.")
    print("Press Enter after each word.")
    print("Then write what you think the sentence means.\n")

    total_score = 0
    max_score = len(sentences) * 5

    for item in sentences:
        sentence_id = item[0]
        sentence = item[1]
        disambiguating_word = item[2]
        trap_explanation = item[3]
        correct_meaning = item[4]
        wrong_keywords = item[5]
        correct_keywords = item[6]

        words = sentence.split()
        reading_times = []

        print("\nNew sentence")
        print("------------")
        input("Press Enter to start reading...")

        for word in words:
            start_time = time.time()
            input(word + " ")
            end_time = time.time()

            reading_time = end_time - start_time
            reading_times.append((word, reading_time))

        user_answer = input("\nWhat do you think this sentence means?\n> ")

        longest_pause_word, longest_pause_time = max(reading_times, key=lambda x: x[1])

        interpretation_result = analyze_interpretation(
            user_answer,
            wrong_keywords,
            correct_keywords
        )

        score = calculate_score(
            interpretation_result,
            longest_pause_word,
            disambiguating_word
        )

        total_score += score

        save_result(
            sentence_id,
            user_answer,
            longest_pause_word,
            longest_pause_time,
            interpretation_result
        )

        print("\nAnalysis")
        print("--------")
        print(f"Sentence: {sentence}")
        print(f"Longest pause: {longest_pause_word} ({longest_pause_time:.2f} seconds)")

        if longest_pause_word.lower() == disambiguating_word.lower():
            print("Processing difficulty detected at the expected disambiguating word.")
        else:
            print(f"Expected disambiguating word: {disambiguating_word}")

        print(f"Interpretation result: {interpretation_result}")
        print(f"Score: {score}/5")
        print(f"Explanation: {trap_explanation}")
        print(f"Correct meaning: {correct_meaning}")

    print("\nExperiment complete.")
    print(f"Final score: {total_score}/{max_score}")
    print("Results saved to SQLite database: garden_path.db")


run_experiment()