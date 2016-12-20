import sys, json, pandas as pd
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

def read_in():
    lines = sys.stdin.readlines()
    # Since our input would only be having one line, parse our JSON data from that
    return json.loads(lines[0])

def main():
    #get our data as an array from read_in()
    #lines = sys.stdin.readlines()
    #lines = json.loads(lines[0])

    #create a numpy array
    input_data = np.array(read_in())


    stop_Words = stopwords.words('english')
    pipeline = Pipeline([
        ('bow', CountVectorizer(stop_words=stop_Words)),
        ('tfidf', TfidfTransformer()),
        ('classifier', MultinomialNB())
    ])

    search_criteria = input_data

    stop_Words = stopwords.words('english')
    df = pd.read_csv('document-data.csv')

    x_data = df['description']
    y_data = df['id']

    model = pipeline.fit(x_data,y_data)
    prediction_prob = model.predict_proba(search_criteria)
    df1 = pd.DataFrame(prediction_prob[0], columns=['probability'])
    result = pd.concat([df, df1], axis=1)
    result.sort_values(by='probability', ascending=False, inplace=True)

    print(result.head(5))
    sys.stdout.flush()

# Start process
if __name__ == '__main__':
    main()