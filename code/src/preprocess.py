import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import re 
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('stopwords') 
nltk.download('wordnet') 
stop_words = set(stopwords.words('english')) 
lemmatizer = WordNetLemmatizer()

def clean_text(text, remove_stopwords=True):
    if pd.isna(text):
        return ""
    text = str(text).lower()  # Convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)  # Remove special characters
    words = text.split()
    
    # Keep critical words in debugging steps by skipping stopword removal
    if remove_stopwords:
        words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]
    else:
        words = [lemmatizer.lemmatize(word) for word in words]
    
    return " ".join(words)

def load_and_preprocess_data(filename):
    # Load dataset
    df = pd.read_csv(filename)

    # Select relevant columns
    df = df[['Incident Name', 'Incident Description', 'Resolution', 'First Debugging Step', 'Communication Log', 'Debugging Steps']]

    # Drop any missing values
    #df.dropna(inplace=True)

    # Fill missing values with placeholders
    df.fillna({'Incident Name': 'Unknown Incident', 'Incident Description': 'No Description', 'Resolution': 'No Resolution', 'First Debugging Step': 'Unknown Step'}, inplace=True)

    #Ensure no NaN values remain
    df.fillna('', inplace=True)

    # Convert all values to strings before cleaning
    df['Incident Name'] = df['Incident Name'].astype(str)
    df['Incident Description'] = df['Incident Description'].astype(str)
    df['Resolution'] = df['Resolution'].astype(str)
    df['First Debugging Step'] = df['First Debugging Step'].astype(str)
    df['Communication Log'] = df['Communication Log'].astype(str)

    # Clean text fields
    df['Incident Name'] = df['Incident Name'].apply(lambda x: clean_text(x, remove_stopwords=False))
    df['Incident Description'] = df['Incident Description'].apply(lambda x: clean_text(x, remove_stopwords=False))
    df['Resolution'] = df['Resolution'].apply(lambda x: clean_text(x, remove_stopwords=False))
    df['First Debugging Step'] = df['First Debugging Step'].apply(lambda x: clean_text(x, remove_stopwords=False))  # No stopword removal

    # Combine text fields into a single string for each row
    df['combined_text'] = df[['Incident Name', 'Incident Description', 'Resolution', 'First Debugging Step', 'Communication Log']].apply(lambda x: ' '.join(x), axis=1)

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(df['combined_text'], df['Debugging Steps'], test_size=0.2, random_state=42)

    # Convert text data into numerical format using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    return X_train_tfidf, X_test_tfidf, y_train, y_test, vectorizer
