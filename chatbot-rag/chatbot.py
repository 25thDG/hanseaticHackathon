import os
import streamlit as st
from openai import OpenAI
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings
from langchain_chroma import Chroma
import final_prompt as prompts
import stage_one

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "-")
LLM_ENDPOINT = os.environ.get("LLM_ENDPOINT", "***")
EMBEDDING_EP = os.environ.get("EMBEDDING_EP", "***")

embeddings = HuggingFaceEndpointEmbeddings(model=EMBEDDING_EP)
llm = OpenAI(base_url=LLM_ENDPOINT, api_key=OPENAI_API_KEY)
vectorstore = Chroma(embedding_function=embeddings, persist_directory="/data")

st.set_page_config(page_title="KIRA", page_icon="🏡", menu_items={})
st.header(':green[🏡 Bitte gebe die Eckdaten zu deinem Gebäude ein ...]', divider="green")

system_prompt = [{
    "role": "system",
    "content": " ".join([
        "Dein name ist KIRA und Du bist ein Berater für Gebäudesanierung.",
        "Beantworte die Fragen ausschließlich auf der Grundlage Deines Kontexts, der aus Deinem zuverlässigen Wissensspeicher abgefragt wird.",
        "Wenn Du Links, Verweise oder Quellen angibst, beziehe Dich dabei ausschließlich auf Fakten, die in Deinem Kontext zu finden sind."
    ])
}]

# Initialize session state variables
if 'Parameter1' not in st.session_state:
    st.session_state.update({
        "YEAR": None,
        "KWH": None,
        "FUEL": None,
        "INSULATION": None,
    })
if 'messages' not in st.session_state:
    st.session_state['messages'] = []
if 'contexts' not in st.session_state:
    st.session_state['contexts'] = []

colheader1,colheader2 = st.columns([4,12])
col_data1, col_data2, col_data3, col_data4 = st.columns(4)
col_data_full,col_data_full2  = st.columns([12,1])
left, middle, right = st.columns(3)


with col_data1:
     st.image("energy_prompt.jpg", caption="Sanierungsfahrplan")
with col_data2:
    st.session_state["YEAR"] = st.selectbox(
        "Baujahr",
        (
            "1900", "1988"
        ),
    )

with col_data3:
    st.session_state["KWH"] = st.selectbox(
        "Energiebedarf",
        (
            "20000", "50000"
        ),
    )
with col_data4:
    st.session_state["FUEL"] = st.selectbox(
        "Energieträger",
        (
            "Gas", "Pellets", "Oel", "Strom", "Fernwaerme"
        ),
    )
with col_data_full:
    options = ["Dach", "Kellerdecke", "Heizungsrohre"]
    st.session_state["INSULATION"] = st.pills("Gebäudeteile mit Dämmung", options, selection_mode="multi")

# Logic to hide/display button
if 'display_result' not in st.session_state:
    st.session_state.display_result = False
if 'reset' not in st.session_state:
    st.session_state.reset = False

context_msgs = ["Kontext zum Baujahr", "Kontext zur Heizung", "Kontext zur Dämmung"]

if not st.session_state.display_result:
    if middle.button("Erstelle Bericht", icon="⏱", use_container_width=True):
        st.session_state.display_result = True
        stage_one.run_stage_one(context_msgs[0] + " wird abgefragt ...",
                                vectorstore, llm, system_prompt, prompts.year_query(), prompts.year_prompt())
        stage_one.run_stage_one(context_msgs[1] + " wird abgefragt ...",
                                vectorstore, llm, system_prompt, prompts.heating_query(), prompts.heating_prompt())
        stage_one.run_stage_one(context_msgs[2] + " wird abgefragt ...",
                                vectorstore, llm, system_prompt, prompts.insulation_query(), prompts.insulation_prompt())
        stage_one.run_stage_two("Erstelle Sanierungsfahrplan ...", llm, system_prompt, prompts.final_prompt())
        st.rerun()

def btn_b_callback():
    st.session_state.display_result=False
    st.session_state.reset=False 


if st.session_state.display_result:
    # Show previous messages
    for index, entry in enumerate(st.session_state['contexts']):
        with st.chat_message('ai'):
            with st.status(context_msgs[index]):
                st.write(entry['content'])
    for entry in st.session_state['messages']:
        with st.chat_message(entry['role']):
            st.write(entry['content'])

    # Handle the user prompt and stream a response
    if prompt := st.chat_input("🦜 Ask me anything about prompt engineering ..."):
        with st.chat_message("user"):
            st.write(prompt)
            st.toast("Working")
        
        with st.chat_message("ai"):
            with st.status("Querying knowledge base"):
                retriever = vectorstore.as_retriever(search_kwargs={'k': 3})
                #last_response = st.session_state.messages[-1]['content'] if st.session_state.messages else ""
                ctx = '\n\n'.join(c.page_content for c in retriever.invoke(query))
                st.write(f"Found a context with {len(ctx)} characters.")
                st.write(ctx)
                st.write(f"Found using the query: {query}")
        
            last_messages = st.session_state.messages[-2:] if len(st.session_state.messages) > 2 else st.session_state.messages
            completion = llm.chat.completions.create(
                messages=system_prompt + [{"role": "system", "content": f"Context: {ctx[0:7500]}"}] + last_messages + [
                    {"role": "user", "content": prompt}
                ],
                model="", stream=True, max_tokens=1000
            )
            response_placeholder = st.empty()  # Placeholder for the streamed response
            response = ""
            for chunk in completion:
                if not chunk.choices[0].finish_reason:
                    delta_content = chunk.choices[0].delta.content
                    response += delta_content
                    response_placeholder.write(response)  # Update the placeholder with the streamed content
        
            st.session_state.messages.extend([
                {"role": "user", "content": prompt},
                {"role": "ai", "content": response},
            ])
     
