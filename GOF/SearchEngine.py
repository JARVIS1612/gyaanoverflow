import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from numpy.linalg import norm
import nltk

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('omw-1.4')

def TextPreprocessing(text):
    if not text:
        return
    # print("text", text)
    words = text.split(" ")

    text_ = " ".join(words)
    words = word_tokenize(text_)
    
    stopwords_ = stopwords.words('english')
    words_ = []
    for i in words:
        if i not in stopwords_ and i not in "`~!@#$%^&*()_-+={}[]:;\"\'<>,.?/":
            words_.append(i)
            
    wnl = WordNetLemmatizer()
    for i in range(len(words_)):
        words_[i] = wnl.lemmatize(words_[i])
    
    return " ".join(words_)



def mini_search(que_dataset, query):
    que_texts = []
    que_ids = []
    comment_texts = []
    tags = []
    for que in que_dataset:
        #make a set of questions
        que_texts.append(que['question'])
        que_ids.append(que['_id'])
        
        #make a set of comments
        comments = []
        for comment in que['comments']:
            comments.append(comment['comment'])
        comment_texts.append(comments)

        #make a set of tags
        tags.append(" ".join(que['tags']))

    print("que_texts:",que_texts)
    print("comment_texts:",comment_texts)

    size = len(que_texts)
    doc_content = []

    #combine the set of questions and answers
    for i in range(size):
        str_ = que_texts[i] + " " + " ".join(comment_texts[i])
        doc_content.append(str_)

    print("doc_content:",doc_content)    

    # Pre process the text
    pre_processed_text = []
    for i in doc_content:
        # print("i", i)
        if i:
            temp = TextPreprocessing(i)
            if temp:
                pre_processed_text.append(temp)

    # print(pre_processed_text)

    #combine set of comments with preprocessed text
    for i in range(len(tags)):
        pre_processed_text[i] = pre_processed_text[i] + " " + tags[i]

    print(pre_processed_text)

    tfidf = TfidfVectorizer(ngram_range=(1,5), max_features=50000)
    matrix = tfidf.fit_transform(pre_processed_text)


    pre_processed_text.append(TextPreprocessing(query))
    matrixq = tfidf.transform(pre_processed_text)

    matrixq = matrixq.todense().tolist()[size]
    matrix = matrix.todense().tolist()

    matrixq = np.array(matrixq)
    matrix = np.array(matrix)

    cosine = np.sum(matrix*matrixq, axis=1)/norm(matrix, axis=1)*norm(matrixq)

    df = pd.DataFrame()
    df['doc'] = que_ids
    df['similarity'] = cosine
    df = df.sort_values(by="similarity", ascending=False)
    print(df[df.similarity > 0])

    return list(df[df.similarity > 0]['doc'])