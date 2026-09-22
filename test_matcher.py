from matcher import FAQMatcher
from faq_data import FAQS

matcher = FAQMatcher(FAQS)

test_questions = [
    "can u accept cod",
    "i get my order at america",
    "u receive the orders from america or other international country",
    "how i get to know that my order get processed",
    "What's the weather today?",  # unrelated, should return no match
]

for question in test_questions:
    match, score = matcher.get_best_match(question)
    print(f"\nUser asked: {question}")
    if match:
        print(f"Matched FAQ: {match['questions'][0]} (score: {score:.2f})")
        print(f"Answer: {match['answer']}")
    else:
        print(f"No good match found (best score: {score:.2f})")