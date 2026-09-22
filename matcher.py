import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from faq_data import FAQS


class FAQMatcher:
    def __init__(self, faqs):
        self.faqs = faqs

        self.all_questions = []
        self.question_to_faq_index = []

        for faq_index, faq in enumerate(faqs):
            for question_variation in faq["questions"]:
                self.all_questions.append(question_variation)
                self.question_to_faq_index.append(faq_index)

        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.faq_vectors = self.model.encode(self.all_questions)

    def get_best_match(self, user_question, threshold=0.35):
        user_vector = self.model.encode([user_question])
        similarities = cosine_similarity(user_vector, self.faq_vectors)[0]

        best_index = similarities.argmax()
        best_score = similarities[best_index]

        if best_score < threshold:
            return None, best_score

        matched_faq_index = self.question_to_faq_index[best_index]
        return self.faqs[matched_faq_index], best_score

    def add_faq(self, faq):
        """Adds one new FAQ (with its question variations) without
        reloading the whole model — just encodes and appends the new ones."""
        faq_index = len(self.faqs)
        self.faqs.append(faq)

        new_vectors = self.model.encode(faq["questions"])
        for question_variation in faq["questions"]:
            self.all_questions.append(question_variation)
            self.question_to_faq_index.append(faq_index)

        self.faq_vectors = np.vstack([self.faq_vectors, new_vectors])