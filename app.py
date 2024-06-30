import streamlit as st
import requests
from langchain_groq import ChatGroq

# Initialize the LLM with the provided API key and model name
llm = ChatGroq(temperature=0.5, groq_api_key="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", model_name="llama3-70b-8192")

def search_query(query):
    # Base URL for the API
    base_url = "https://api.tavily.com/"
    
    # Endpoint for the search
    endpoint = "search"
    
    # Request payload
    payload = {
        "api_key": "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",
        "query": query,
        "search_depth": "basic",
        "include_answer": True,
        "include_images": False,
        "include_raw_content": False,
        "max_results": 3,
        "include_domains": [],
        "exclude_domains": []
    }
    
    # Make the POST request
    response = requests.post(f"{base_url}{endpoint}", json=payload)
    
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()
        
        # Extract and return the answer and results
        answer = data.get("answer", "")
        results = data.get("results", [])
        
        return answer, results
    else:
        return None, None

def generate_faq_from_info(info):
    # Prepare the prompt with the gathered information
    prompt = f'''
    ### Instructions ###
    Based on the following information, generate 20 frequently asked questions (FAQs) related to the product. Each FAQ should be clear and concise, providing useful information about the product.
    
    Information:
    {info}
    
    ### FAQs ###
    1.
    2.
    3.
    4.
    5.
    6.
    7.
    8.
    9.
    10.
    11.
    12.
    13.
    14.
    15.
    16.
    17.
    18.
    19.
    20.
    '''
    
    # Call the LLM to generate the FAQs
    response = llm.invoke(prompt)
    return response.content

def generate_faqs(product: str):
    # Step 1: Use Tavily to gather information about the product
    answer, results = search_query(product)
    
    # Combine the gathered information into a single string
    combined_info = answer + "\n" + "\n".join([result['title'] + ": " + result['url'] for result in results])
    
    # Step 2: Use the LLM to generate 20 FAQs based on the gathered information
    faqs = generate_faq_from_info(combined_info)
    
    return faqs

def answer_question(faqs, question):
    # Prepare the prompt with the FAQs and the new question
    prompt = f'''
    ### Instructions ###
    Based on the following FAQs, answer the new question about the product.
    
    FAQs:
    {faqs}
    
    New Question:
    {question}
    
    Answer:
    '''
    
    # Call the LLM to answer the question
    response = llm.invoke(prompt)
    return response.content

# Streamlit app
st.title("Product FAQ Generator and Q&A")

# Input product description
product_description = st.text_input("Enter the product description:")


if product_description:
    # Generate FAQs
    faqs = generate_faqs(product_description)
    st.markdown("## Generated FAQs: ##")
    st.markdown(faqs)

    # Input new question
    new_question = st.text_input("Enter your question about the product:")
    
    if new_question:
        # Answer the new question based on the generated FAQs
        answer = answer_question(faqs, new_question)
        st.markdown("## Answer to the new question: ##")
        st.markdown(answer)
