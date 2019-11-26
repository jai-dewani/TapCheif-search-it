from flask import Flask, render_template, request, redirect
import flask
from collections import Counter
app = Flask(__name__)

'''
Cleans the document of special characters like '",.-()
'''
def cleaning(document):
    document = document.replace(',','').replace('.','').replace('"','').replace('-','').replace('-','').replace(')','').replace('(','')
    return document

'''
Reads text.txt amd return the documents sperated and cleaned.
'''
def readfile(filename):
    f = open('text.txt','r')
    text = f.read()
    return1 = text.split('\n\n')
    split_document = text.split('\n\n')
    for i in range(len(split_document)):
        clean_doc = cleaning(split_document[i])
        split_document[i] = clean_doc.split()    
    return split_document,return1

'''
Writes all the new documents back to text.txt
'''
def writefile(filename,text):
    f = open(filename,'a+')
    f.write(text+'\n\n')
    f.close()

'''
Main class, stores words with their document number and position. 
'''
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

'''
Read text.txt and creates a initial inverted index object.
'''
def tokenize():
    text, orignal_text = readfile('text.txt')
    # print(*text[:5])
    invertedIndex = InvertedIndex()
    for i in range(len(text)):
        for j in range(len(text[i])):
            invertedIndex.insert(text[i][j],i,j)
    return invertedIndex,orignal_text

'''
Home route, return a home page
'''
@app.route('/')
def index():
    return flask.render_template('./index.html')

'''
Search route, redirects to home page on a GET request and returns a list of document on a POST request with a search key
'''
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
                sentence = ar
                ans.append([result,sentence])
            return render_template('search.html',results = ans,word = word_to_search)
    else:
        return redirect("/")

'''
Insert route, redirects to homepage on a GET request and accepts a document or a list of documents seprated by two newlines in POST request and adds all of them to the index.
'''
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

'''
Clean route, Deletes all the index form memory
'''
@app.route('/clean',methods=['GET'])
def clean():
    global invertedIndex
    invertedIndex.clean()
    return redirect("/")

# Genrates object of Inverted Index and text from text.txt
invertedIndex, text = tokenize()
if __name__=="__main__":
    # text = [i.split() for i in text]
    app.run(use_reloader=True, debug=True)
