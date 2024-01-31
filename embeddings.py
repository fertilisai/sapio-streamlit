import tempfile
from langchain.chat_models import ChatOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.document_loaders import Docx2txtLoader
from langchain.document_loaders import TextLoader
# from langchain.document_loaders import UnstructuredODTLoader
# from langchain.document_loaders import UnstructuredURLLoader


def load_docs(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        docs = parse_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".txt"):
        docs = parse_txt(uploaded_file)
    # elif uploaded_file.name.endswith(".docx"):
    #     docs = parse_docx(uploaded_file)
    # loader = UnstructuredODTLoader("example_data/fake.odt", mode="elements")
    # loader = UnstructuredURLLoader(urls=urls)
    else:
        raise ValueError("File type not supported!")
    return docs


def create_temp_file(uploaded_file):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as temp_file:
            temp_file.write(uploaded_file.read())
    return temp_file.name


def parse_docx(file):
    temp_file = create_temp_file(file)
    loader = Docx2txtLoader(temp_file)
    doc = loader.load()
    return doc


def parse_pdf(file):
    temp_file = create_temp_file(file)
    loader = PyPDFLoader(temp_file)
    doc = loader.load()
    return doc


def parse_txt(file):
    temp_file = create_temp_file(file)
    loader = TextLoader(temp_file)
    doc = loader.load()
    return doc


def split_docs(docs, chunk_size=1000, chunk_overlap=0):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splits = text_splitter.split_documents(docs)
    return splits


def get_emb(splits):
    embeddings = OpenAIEmbeddings()
    db = FAISS.from_documents(splits, embeddings)
    # db.save_local("faiss_index")
    return db


def get_context_from_emb(db, query):
    # db = FAISS.load_local("faiss_index", embeddings)
    similar_docs = db.similarity_search(query)
    return similar_docs[0].page_content
