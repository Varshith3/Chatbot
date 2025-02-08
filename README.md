# Chatbot

## I made this chatbot using Langchain and Cohere LLM
I used Cohere instead openai because my credits was expired inorder to use openai so i choose cohere.

## Process
I loaded the data using URL loader and created a file with the extracted text data and converted the text into chunks and created embeddings by using cohere embeddings and stored the embeddings in Langchain vectorstore which is FAISS. 

## Clone this repository
Clone this repository by using git clone https://github.com/Varshith3/Chatbot.git \n
Install the dependencies mentioned in the file \n
Add your Cohere API KEY in a .env file \n
Run the python application \n
By using postman or curl send a POST request to '/chat' in json format \n
{ \n
  "query": "Tell me the about the available courses" \n
} \n
