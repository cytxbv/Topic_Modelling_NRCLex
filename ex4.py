import os
import spacy
from collections import defaultdict
from gensim import corpora, models
from gensim.models import CoherenceModel
from multiprocessing import freeze_support

def main():
    # Load spaCy model with increased max_length limit
    nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

    # Set the desired max_length limit
    nlp.max_length = 20_000_000  # For example, set it to 20 million characters

    # Define your custom stop words
    custom_stop_words = {'page', 'column', 'advertisements', 'advertisement', 'masthead', 'untitled', 'page', 'column', 'miscellaneous', 'news', 'new'}

    # Extend spaCy's default stop words with custom stop words
    nlp.Defaults.stop_words |= custom_stop_words

    # Directory containing .txt files
    directory = 'output_titles/'

    # List to store preprocessed documents
    documents = []

    # Read and preprocess the text files
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                text = file.read()
                # Preprocess text using spaCy
                doc = nlp(text)
                # Tokenize and remove stop words
                tokens = [token.lemma_.lower() for token in doc if not token.is_stop and token.is_alpha]
                documents.append(tokens)

    # Create dictionary and corpus for LDA model
    dictionary = corpora.Dictionary(documents)
    corpus = [dictionary.doc2bow(doc) for doc in documents]

    # Define range of number of topics to explore
    min_topics = 2
    max_topics = 10
    step_size = 1
    topics_range = range(min_topics, max_topics, step_size)

    # Store coherence scores
    coherence_scores = []

    # Iterate over different number of topics
    for num_topics in topics_range:
        # Train LDA model
        lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=15)

        # Compute coherence score
        coherence_model_lda = CoherenceModel(model=lda_model, texts=documents, dictionary=dictionary, coherence='c_v')
        coherence_score = coherence_model_lda.get_coherence()
        coherence_scores.append((num_topics, coherence_score))

    # Select the model with the highest coherence score
    best_num_topics, best_coherence_score = max(coherence_scores, key=lambda x: x[1])
    print(f"Best number of topics: {best_num_topics}, Coherence Score: {best_coherence_score}")

    # Train LDA model with the best number of topics
    lda_model = models.LdaModel(corpus, num_topics=best_num_topics, id2word=dictionary, passes=15)

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

if __name__ == '__main__':
    freeze_support()
    main()
