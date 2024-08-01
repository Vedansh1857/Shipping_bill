import os
# import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import asyncio
import concurrent.futures

# Load environment variables from .env file
load_dotenv()

# Configure the Google Generative AI API with the API key from the environment variable
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Extracting the PDFs content concurrently...
def get_pdf_text(pdf_docs):
    def extract_text(pdf):
        text = ""
        doc = PdfReader(pdf)
        for page in doc.pages:
            text += page.extract_text()
        return text
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        texts = executor.map(extract_text, pdf_docs)
    
    return "".join(texts)

# Dividing the texts into smaller chunks...
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Convert these chunks into vectors...
def get_vector_stores(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_stores = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_stores.save_local("faiss-index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "n/a", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Questions: \n{questions}\n
    Answers:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "questions"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

async def get_batch_response(questions, embeddings, vector_stores, semaphore, retries=3):
    async with semaphore:
        for attempt in range(retries):
            try:
                loop = asyncio.get_event_loop()
                docs = await loop.run_in_executor(None, vector_stores.similarity_search, questions)
                chain = get_conversational_chain()
                response = await loop.run_in_executor(None, chain, {"input_documents": docs, "questions": questions}, True)
                return response["output_text"]
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for questions '{questions}' with error: {e}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
        raise Exception(f"Failed to get response for questions '{questions}' after {retries} attempts")

def generate_question(field_id):
    return f"{field_id}?"

# Process the PDFs and create the FAISS index
pdf_docs = [r"D:/PinkmoonAI/invoice1r.pdf", r"D:/PinkmoonAI/pl1r.pdf"]
raw_text = get_pdf_text(pdf_docs)
text_chunks = get_text_chunks(raw_text)
get_vector_stores(text_chunks)

# Load the vector stores and embeddings once
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
vector_stores = FAISS.load_local("faiss-index", embeddings, allow_dangerous_deserialization="True")

# Set up the webdriver for Edge
edge_options = Options()
edge_options.use_chromium = True

driver = webdriver.Edge(options=edge_options)

async def collect_batch_data(batch, semaphore):
    batch_data = {}
    questions = []
    field_ids = []
    
    for element in batch:
        field_id = element.get_attribute("id")
        if field_id:
            if field_id == "User-Job-Date":
                current_date = datetime.now().strftime("%d-%m-%Y")
                batch_data[field_id] = current_date
            elif field_id == "Supporting_Documents_Upload":
                file_path = r"D:/PinkmoonAI/invoice1r.pdf"
                batch_data[field_id] = file_path
            else:
                question = generate_question(field_id)
                questions.append(question)
                field_ids.append(field_id)
    
    combined_questions = "\n".join(questions)
    response = await get_batch_response(combined_questions, embeddings, vector_stores, semaphore)
    answers = response.split('\n')
    
    # Debugging: Print the raw response
    print("Raw response received:")
    print(response)
    
    for field_id, answer in zip(field_ids, answers):
        # Ensure only the answer part is filled in the field
        if '?' in answer:
            answer = answer.split('?', 1)[-1].strip()
        batch_data[field_id] = answer.strip()
    
    # Debugging: Print the batch data
    print("Batch data to be filled:")
    print(batch_data)
    
    return batch_data

async def fill_field(element, answer):
    # Debugging: Print the field ID and the answer being filled
    print(f"Filling field {element.get_attribute('id')} with answer: {answer}")
    element.clear()
    element.send_keys(answer)

async def fill_fields_in_batches(elements, batch_size, delay, semaphore):
    for i in range(0, len(elements), batch_size):
        batch = elements[i:i + batch_size]
        try:
            batch_data = await collect_batch_data(batch, semaphore)
            tasks = [fill_field(element, batch_data[element.get_attribute("id")]) for element in batch if element.get_attribute("id") in batch_data]
            await asyncio.gather(*tasks)
        except Exception as e:
            print(f"An error occurred while processing batch {i // batch_size}: {e}")
        await asyncio.sleep(delay)

try:
    # Open the webpage
    driver.get("https://shippingbill.onrender.com")
    driver.maximize_window()

    # Retrieve all input fields
    all_elements = driver.find_elements(By.TAG_NAME, "input")
    excluded_ids = ['Adress1', 'City', 'Pin']

    # Filter out excluded elements
    filtered_elements = []
    for element in all_elements:
        # if element.get_attribute('name') in excluded_names:
        #     continue
        if element.get_attribute('id') in excluded_ids:
            continue
        # if any(cls in excluded_classes for cls in element.get_attribute('class').split()):
        #     continue
        filtered_elements.append(element)

    # Define a semaphore to limit concurrent requests
    semaphore = asyncio.Semaphore(2)  # Adjust the number of concurrent requests as needed

    # Run the async function
    asyncio.run(fill_fields_in_batches(filtered_elements, batch_size=100, delay=2, semaphore=semaphore))

    print(f"Processing element: {element.get_attribute('id')}")

except Exception as e:
    print(f"An error occurred: {e}")

# finally:
#     driver.quit()