import streamlit as st
import os
import requests
from langchain import PromptTemplate, LLMChain
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

#Load secrets from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

#setup streamlit UI
st.title("Results Analysis")
st.subheader("Financial Analysis powered by GPT + Serper")

topic = st.text_input("Company Name")
number = st.number_input("Number of Lines", min_value=5, max_value=200, value=10)

# define function to search using Serper
def run_serper_search(query):
    headers = {
        "X-API-KEY": SERPER_API_KEY,
        "Content-Type": "application/json"
    }
    data = {"q": query, "num":10}
    response = requests.post("https://google.serper.dev/search", headers=headers, json=data)
    results = response.json()
   
    if "organic" in results:
        return "\n\n".join([f"{r['title']}: {r['link']}" for r in results["organic"]])
    else:
        return "No search results found"

#On generate button click
if st.button("Generate") and topic:
    query = f"{topic} Q4 results April 2025 site:moneycontrol.com OR site:economictimes.indiatimes.com OR site:livemint.com"
    st.markdown(f"**Search Query Used:** `{query}`")
    web_results = run_serper_search(query)
    
    tweet_template = """
    Use the following recent news articles to analyze the **latest quarterly financial results** of the company: "{topic}". Write a concise summary in {number} lines.
    Focus on:
    - Revenue and profit changes
    - Growth outlook
    - Margins and cost trends
    - Analyst commentary or stock guidance
    
    search results:
    {web_results}
    Make your tone analytical and factual. DO NOT repeat headlines or mention search results.
    """

    prompt = PromptTemplate(
        input_variables=["number", "topic", "web_results"],
        template=tweet_template
    )

    llm = ChatOpenAI(model_name="gpt-4o", temparature=0.7)
    chain = LLMChain(prompt=prompt, llm=llm)
    
    #gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")
    #review_chain = review_prompt | gemini_model
    #chain = LLMChain(prompt=prompt, llm=gemini_model)
    
    # Run the chain
    output = chain.invoke({
            "number": number,
            "topic": topic,
            "web_results": web_results
        })  
    #display result
    st.markdown("### Generated analysis")
    st.write(output["text"])
