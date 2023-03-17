import nltk
nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_book_sentiment(filename):
    # Load the book text from file
    with open(filename, 'r', encoding='utf-8') as f:
        book_text = f.read()

    # Use the Vader Sentiment Analyzer to compute the sentiment score
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(book_text)

    # Print the sentiment scores
    print(f"Sentiment score of \"{filename}\":")
    print(f"Positive: {sentiment_scores['pos']:.2f}")
    print(f"Negative: {sentiment_scores['neg']:.2f}")
    print(f"Neutral: {sentiment_scores['neu']:.2f}")
    print(f"Compound: {sentiment_scores['compound']:.2f}")

# Example usage: get the sentiment score of the book "example_book.txt"
get_book_sentiment("example_book.txt")
