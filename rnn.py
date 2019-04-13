import numpy as np # linear algebra
from keras.preprocessing.sequence import pad_sequences
import re
import tensorflow as tf

import pickle
def savetofile(obj,filename):
    pickle.dump(obj,open(filename+".p","wb"))
def openfromfile(filename):
    temp = pickle.load(open(filename+".p","rb"))
    return temp

tokenizer = openfromfile("rnntokenizer")
model = openfromfile("rnnmodel")

def clean_rnn(x):
    
    x = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', '', str(x), flags=re.MULTILINE)
    x = x.lower()
    x = re.sub('[^a-zA-z0-9\s]','',x)
    x = re.sub('\s+',' ', x)
    
    return x

def fbsrnn(text):
    text = clean_rnn(text)
    cmt = []
    cmt.append(text)
    #vectorizing the tweet by the pre-fitted tokenizer instance
    cmt = tokenizer.texts_to_sequences(cmt)
    #padding the tweet to have exactly the same shape as `embedding_2` input
    cmt = pad_sequences(cmt, maxlen=40, dtype='int32', value=0)
    #print(twt)
    sentiment = model.predict(cmt,batch_size=1,verbose = 2)[0]
    tf.logging.set_verbosity(tf.logging.ERROR)
    if(np.argmax(sentiment) == 0):
        return 'Negative'
    elif (np.argmax(sentiment) == 1):
        return 'Positive'
        
'''       
txt = input("Enter the feedback: ")
fbsrnn(txt)'''