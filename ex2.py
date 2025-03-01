import os
import spacy
from collections import defaultdict
from gensim import corpora, models
from gensim.models import Phrases

# Load spaCy model with increased max_length limit
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

# Set the desired max_length limit
nlp.max_length = 20_000_000  # For example, set it to 20 million characters

# Define your custom stop words

custom_stop_words = {
    'time', 'eye', 'good', 'god', 'face', 'hand', 'way', 'monster', 'head', 'thing', 'voice', 'year', 'arm', 'foot', 'old', 'giant'
}

# Extend spaCy's default stop words with custom stop words
nlp.Defaults.stop_words |= custom_stop_words

# Directory containing .txt files
directory = 'output_titles/annabeth_diag'

# List to store preprocessed documents
documents = []

# Read and preprocess the text files
for filename in os.listdir(directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(directory, filename)
with open(file_path, "r", encoding="utf-8") as file:

            text = file.read()

            # Preprocess text using spaCy
            doc = nlp(text)
            # Tokenize and remove stop words
            tokens = [
    token.lemma_.lower() 
    for token in doc 
    if not token.is_stop and token.is_alpha and len(token.text) > 2 and token.pos_ in ["NOUN", "ADJ"]
]

            documents.append(tokens)

# Create dictionary and corpus for LDA model

bigram = Phrases(documents, min_count=5, threshold=10)
bigram_mod = [bigram[doc] for doc in documents]

# Update dictionary and corpus with bigrams
dictionary = corpora.Dictionary(bigram_mod)
corpus = [dictionary.doc2bow(doc) for doc in bigram_mod]

# Train LDA model
lda_model = models.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=100, alpha= 'auto', eta= 'auto', per_word_topics = True)


# Print the topics and related words
for idx, topic in lda_model.print_topics(-1):
    print(f"Topic {idx}: {topic}")

# Save the topics to a file
output_file = 'topics.txt'
with open(output_file, 'w') as f:
    for idx, topic in lda_model.print_topics(-1):
        f.write(f"Topic {idx}: {topic}\n")

print(f"Topics saved to {output_file}")

# Save the topic distribution for all documents in a single .txt file
output_file_topic_distribution = 'topic_distribution_all_docs.txt'
with open(output_file_topic_distribution, 'w') as f:
    for i, doc in enumerate(corpus):
        f.write(f"Document {i} topic distribution:\n")
        topic_distribution = lda_model.get_document_topics(doc, per_word_topics=True)
        for topic, weight in topic_distribution[0]:
            f.write(f"Topic {topic}: {weight}\n")

print(f"Topic distributions saved to {output_file_topic_distribution}")
