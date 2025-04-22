from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import LLMChain
from langchain import PromptTemplate

import streamlit as st
import os

os.environ['GOOGLE_API_KEY'] = st.secrets['GOOGLE_API_KEY']

# Create prompt template for generating tweets

tweet_template = "Provide a brief review in {number} lines on the book {book}"

tweet_prompt = PromptTemplate(template = tweet_template, input_variables = ['number', 'book'])

# Initialize Google's Gemini model
gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")


# Create LLM chain using the prompt template and model
tweet_chain = tweet_prompt | gemini_model


import streamlit as st

st.header("BOOK REVIEW")

st.subheader("Reviews By Generative AI")

book = st.text_input("Name of the Book")

number = st.number_input("Number of Lines", min_value = 5, max_value = 50, value = 1, step = 1)

if st.button("Generate"):
    tweets = tweet_chain.invoke({"number" : number, "book" : book})
    st.write(tweets.content)
    
