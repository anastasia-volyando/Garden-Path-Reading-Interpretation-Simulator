def analyze_interpretation(user_answer, wrong_keywords, correct_keywords):
    answer = user_answer.lower()

    wrong_list = wrong_keywords.lower().split(",")
    correct_list = correct_keywords.lower().split(",")

    wrong_matches = 0
    correct_matches = 0

    for keyword in wrong_list:
        keyword = keyword.strip()
        if keyword and keyword in answer:
            wrong_matches += 1

    for keyword in correct_list:
        keyword = keyword.strip()
        if keyword and keyword in answer:
            correct_matches += 1

    if correct_matches > wrong_matches:
        return "Correct or mostly correct interpretation"
    elif wrong_matches > correct_matches:
        return "Possible garden-path trap detected"
    else:
        return "Unclear interpretation"


def calculate_score(interpretation_result, longest_pause_word, disambiguating_word):
    score = 0

    if interpretation_result == "Correct or mostly correct interpretation":
        score += 3
    elif interpretation_result == "Unclear interpretation":
        score += 1

    if longest_pause_word.lower() == disambiguating_word.lower():
        score += 2

    return score