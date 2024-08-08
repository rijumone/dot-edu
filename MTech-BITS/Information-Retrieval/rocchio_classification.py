import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Example training documents
positive_docs = [
    "I love this product",
    "This is an amazing experience",
    "I had a fantastic time"
]

negative_docs = [
    "I hate this product",
    "This was a terrible experience",
    "I had an awful time"
]

# Combine all documents for TF-IDF vectorization
all_docs = positive_docs + negative_docs

# Vectorize the documents using TF-IDF
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(all_docs).toarray()
# import pdb;pdb.set_trace()

# Get the feature names (terms)
terms = vectorizer.get_feature_names_out()

# Create a heatmap
plt.figure(figsize=(10, 6))
sns.heatmap(tfidf_matrix, annot=True, fmt=".2f", cmap="YlGnBu",
            xticklabels=terms, yticklabels=[f'Doc{i+1}' for i in range(len(all_docs))])
plt.title('TF-IDF Heatmap')
plt.xlabel('Terms')
plt.ylabel('Documents')
plt.show()

# Split the TF-IDF matrix into positive and negative class matrices
positive_matrix = tfidf_matrix[:len(positive_docs)]
negative_matrix = tfidf_matrix[len(positive_docs):]

# Calculate the centroids for each class
positive_centroid = np.mean(positive_matrix, axis=0)
negative_centroid = np.mean(negative_matrix, axis=0)

# New document to classify
new_doc = ["I had a terrible experience with this product"]

# Vectorize the new document using the same vectorizer
new_doc_tfidf = vectorizer.transform(new_doc).toarray()

# Calculate cosine similarity between the new document and both centroids
similarity_to_positive = cosine_similarity(
    new_doc_tfidf, positive_centroid.reshape(1, -1))
similarity_to_negative = cosine_similarity(
    new_doc_tfidf, negative_centroid.reshape(1, -1))

# Print the classification result
if similarity_to_positive > similarity_to_negative:
    print("The document is classified as: Positive")
else:
    print("The document is classified as: Negative")
