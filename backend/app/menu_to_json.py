import os
import getpass

# Set OpenAI API key
# os.environ['OPENAI_API_KEY'] = getpass.getpass()

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import List
from config import Config
import json


# Initialize ChatOpenAI model
model = ChatOpenAI()

# Define Pydantic models for JSON schema
class MenuItem(BaseModel):
    name: str
    description: str
    price: str

class MenuCategory(BaseModel):
    category: str
    items: List[MenuItem]

class RestaurantMenu(BaseModel):
    restaurant_name: str
    menu: List[MenuCategory]

# Define the menu query prompt
menu_query = """
Take the following restaurant menu in consideration and extract the relevant information:\n
{menu_text}
\n
Format it into the following JSON schema:\n
{format_instructions}
"""

# Initialize JsonOutputParser with the RestaurantMenu schema
parser = JsonOutputParser(pydantic_object=RestaurantMenu)

# Define format instructions
format_instructions = parser.get_format_instructions()

# Define the prompt template
prompt = PromptTemplate(
  template=menu_query,
  input_variables=["menu_text", "format_instructions"],
)

# Combine prompt, model, and parser into a chain
chain = prompt | model | parser


def process_menu_text(menu_text: str):
    # Invoke the chain with the menu query
    result = chain.invoke({"menu_text": menu_text, "format_instructions": format_instructions})
    
    # Return the parsed JSON result
    return result

# Example usage
# For an example take the markdown in the aetna_neufahrn.json file inside the static folder 
with open('app/static/aetna_neufahrn.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)
menu_text = json_data[0]['menu_text_markdown']
result = process_menu_text(menu_text)
print(result)
