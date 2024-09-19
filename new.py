
from langchain_community.document_loaders import CSVLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
loader = CSVLoader(file_path='student_details.csv')
embedding = OpenAIEmbeddings()
index_creator = VectorstoreIndexCreator(embedding=embedding)
docsearch = index_creator.from_loaders([loader])