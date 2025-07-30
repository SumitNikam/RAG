from vertexai.generative_models import GenerativeModel
from vertexai.preview import generative_models

# saftey setting for gemini model
gemini_safety_setting = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

# Function to generate the response using chat model
def code_gen(
    prompt,
    llm_model,
    model_config_params,
):
    """
    This function generates a python code using chat-bison32k llm model

    input:
    question (str): query to llm

    output: python code based on sales_df, costs_df and channel_imp_df data
    """
    # Configuration parameters for chat bison
    parameters = model_config_params

    # generates the python code
    response = llm_model.send_message(prompt, **parameters)

    return response

# Function to fine tune the response generated from chat model
def rephrase_model_response(
    llm_model,
    model_config_params,
    text_input,
    plot_image
):
    """
    This function fine tunes the text input into a human readable business language.
    Also, it can generate interpretation of the plots and charts.

    text_input (str): combined question and answer string as a text input
    from the the chat model
    plot_image : image of the plot or chart in a binary format
    """

    # configurations for gemini model
    generation_config = model_config_params

    safety_settings = gemini_safety_setting

    if plot_image:
        response = llm_model.send_message(
            [text_input, plot_image],
            generation_config=generation_config,
            safety_settings=safety_settings
            )
    else:
        response = llm_model.send_message(
            [text_input],
            generation_config=generation_config,
            safety_settings=safety_settings
            )

    # final_response = "".join(response.text for response in responses)
    final_response = response.text

    return final_response

# Function to extract entity from python code
def extract_entity(
    python_code_instr,
    code_extractor_model,
    entity_extrt_model_config
):
    """
    python_code_instr (str): string of python code and the instructions

    return: entities extracted from python code
    """
    safety_settings = gemini_safety_setting

    entities = code_extractor_model.generate_content(
      [python_code_instr],
      generation_config = entity_extrt_model_config,
      safety_settings = safety_settings,
      stream=True
    )

    objects = ""
    for entity in entities:
        objects += entity.text

    return objects

def summarise_chat(
    chat_history_prompt,
    model_name,
    generation_config
):
    summary_model = GenerativeModel(model_name)
    summary = summary_model.generate_content(
        [chat_history_prompt],
        generation_config=generation_config,
        safety_settings=gemini_safety_setting,
        stream=True
        )

    chat_summary = ""

    for response in summary:
        chat_summary += response.text

    return chat_summary
