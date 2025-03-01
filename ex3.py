import matplotlib.pyplot as plt
import numpy as np

# Load the topic distribution from the file
topic_distribution_file = 'topic_distribution_all_docs.txt'
topic_distribution_data = []

# Read and parse the topic distribution data from the file
with open(topic_distribution_file, 'r') as f:
    lines = f.readlines()
    current_doc_topic_dist = {}  # Initialize topic distribution for the current document
    for line in lines:
        if line.startswith('Document'):
            # Store the previous document's topic distribution and initialize for the next document
            if current_doc_topic_dist:
                topic_distribution_data.append(current_doc_topic_dist)
                current_doc_topic_dist = {}
        elif line.strip():
            # Parse topic distribution line
            topic, weight = line.strip().split(': ')
            current_doc_topic_dist[int(topic.split()[1])] = float(weight)
    # Store the topic distribution of the last document
    if current_doc_topic_dist:
        topic_distribution_data.append(current_doc_topic_dist)

# Determine the maximum number of topics across all documents
max_topics = max(max(topic_dist.keys()) for topic_dist in topic_distribution_data) + 1

# Create a numpy array to store topic distribution data
topic_distributions = np.zeros((len(topic_distribution_data), max_topics))

# Populate the numpy array with topic distribution data
for i, topic_dist in enumerate(topic_distribution_data):
    for topic, weight in topic_dist.items():
        topic_distributions[i, topic] = weight

# Plot the stacked bar chart
fig, ax = plt.subplots()
ind = np.arange(len(topic_distribution_data))

bottom = np.zeros(len(topic_distribution_data))
for i in range(max_topics):
    ax.bar(ind, topic_distributions[:, i], bottom=bottom, label=f"Topic {i}")
    bottom += topic_distributions[:, i]

ax.set_xlabel('Documents')
ax.set_ylabel('Topic Proportion')
ax.set_title('Topic Distribution of Documents')
ax.legend()
plt.show()


