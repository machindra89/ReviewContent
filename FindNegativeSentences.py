import nltk
from nltk.tokenize import sent_tokenize
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the book
with open('book.txt', 'r') as f:
    book = f.read()

# Split the book into sentences
sentences = sent_tokenize(book)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Define the negative sentiment threshold
threshold = -0.7

# Identify the negative sentences
neg_sentences = []
for i, sentence in enumerate(sentences):
    score = sia.polarity_scores(sentence)['compound']
    if score < threshold:
        neg_sentences.append((sentence, i+1))

# Print the negative sentences and their page numbers
for sentence, page in neg_sentences:
    print(f"Page {page}: {sentence}")
