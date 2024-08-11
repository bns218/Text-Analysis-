import pandas as pd
import requests
from bs4 import BeautifulSoup
import nltk
import os
import re


# Ensure the necessary NLTK resources are downloaded
nltk.download('punkt')


# Load the input Excel file
input_df = pd.read_csv('Input.csv')


# Define paths to StopWords and MasterDictionary directories
stopwords_dir = 'StopWords'
positive_words_file = os.path.join('MasterDictionary', 'positive-words.txt')
negative_words_file = os.path.join('MasterDictionary', 'negative-words.txt')


# Function to load stopwords
def load_stopwords(stopwords_dir):
    stopwords = set()
    for file_name in os.listdir(stopwords_dir):
        file_path = os.path.join(stopwords_dir, file_name)
        with open(file_path, 'r') as file:
            stopwords.update([line.strip().lower() for line in file])
    return stopwords


# Function to load positive and negative words
def load_wordlist(file_path):
    with open(file_path, 'r') as file:
        words = set([line.strip().lower() for line in file])
    return words


# Load stopwords
stopwords = load_stopwords(stopwords_dir)


# Load positive and negative words
positive_words = load_wordlist(positive_words_file)
negative_words = load_wordlist(negative_words_file)


# Function to clean and tokenize text
def clean_and_tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [re.sub(r'[^a-zA-Z]', '', token) for token in tokens]  # Remove punctuation
    tokens = [token for token in tokens if token and token not in stopwords]
    return tokens


# Function to calculate sentiment scores
def calculate_sentiment_scores(tokens):
    positive_score = sum(1 for word in tokens if word in positive_words)
    negative_score = sum(1 for word in tokens if word in negative_words)
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(tokens) + 0.000001)
    return positive_score, negative_score, polarity_score, subjectivity_score


# Function to calculate readability metrics
def calculate_readability_metrics(text):
    sentences = nltk.sent_tokenize(text)
    words = clean_and_tokenize(text)
    complex_words = [word for word in words if len(nltk.word_tokenize(word)) > 2]
    
    avg_sentence_length = len(words) / len(sentences)
    percentage_complex_words = len(complex_words) / len(words)
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    return avg_sentence_length, percentage_complex_words, fog_index


# Function to calculate other metrics
def calculate_other_metrics(tokens):
    word_count = len(tokens)
    complex_word_count = sum(1 for word in tokens if len(nltk.word_tokenize(word)) > 2)
    syllable_per_word = sum([len(re.findall(r'[aeiouy]', word)) for word in tokens]) / len(tokens)
    avg_word_length = sum(len(word) for word in tokens) / len(tokens)
    personal_pronouns = len(re.findall(r'\b(i|we|my|ours|us)\b', ' '.join(tokens)))
    return word_count, complex_word_count, syllable_per_word, avg_word_length, personal_pronouns


# Main processing function
def process_articles(input_df):
    output_data = []

    for _, row in input_df.iterrows():
        url_id = row['URL_ID']
        url = row['URL']

        # Extract article text
        response = requests.get(url)
        #Parse the webpage content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        #Find the element with the specific class
        content = soup.find('div', class_="td-post-content tagdiv-type")

        #Extract and print the text
        if content:
            text = content.get_text(separator=' ').strip()
        else:
            print("No content found with the specified class.")

        # Save article text to file
        with open(f'{url_id}.txt', 'w', encoding='utf-8') as file:
            file.write(text)
        
         # Tokenize and clean text
        tokens = clean_and_tokenize(text)

        # Sentiment analysis
        positive_score, negative_score, polarity_score, subjectivity_score = calculate_sentiment_scores(tokens)

        # Readability metrics
        avg_sentence_length, percentage_complex_words, fog_index = calculate_readability_metrics(text)

        # Other metrics
        word_count, complex_word_count, syllable_per_word, avg_word_length, personal_pronouns = calculate_other_metrics(tokens)

        # Collect output data
        output_data.append({
            'URL_ID': url_id,
            'URL': url,
            'POSITIVE SCORE': positive_score,
            'NEGATIVE SCORE': negative_score,
            'POLARITY SCORE': polarity_score,
            'SUBJECTIVITY SCORE': subjectivity_score,
            'AVG SENTENCE LENGTH': avg_sentence_length,
            'PERCENTAGE OF COMPLEX WORDS': percentage_complex_words,
            'FOG INDEX': fog_index,
            'AVG NUMBER OF WORDS PER SENTENCE': avg_sentence_length,
            'COMPLEX WORD COUNT': complex_word_count,
            'WORD COUNT': word_count,
            'SYLLABLE PER WORD': syllable_per_word,
            'PERSONAL PRONOUNS': personal_pronouns,
            'AVG WORD LENGTH': avg_word_length
        })

    # Convert output data to DataFrame and save to Excel
    output_df = pd.DataFrame(output_data)
    output_df.to_csv('Output Data Structure.csv', index=False)


# Run the processing function
process_articles(input_df)


