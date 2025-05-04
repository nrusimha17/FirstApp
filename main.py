import streamlit as st
import os
import requests
from langchain import PromptTemplate, LLMChain
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.chat_models import ChatOpenAI

#Load secrets from Streamlit secrets
os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
SERPER_API_KEY = st.secrets["SERPER_API_KEY"]

#setup streamlit UI
st.title("Real-time Tweet Generator")
st.subheader("Generate tweets using GPT + Serper")

topic = st.text_input("Enter a topic")
number = st.number_input("Enter the number of tweets", min_value=1, max_value=10, value=3)

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
    use the following recent Google search results to write {number} engaging tweets about: "{topic}"

    search results:
    {web_results}

    The tweets shoudl be creative, short and twitter-friendly.
    """

    prompt = PromptTemplate(
        input_variables=["number", "topic", "web_results"],
        template=tweet_template
    )

    #llm = ChatOpenAI (model_name="gpt-4o",temparature=0.7)
    gemini_model = ChatGoogleGenerativeAI(model = "gemini-1.5-flash-latest")
    #chain = LLMChain(prompt=prompt, llm=llm)
    review_chain = review_prompt | gemini_model
    chain = LLMChain(prompt=prompt, llm=gemini_model)
    output = chain.invoke(
        {
            "number": number,
            "topic": topic,
            "web_results": web_results
        })  
    st.markdown("### Generated tweets")
    st.write(output["text"])
