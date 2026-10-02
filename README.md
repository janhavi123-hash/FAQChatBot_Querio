# Querio — FAQ Chatbot

An AI-powered FAQ chatbot built for a fictional online store, "Querio Store." Users can ask questions in natural language and get matched to the most relevant answer — even if their phrasing doesn't exactly match the stored FAQ.

🔗 **Live Demo:** [https://janhavi123-hash-faqchatbot-querio-app-juu8nc.streamlit.app/]

## Demo Video
📹 [Watch the demo video](https://drive.google.com/file/d/1gSJ2JoPFt_f72budWOcWBJdYuMc6dic2/view?usp=drivesdk)

## Features
- Natural language question matching using AI sentence embeddings (not just exact keyword matching)
- Chat interface with a WhatsApp-style bubble UI
- Sidebar with browsable FAQ topics
- Emoji-based feedback on each answer (😃 / 😐 / 😞)
- Ability to add new FAQs directly through the UI, saved persistently

## Tech Stack
- Python
- Streamlit (web interface)
- sentence-transformers (semantic sentence embeddings — `all-MiniLM-L6-v2`)
- scikit-learn (cosine similarity)

## How It Works
1. Every stored FAQ has several example phrasings of the same question.
2. Each phrasing is converted into a vector using a pretrained sentence-embedding model, which captures the *meaning* of the sentence rather than just its exact words.
3. When a user asks something, their question is converted the same way, and compared against all stored FAQ vectors using cosine similarity.
4. The closest match above a confidence threshold is returned as the answer; below that, the bot gives a fallback response.

## Known Limitations
- Since it's matching against a fixed set of stored answers, it can only answer what it has been taught — it can't generate brand-new answers.
- Very short or grammatically broken questions (e.g. missing verbs) are sometimes matched less accurately than clearly-worded ones, since the AI model relies partly on sentence structure.
- The first run downloads a ~90MB pretrained model, so initial startup is slower than subsequent runs.
