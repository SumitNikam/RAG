import streamlit as st

from vertexai.language_models import ChatModel
from vertexai.generative_models import GenerativeModel
from vertexai.preview import generative_models

# Function to store the chat history and model in cache
@st.cache_resource
def import_code_gen_model(
    session_state_time,
    model_name,
    context_to_llm,
    train_examples
):
    """
    Function to trigger and load the code generation LLM for every new session.
    It helps to hold the chat history and context during the chat session.
    Avoids chat restart for every question asked on a streamlit UI.
    
    session_state_time : time stamp of the session
    context_to_llm : Context to generate the code
    train_examples : Few shot training examples to train the llm

    return: Refreshed code gen llm (chat-bison) model
    """
    # Session time stamp value to retain the chat in streamlit cache
    session_state_time = session_state_time

    # import chat bison model to generate the python code
    chat_model = ChatModel.from_pretrained(model_name)

    # Start the chat model
    code_gen_llm = chat_model.start_chat(
        context=context_to_llm, examples = train_examples
    )

    return code_gen_llm

@st.cache_resource
def import_text_gen_model(
    model_name,
    session_state_time
):
    """
    Function to trigger and load the text generation LLM for every new session.
    It helps to hold the chat history and context during the chat session.
    Avoids chat restart for every question asked on a streamlit UI.
    
    session_state_time : time stamp of the session

    return: Refreshed text generation llm (gemini) model
    """
    # call the gemini model
    gemini_model = GenerativeModel(model_name)

    # start text gen LLM model
    text_gen_llm = gemini_model.start_chat()

    return text_gen_llm

# @st.cache_resource
def import_entity_extract_llm(
    model_name,
    session_state_time
):
    """
    Function to trigger and load the llm to extract the entities from the python code.
    Helps in describing the plots.
    It helps to hold the chat history and context during the chat session.
    Avoids chat restart for every question asked on a streamlit UI.

    session_state_time : time stamp of the session

    return: Refreshed text generation llm (gemini) model
    """
    # call the gemini model
    gemini_extract_model = GenerativeModel(model_name)

    return gemini_extract_model
