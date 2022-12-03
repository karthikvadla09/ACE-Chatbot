#importing all the libraries and scripts
import nltk
import random
import string
from tkinter import *
import re, string, unicodedata
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import wikipedia as wk
from collections import defaultdict
import warnings


nltk.download('omw-1.4')
nltk.download('averaged_perceptron_tagger')

warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, linear_kernel

#importing raw data
data = open("HS.txt", 'r', errors='ignore')
raw = data.read()
raw = raw.lower()


sent_tokens = nltk.sent_tokenize(raw)

#Praising the content retrieved
def Normalize(text):
    remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
    # word tokenization
    word_token = nltk.word_tokenize(text.lower().translate(remove_punct_dict))

    # remove ascii
    new_words = []
    for word in word_token:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        new_words.append(new_word)

    # Remove tags
    rmv = []
    for w in new_words:
        text = re.sub("&lt;/?.*?&gt;", "&lt;&gt;", w)
        rmv.append(text)

    # pos tagging and lemmatization
    tag_map = defaultdict(lambda: wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    lmtzr = WordNetLemmatizer()
    lemma_list = []
    rmv = [i for i in rmv if i]
    for token, tag in nltk.pos_tag(rmv):
        lemma = lmtzr.lemmatize(token, tag_map[tag[0]])
        lemma_list.append(lemma)
    return lemma_list

#General input for welcome message
welcome_input = ("hello", "hi", "greetings", "sup", "what's up", "hey",)
welcome_response = ["hi", "hey", "nods", "hi there", "hello", "I am glad! You are talking to me"]

#Welcome message
def welcome(user_response):
    for word in user_response.split():
        if word.lower() in welcome_input:
            return random.choice(welcome_response)

#Generating response
def generateResponse(user_response):
    robo_response = ''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=Normalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    # vals = cosine_similarity(tfidf[-1], tfidf)
    vals = linear_kernel(tfidf[-1], tfidf)
    idx = vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if (req_tfidf == 0) or "tell me about" in user_response:
        print("Checking Wikipedia")
        if user_response:
            robo_response = wikipedia_data(user_response)
            return robo_response
    else:
        robo_response = robo_response + sent_tokens[idx]
        return robo_response  # wikipedia search nltk.download('omw-1.4')

#searhing the wikipedia
def wikipedia_data(input):
    reg_ex = re.search('tell me about (.*)', input)
    try:
        if reg_ex:
            topic = reg_ex.group(1)
            wiki = wk.summary(topic, sentences=3)
            return wiki
    except Exception as e:
        print("No content has been found")

def printInput():
    flag = True
    #while (flag == True):
    user_response = inputtxt.get(1.0,"end-1c")
    user_response = user_response.lower()
    if (user_response not in ['bye', 'shutdown', 'exit', 'quit']):
        if (user_response == 'thanks' or user_response == 'thank you'):
            flag = False
            print("Chatterbot : You are welcome..")
        else:
            if (welcome(user_response) != None):
                print("Chatterbot : " + welcome(user_response))
                #outputtxt.insert(root.END, robo_response)
            else:
                print("Chatterbot : ", end="")
                response = generateResponse(user_response)
                outputtxt.insert(END, response)
                sent_tokens.remove(user_response)

#deleting the text
def delete_text():
    inputtxt.delete("1.0","end")
    outputtxt.delete("1.0","end")

#Interface for the chatbot
root = Tk()
root.title("Chatbot")

f1 = Frame(root, padx=15, pady=10)
b1 = Button(root, text="SEND", command=printInput)
b2 = Button(root, text="DELETE", command=delete_text)
inputtxt = Text(f1, height=15, width=40)
outputtxt = Text(f1, height=15, width=40)

inputtxt.pack()
f1.pack()
outputtxt.pack()
b1.pack()
b2.pack()
root.mainloop()
