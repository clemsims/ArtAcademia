# utils_prompt.py

import os
import random
import re
import json


import streamlit as st

from groq import Groq

from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel

from langchain_groq import ChatGroq


def clean_json(llm_output):
    # Remove any extraneous characters before the first { and after the last }
    start_index = llm_output.find('{')
    end_index = llm_output.rfind('}') + 1
    json_like_str = llm_output[start_index:end_index]
    
    # Remove any invalid characters (non-printable ASCII characters)
    json_like_str = re.sub(r'[^\x20-\x7E]+', '', json_like_str)

    # Correct any common JSON issues
    json_like_str = json_like_str.replace('\\"', '"')  # Fix improperly escaped quotes
    json_like_str = re.sub(r',\s*}', '}', json_like_str)  # Remove trailing commas before closing brace
    json_like_str = re.sub(r',\s*]', ']', json_like_str)  # Remove trailing commas before closing bracket
    
    # Validate and load the JSON
    try:
        data = json.loads(json_like_str)
    except json.JSONDecodeError as e:
        print("-------failed json----------",json_like_str)
        raise ValueError(f"Failed to parse JSON: {e}")
    
    return json.dumps(data)

def parse_json(json_string):
    # split to get only up to the closing bracket
    new_json_string = json_string.split("}")[0] + "}"
    # find the first {
    start_index = new_json_string.find('{')
    # find the last }
    end_index = new_json_string.rfind('}') + 1
    # get the json string
    json_like_str = new_json_string[start_index:end_index]
    return json_like_str