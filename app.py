import base64
import datetime
import io
import json
import os
from PIL import Image

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from vertexai.generative_models import Part

# from src.specific import caching_bq_data as bq_cache
from src.specific import llm_prompts
from src.specific import data_schema
from src.specific import preprocessing_data as dp
from src.specific import few_shot_training as fst
from src.specific import llm_models
from src.specific import llm_interactions
from src.specific import utils
from src.specific.read_data import read_data_gcs


def main():
    #####################################
    #   Streamlit page configuration    #
    #####################################
    # import vodafone logo
    vf_logo = Image.open("./assets/vodafone_logo.png")

    # set page configuration
    st.set_page_config(
        page_title="RO-Bot",
        page_icon=vf_logo,
        layout="wide",
    )
    st.set_option(
        'deprecation.showPyplotGlobalUse',
        False
    )

    # Avoid auto page scroll during chat session
    st.markdown("""
    <style>
        *, {
            box-sizing: inherit;
        }
        </style>""",
    unsafe_allow_html=True)


    ######################################
    #       Load parameters              #
    ######################################
    with open('./config/lab.json') as f:
        payloads = json.load(f)

    ######################################
    #   Import the required datasets     #
    ######################################
    # Google project id
    project_id = payloads['google_project']
    bucket_name = ""
    file = ""

    # Import the data
    df = read_data_gcs()
    cltv = pd.read_csv(payloads['query_params_dict']['cltv_data'])
    
    ###############################
    #      Data prep              #
    ###############################
    # Prepare year and month column
    df = dp.extract_year_month(
        input_df=df,
        date_col='accounting_rpt_month',
        date_format="%Y-%m-%d"
    )
    cltv_df = dp.extract_year_month(
        cltv,
        "MONTH_ID",
        "%d/%m/%Y"
    )

    # Extract max dates from data
    df_end_date = max(df['date'])
    
    # Create data set information for LLM context
    DF_INFO = df.dtypes
    CLTV_DF_INFO = cltv_df.dtypes

    # Create a meta data for df
    num_dict, obj_dict = data_schema.get_schema_info(df)
    df_desc = dict(list(obj_dict.items())+list(num_dict.items()))

    # Create a meta data for cltv df
    num_dict, obj_dict = data_schema.get_schema_info(cltv_df)
    cltv_df_desc = dict(list(obj_dict.items())+list(num_dict.items()))

    ##########################################
    #      Set up the context for LLM        #
    ##########################################
    # Add description to the data set schema
    DF_INFO, CLTV_DF_INFO = llm_prompts.prepare_data_schema_context(
        DF_INFO,
        CLTV_DF_INFO
    )

    # Instruction for the llm
    context = llm_prompts.prepare_code_generation_prompt(
        df_end_date,
        DF_INFO,
        CLTV_DF_INFO,
        df_desc,
        cltv_df_desc
    )

    # Business context to fine tune the answer
    business_context = llm_prompts.prepare_business_interpretation_prompt(
        DF_INFO,
        CLTV_DF_INFO,
        df_desc,
        cltv_df_desc
    )

    # Instruction text to extract plot description
    plot_desc_instruction = llm_prompts.prepare_plot_extraction_instruction()

    ######################################
    #  Few shot examples for chat-bison  #
    ######################################
    examples = fst.few_shot_examples()

    ######################################
    #           Chatbot layout           #
    ######################################
    col1, col2 = st.columns([20, 3])
    with col1:
        GRADIENT_TEXT_HTML = """
        <style>
        .gradient-text {
            background-color:LightCoral;
            font-weight: bold;
            background: -webkit-linear-gradient(left, red, orange);
            background: linear-gradient(to right, red, orange);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: inline;
            font-size: 3em;
        }
        </style>
        <div class="gradient-text">RO-Bot</div>
        """
        st.markdown(GRADIENT_TEXT_HTML, unsafe_allow_html=True)
    with col2:
        # Add vodafone logo
        st.image("./assets/vodafone_logo.png")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {
                "role": "assistant",
                "content": "**Hi, I'm RO Bot. What insights would you like me to extract?**"
            }
        ]

    # Initializing the chat session timestamp
    if "timestamp" not in st.session_state:
        st.session_state["timestamp"] = [str(datetime.datetime.now())]

    # Initialize the session state to store code history
    if 'code_gen_hist' not in st.session_state:
        st.session_state['code_gen_hist'] = []

    # Initialize the session state to store consumed tokens
    if 'totaltokens' not in st.session_state:
        st.session_state['totaltokens'] = 0

    # Chat session time to store a chat history
    chat_session_time = st.session_state["timestamp"]

    # Clear conversation buttion
    restart_chat = st.sidebar.button("➕  New Chat")
    if restart_chat:
        st.sidebar.write("Restarting the chat session")
        del st.session_state.messages
        del st.session_state.timestamp
        # st.session_state.key = value + 1
        st.rerun()

    # Call the models for the chat session
    code_gen_llm = llm_models.import_code_gen_model(
        session_state_time=chat_session_time,
        model_name=payloads["llm_models"]["code_generation_llm"],
        context_to_llm=context,
        train_examples=examples
    )

    text_gen_llm = llm_models.import_text_gen_model(
        model_name=payloads["llm_models"]["text_generation_llm"],
        session_state_time=chat_session_time
    )

    entity_extract_llm = llm_models.import_entity_extract_llm(
        model_name=payloads["llm_models"]["code_entity_extract_llm"],
        session_state_time=chat_session_time
    )

    # Display the previous chats
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).markdown(
            msg["content"],
            unsafe_allow_html=True
        )

    # Execute previous python code (to tackle streamlit page refresh)
    # To store the executions in memory
    if len(st.session_state.code_gen_hist) > 0:
        for prev_py_code in st.session_state.code_gen_hist:
            print(prev_py_code)
            try:
                exec(prev_py_code)
            except Exception as e:
                prev_py_code = ""
                exec(prev_py_code)

    # User query input and its display
    if input_question := st.chat_input(placeholder="Please enter your query."):
        # Question to display on the UI
        query = "**"+input_question+"**"
        st.session_state.messages.append({"role": "user", "content": query})
        st.chat_message("user").markdown(query, unsafe_allow_html=True)

        # Chat-bison model configuration
        cb_config = payloads["model_config_parameters"]["code_gen_model"]

        # Try catch to handle any error with the model output generation
        try:
            # Generate the code
            model_response = llm_interactions.code_gen(
                prompt=input_question,
                llm_model=code_gen_llm,
                model_config_params=cb_config
            )
            
            # Extract the code generated from model_response
            py_code = model_response.text
            
            # Clean the generated code text for execution
            code_output = py_code.split('```')[1].split('python')[1] if (
                ('python' in py_code) and ('#' in py_code)
            ) else py_code            

            # Chat-bison model configuration
            gemini_config = payloads["model_config_parameters"]["text_gen_model"]

            # Check if the generated code snippet is a valid python snippet
            if utils.is_valid_python(code_output):
                # Store the python code in session state
                if code_output not in st.session_state.code_gen_hist:
                    st.session_state.code_gen_hist.append(code_output)

                # Execute the code output
                exec(code_output)

                # If image not generated in code (text output)
                if code_output.find('plot') == -1:
                    with utils.stdoutIO() as s:
                        exec(code_output)
                    exe_output = s.getvalue()

                    # Rephrase the output text
                    tuned_answer = llm_interactions.rephrase_model_response(
                        llm_model=text_gen_llm,
                        model_config_params=gemini_config,
                        text_input=business_context +
                        f"""User input: {input_question}, 
                        python output: {exe_output}""",
                        plot_image=None
                    )
                else:
                    # Diplay the plot on UI
                    buf = io.BytesIO()
                    plt.savefig(buf, format="png")
                    plot_image = Image.open(buf)
                    resized_plot_image = plot_image.resize((400, 350))
                    st.image(resized_plot_image)

                    # If the code consists an image
                    py_code_instr = f"""instructions: {plot_desc_instruction}\npython code: {code_output}"""

                    # Gemini entity extraction model configuration
                    ent_config = payloads[
                        "model_config_parameters"
                    ]["entity_extract_model"]
                    
                    # Extract object names used to generate the plot
                    plot_object_name = llm_interactions.extract_entity(
                        python_code_instr=py_code_instr,
                        code_extractor_model=entity_extract_llm,
                        entity_extrt_model_config=ent_config
                    )

                    # Extract dataset objects used to generate the plot
                    plot_object = eval(
                        plot_object_name.split('plotted_object: ')[1]
                    )
                    
                    # Context to interpret the plots
                    context_text = business_context + \
                        f"""\nTable: {plot_object},\nQuestion: {input_question}"""

                    # Rephrase the plot interpretation
                    tuned_answer = llm_interactions.rephrase_model_response(
                        llm_model=text_gen_llm,
                        model_config_params=payloads[
                            "model_config_parameters"
                        ]["plot_desc_model"],
                        text_input=context_text,
                        plot_image=None)
            else:
                # Allocate the out-of-context response
                tuned_answer = model_response.text
        except Exception as e:
            tuned_answer = """Please rephrase the question,
            to get the desired output for data.
            1. Maybe the question is not clear
            2. The data is unavailable to generate answer for the given question
            3. The LLM model has reached the token limit and
            the chat has reset
            """

        # Store the answer in session state and display it on UI
        with st.chat_message("assistant"):
            st.markdown(tuned_answer)
            # The messages to be appended to the chat history
            st.session_state.messages.append({
                "role": "assistant",
                "content": tuned_answer
            })

        ######################################
        #   Summarise the chat history       #
        ######################################
        exception_answer = """Please rephrase the question,
        to get the desired output for data.
        1. Maybe the question is not clear
        2. The data is unavailable to generate answer for the given question
        3. The LLM model has reached the token limit and
        the chat has reset
        """

        try:
            # Total tokens consumed by chat-bison
            chat_resp_list = model_response.raw_prediction_response.metadata[
                'tokenMetadata'
                ].values()
            # Calculate total tokens consumed (input+output)
            consumed_tokens = sum(
                [
                    item['totalTokens'] for item in chat_resp_list
                ]
            )
            # Save consumed tokens to session state
            st.session_state['totaltokens'] = consumed_tokens
        except Exception as e:
            # Allocate the cosumed tokens stored in a session state
            consumed_tokens = st.session_state['totaltokens']

        # Maximum threshold allowed to consume
        max_consumed_tokens = payloads["max_consumed_token_limit"]

        # Check if chat's token limit is reached
        if consumed_tokens >= max_consumed_tokens or tuned_answer == exception_answer:
            # Clear the cached resource of the chat-bison model
            llm_models.import_code_gen_model.clear()

            # Extract chat history
            user_inputs = [
                msg.content for msg in code_gen_llm.message_history if msg.author == 'user'
            ]

            final_outputs = [
                msg.parts[0].text for msg in text_gen_llm.history if msg.role == 'model'
            ]

            summary_instr = """Above is a conversations between a user and a bot.
            Summarise the given conversation.
            Do not include information about the bot interface."""

            chat_summary_prompt = f"""user_inputs: {user_inputs},
            final_outputs: {final_outputs}, instructions: {summary_instr}
            """

            # Summarise chat-history
            previous_chat_summary = llm_interactions.summarise_chat(
                chat_summary_prompt,
                model_name=payloads[
                    "llm_models"
                ]["text_generation_llm"],
                generation_config=payloads[
                    "model_config_parameters"
                ]["chat_summary_model"]
            )

            # Chat-bison restart
            code_gen_llm = llm_models.import_code_gen_model(
                session_state_time=chat_session_time,
                model_name=payloads["llm_models"]["code_generation_llm"],
                context_to_llm=context + previous_chat_summary,
                train_examples=examples
            )

if __name__ == "__main__":
    main()
