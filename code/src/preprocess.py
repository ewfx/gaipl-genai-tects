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

def clean_text(text): 
    if pd.isna(text): 
        return "" 
    text = text.lower() 
    # Convert to lowercase 
    text = re.sub(r'[^a-zA-Z0-9 ]', '', text)
    # Remove special characters
    words = text.split() 
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  
    # Lemmatization & stopword removal 
    return " ".join(words)


def load_and_preprocess_data(filename):
    # Load dataset
    df = pd.read_csv(filename)

    # Select relevant columns
    df = df[['Incident Name', 'Incident Description', 'Resolution', 'First Debugging Step']]

    # Drop any missing values
    #df.dropna(inplace=True)

    # Fill missing values with placeholders
    df.fillna({'Incident Name': 'Unknown Incident', 'Incident Description': 'No Description', 'Resolution': 'No Resolution', 'First Debugging Step': 'Unknown Step'}, inplace=True)

    # Clean text fields
    df['Incident Name'] = df['Incident Name'].apply(clean_text)
    df['Incident Description'] = df['Incident Description'].apply(clean_text)
    df['Resolution'] = df['Resolution'].apply(clean_text)
    df['First Debugging Step'] = df['First Debugging Step'].apply(clean_text)


    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(df[['Incident Name', 'Incident Description', 'Resolution']], df['First Debugging Step'], test_size=0.2, random_state=42)

    # Convert text data into numerical format using TF-IDF
    vectorizer = TfidfVectorizer()
    X_train_tfidf = vectorizer.fit_transform(X_train.apply(lambda x: ' '.join(x), axis=1))
    X_test_tfidf = vectorizer.transform(X_test.apply(lambda x: ' '.join(x), axis=1))

    return X_train_tfidf, X_test_tfidf, y_train, y_test, vectorizer
