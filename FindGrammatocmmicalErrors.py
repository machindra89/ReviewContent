import nltk
import language_tool_python

# Load the book
with open('book.txt', 'r') as f:
    book = f.read()

# Split the book into sentences
sentences = nltk.sent_tokenize(book)

# Initialize the LanguageTool client
tool = language_tool_python.LanguageTool('en-US')

# Loop over each sentence and check for grammatical errors
errors = []
for i, sentence in enumerate(sentences):
    matches = tool.check(sentence)
    if matches:
        for match in matches:
            errors.append((match.ruleId, match.msg, sentence, i+1))

# Print the errors along with their corresponding sentence and page number
for error in errors:
    print(f"Page {error[3]}: {error[2]}\nError: {error[1]} (Rule ID: {error[0]})\n")
