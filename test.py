from faq_data import FAQS

for faq in FAQS:
    print(faq["questions"][0], "->", faq["answer"])