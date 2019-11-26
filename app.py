from flask import Flask, render_template, request, redirect
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

class InvertedIndex:
    def __init__(self):
        self.dict = {}

    def insert(self,word,document,position):
        if self.dict.get(word)==None:
            self.dict[word.lower()] = [[document,position]]
        else:
            self.dict[word.lower()].append([document,position])

    def find(self,word):
        try:
            positions = self.dict[word]
        except:
            return "No match found" 
        document = [i[0] for i in positions]
        count_document = Counter(document)
        sorted_documents = [[count_document[i],i] for i in count_document]
        sorted_documents.sort(reverse=True)
        final_documents = [i[1] for i in sorted_documents]
        print(sorted_documents)
        return final_documents[:10]

    def clean(self):
        self.dict = {}

def tokenize():
    text, orignal_text = readfile('text.txt')
    # print(*text[:5])
    invertedIndex = InvertedIndex()
    for i in range(len(text)):
        for j in range(len(text[i])):
            invertedIndex.insert(text[i][j],i,j)
    return invertedIndex,orignal_text

@app.route('/')
def index():
    return flask.render_template('./index.html')

@app.route('/search',methods=['POST','GET'])
def search():

    global text, invertedIndex
    if request.method == 'POST':
        word_to_search = request.form['search']
        results = invertedIndex.find(word_to_search)
        if type(results)==str:
            return render_template('search.html',word = word_to_search)
        else:
            ans = []
            for result in results:
                ar = text[result]
                ar = ' '.join(ar)
                sentence = ar
                ans.append([result,sentence])
            return render_template('search.html',results = ans,word = word_to_search)
    else:
        return redirect("/")

@app.route('/insert',methods=['GET','POST'])
def insert():
    global text, invertedIndex
    if request.method=='POST':
        textarea = request.form['text']
        texts = textarea.split('\n\n')
        for document in texts:
            writefile('text.txt',document)
            # Cleaning the paragraph
            document = cleaning(document)
            text.append(document)
            # Write the new lines file
            words = document.split()
            # Inserting new words to Index
            document_no = len(text)
            for j in range(len(words)):
                invertedIndex.insert(document[j],document_no,j)
        return render_template('index.html')   
    else:
        return render_template('insert.html')

@app.route('/clean',methods=['GET'])
def clean():
    global invertedIndex
    invertedIndex.clean()
    return redirect("/")

invertedIndex = None
if __name__=="__main__":
    global text 
    invertedIndex, text = tokenize()
    text = [i.split() for i in text]
    app.run(use_reloader=True, debug=True)

