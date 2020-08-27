import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re
import os

def Corpus_Cleaner():

    # clean the manually sorted reviews for training
    pos = os.listdir('txt_sentoken/pos')
    neg = os.listdir('txt_sentoken/neg')

    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    # change this line to this to neg or pos
    for review in pos:
        # change this line to this to /neg or /pos
        review_file = 'txt_sentoken/pos/' + review
        open_file = open(review_file)
        review_lines = open_file.readlines()
        clean_lines = []
        
        for line in review_lines:

            # lower case, remove special characters, tokenize
            doc = nltk.word_tokenize(re.sub('[^a-zA-Z-]+', ' ', line.lower()))

            # remove stop words
            no_stop = [w for w in doc if not w in stop_words]

            # stemming words
            stem = ' '.join([ps.stem(w) for w in no_stop]).strip()

            # add the lines to a list if they are not empty
            if stem != '': clean_lines.append(stem)

        open_file.close()

        with open(review_file, 'w') as clean_file:
            clean_file.write('\n'.join(clean_lines))
            clean_file.close()

def IMDB_Cleaner(review):

    review_lines = review.splitlines()
    clean_lines = []
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()

    for i in [j for j in range(len(review_lines) - 2) if j != 2]:
        
        # lower case, remove special characters, tokenize
        doc = nltk.word_tokenize(re.sub('[^a-zA-Z-]+', ' ', review_lines[i].lower()))

        # remove stop words
        no_stop = [w for w in doc if not w in stop_words]

        # stemming words
        stem = ' '.join([ps.stem(w) for w in no_stop]).strip()

        # append lines to a list if they are not empty
        if stem != '': clean_lines.append(stem)

    # return the whole review after cleaning
    return ' '.join(clean_lines).replace('warning spoiler ', '')

#if __name__ == "__main__":
    #Corpus_Cleaner()