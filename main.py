import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from langchain_cohere import ChatCohere
from langchain_community.document_loaders import UnstructuredURLLoader, TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv


# Load environment variables
load_dotenv()
api_key = os.getenv('COHERE_API_KEY')


# Loading the data using URL Loader
url = ["https://brainlox.com/courses/category/technical"]
loader = UnstructuredURLLoader(urls=url)
docs = loader.load()


# Creating a new file with extracted content
with open("extracted_content.txt", "w", encoding="utf-8") as file:
    for doc in docs:
        file.write(doc.page_content)


# LLM
llm = ChatCohere(model="command-xlarge-nightly", cohere_api_key=api_key)


# Extracting text from the document
raw_documents = TextLoader('extracted_content.txt').load()
text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=0)
documents = text_splitter.split_documents(raw_documents)


# Creating embeddings for the text
embeddings = CohereEmbeddings(model="embed-english-v2.0", cohere_api_key=api_key)


# Storing the embeddings in the vector store
db = FAISS.from_documents(documents, embeddings)


# Set up Flask app
app = Flask(__name__)
api = Api(app)


# Chatbot
class Chatbot(Resource):
    def post(self):
        try:
            user_query = request.json.get("query")
            if not user_query:
                return {"error": "Please provide a query"}, 400

            # Search similar documents
            docs = db.similarity_search(user_query)
            relevant_info = "\n".join([doc.page_content for doc in docs]) if docs else "No relevant info found."

            # Fetch Cohere LLM response
            response = llm.predict(f"User asked: '{user_query}'. Here's relevant info: {relevant_info}")
            clean_response = response.replace("\n", " ").strip()
            return jsonify({"response": clean_response})
        
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

api.add_resource(Chatbot, "/chat")

if __name__ == '__main__':
    app.run(debug=True)