from glob import glob
import requests
import zipfile
import io
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma

EMBEDDING_EP = os.environ.get("EMBEDDING_EP", "***")

embeddings = HuggingFaceEndpointEmbeddings(model=EMBEDDING_EP)

print("Downloading prompt engineering guide")
url = 'https://github.com/bundestag/gesetze/archive/refs/heads/master.zip'
response = requests.get(url)
with zipfile.ZipFile(io.BytesIO(response.content)) as the_zip_file:
    the_zip_file.extractall('/data') 

text_splitter = text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=500)

texts = list(glob("/data/gesetze-master/g/geg/*.md"))
chunks = []

for doc in texts:
    with open(doc) as f:
        for chunk in text_splitter.split_text(f.read()):
            try:
                chunks.append(chunk)
            except Exception as ex:
                print(doc, len(chunk), "not processable", str(ex))

print("Generate semantic index for prompt engineering guide")
vectorstore = Chroma.from_texts(chunks, embeddings, persist_directory="/data")
