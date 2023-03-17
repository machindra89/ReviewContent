!pip install -U sentence-transformers

from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd
import nltk
nltk.download('punkt')

from nltk.tokenize import sent_tokenize

def find_duplicate_sentences(filename, threshold=0.7):
    # Load the book text from file
    with open(filename, 'r', encoding='utf-8') as f:
        book_text = f.read()

    # Tokenize the book into sentences
    sentences = sent_tokenize(book_text)

    # Load a pre-trained sentence embedding model
    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # Generate sentence embeddings
    embeddings = model.encode(sentences)

    # Compute pairwise cosine similarity between embeddings
    similarity_matrix = np.inner(embeddings, embeddings)

    # Find duplicate sentences based on their semantic similarity
    duplicate_pairs = []
    for i in range(len(sentences)):
        for j in range(i+1, len(sentences)):
            if similarity_matrix[i,j] > threshold:
                duplicate_pairs.append((i,j))

    # Output the duplicate sentences and their page numbers
    if duplicate_pairs:
        pages = [i+1 for i in range(len(sentences))]
        df = pd.DataFrame({'Page': pages, 'Sentence': sentences})
        for pair in duplicate_pairs:
            print(f"\"{df.iloc[pair[0]]['Sentence']}\" (Page {df.iloc[pair[0]]['Page']}) is similar to \"{df.iloc[pair[1]]['Sentence']}\" (Page {df.iloc[pair[1]]['Page']})")
    else:
        print("No duplicate sentences found")

# Example usage: find duplicate sentences in the book "example_book.txt"
find_duplicate_sentences("example_book.txt", threshold=0.7)
