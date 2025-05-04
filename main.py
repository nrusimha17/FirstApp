import streamlit as st
import os
import requests
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.chat_models import ChatOpenAI

#Load secrets from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

#setup streamlit UI
st.title("Results Analysis")
st.subheader("Latest data using GPT + Serper")

topic = st.text_input("Company Name")
number = st.number_input("Number of Lines", min_value=10, max_value=100, value=10)

def run_serper_search(query):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
    results = response.json()
   
    if "organic" in results:
        return "\n\n".join([f"{r['title']}: {r['link']}" for r in results["organic"][:5]])
    else:
        return "No search results found"

#On generate button click
if st.button("Generate") and topic:
    web_results = run_serper_search(topic)

    tweet_template = """
    use the following recent Google search results to analyse latest results of the company: "{topic}" and write a summary in {number} lines. 
    Outline most important points about revenue, margins, growth prospects
    search results:
    {web_results}
    Add analysts' estimates about the stock price direction.
    """

    prompt = PromptTemplate(
        input_variables=["number", "topic", "web_results"],
        template=tweet_template
    )

    llm = ChatOpenAI (model_name="gpt-4o",temparature=0.7)
    #gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")
    chain = LLMChain(prompt=prompt, llm=llm)
    #review_chain = review_prompt | gemini_model
    #chain = LLMChain(prompt=prompt, llm=gemini_model)
    output = chain.invoke(
        {
            "number": number,
            "topic": topic,
            "web_results": web_results
        })  
    st.markdown("### Generated analysis")
    st.write(output["text"])
