# TapSearch 
TapSearch is a simple web app that allows you to search through documents.
It uses an inverted index to speed up the process of searching.

## **How it works**  
Whenever a new document is inserted, it adds all the words to the inverted index. 
Whenever a user searches for a word top ten references to that word is returned 
(*top ten are calculated on the basis of how many time that word was encountered in document*)

## **How to use** 
- **Search:** It has already been given *text.txt* as input, so you can start finding different words in this collection of documents.
- **Delete** If you want to insert your own document ONLY, you will first need to remove all the existing ones. 
Delete functionality will do this for you. 
- **Insert:** You can also insert your own documents in searchable context through Insert function. 
More than one document can be inserted by keeping two newlines between them.

## **How to Build**
Clone this project on your system by running,
*make sure you have python3 and pip installed*

Downloads the project
```
git clone https://github.com/jai-dewani/TapCheif-search-it.git 
```
Change directory
```
cd TapCheif-search-it  
```
Intall all the dependencies
```
pip requirements.txt 
```
Start the main server
```
python app.py 
```
