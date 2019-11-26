from flask import Flask, render_template, request
import flask
from collections import Counter
app = Flask(__name__)


def cleaning(document):
    document = document.replace(',','').replace('.','').replace('"','').replace('-','').replace('-','').replace(')','').replace('(','')
    return document

def readfile(filename):
    f = open('text.txt','r')
    text = f.read()
    split_document = text.split('\n\n')
    for i in range(len(split_document)):
        clean_doc = cleaning(split_document[i])
        # clean_doc.split()
        split_document[i] = clean_doc.split()    
    # print(split_document[:5])
    return split_document,text.split('\n\n')

def writefile(filename,text):
    f = open(filename,'a+')
    f.write(text+'\n\n')
    f.close()

def readimdb():
    f = open('IMDB Dataset.csv','r+')
    i = 0
    while(i<50000):
        r = f.readline()
        # print(i,r)
        r = r.split(',')
        r = r[:-1]
        r = ','.join(r)
        r = r.replace('<br />','')
        # print(r)
        writefile('text.txt',r)
        # i+=1
        # print(i)
    f.close()


class InvertedIndex:
    def __init__(self):
        self.dict = {}
    def insert(self,word,document,position):
        if self.dict.get(word)==None:
            self.dict[word.lower()] = [[document,position]]
        else:
            self.dict[word.lower()].append([document,position])
    def find(self,word):
        positions = self.dict[word]
        document = [i[0] for i in positions]
        
        return 

print("START")

def tokenize():
    text, orignal_text = readfile('text.txt')
    # print(*text[:5])
    invertedIndex = InvertedIndex()
    for i in range(len(text)):
        for j in range(len(text[i])):
            invertedIndex.insert(text[i][j],i,j)
    return invertedIndex,orignal_text
    # word = input("Enter a word ")
    # ans = invertedIndex.find(word)
    # for i in range(min(10,len(ans))):
    #     a = ans[i]
    #     print(text[a[0]][a[1]:a[1]+10])
    # print(ans[:min(10,len(ans))])

@app.route('/')
def hello_word():
    return flask.render_template('./index.html')

@app.route('/search',methods=['POST','GET'])
def search():
    global text
    if request.method == 'POST':
        word_to_search = request.form['search']
        results = invertedIndex.find(word_to_search)
        ans = []
        for result in results:
            start = result[1]-5
            end = result[1]+5
            print(text[0:10])
            ar = text[result[0]]
            ar.split(word_to_search)

            sentence = ' '.join(ar)

            ans.append([result[0],sentence])
        return render_template('search.html',results = ans,word = word_to_search)
    else:
        return flask.render_template('./index.html')


if __name__=="__main__":
    global invertedIndex, text 
    invertedIndex, text = tokenize()
    print(text[0:2])
    text = [i.split() for i in text]
    app.run(use_reloader=True, debug=True)