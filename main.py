from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import LLMChain
from langchain import PromptTemplate

import streamlit as st
import os

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']

# Create prompt template for generating tweets

review_template = "Answer in {number} lines about the question {book}"

review_prompt = PromptTemplate(template = review_template, input_variables = ['number', 'book'])

# Initialize Google's Gemini model
gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")


# Create LLM chain using the prompt template and model
review_chain = review_prompt | gemini_model


import streamlit as st

st.header("Current Affairs")

st.subheader("By Generative AI")

book = st.text_input("Ask your Question")

number = st.number_input("Number of Lines", min_value = 5, max_value = 50, value = 5, step = 1)

if st.button("Generate"):
    reviews = review_chain.invoke({"number" : number, "book" : book})
    st.write(reviews.content)
    
