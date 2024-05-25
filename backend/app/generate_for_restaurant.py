import os
import json
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage

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

# Initialize ChatOpenAI model
print("Initializing ChatOpenAI model...")
model = ChatOpenAI(temperature=0.8)

# Initialize JsonOutputParser with the RestaurantMenu schema
print("Initializing JsonOutputParser with the RestaurantMenu schema...")
parser = JsonOutputParser(pydantic_object=RestaurantMenu)

# Define format instructions
print("Defining format instructions...")
format_instructions = parser.get_format_instructions()

# Define the prompt template
print("Defining the prompt template...")
menu_query_template = """
Generate a restaurant menu with the following details:
Restaurant Name: {restaurant_name}
Setting: {setting}
Format it into the following JSON schema:
{format_instructions}
GIVE THE ITEMS PROPER FOOD NAMES AND NOT ITEM 1, ITEM 2, ETC.
DO NOT NAME MULTIPLE ITEMS IN THE SAME CATEGORY THE SAME NAME.
DO NOT RESTRICT YOURSELF TO A SPECIFIC CUISINE; BE CREATIVE.
"""

prompt = PromptTemplate(
    template=menu_query_template,
    input_variables=["restaurant_name", "setting", "format_instructions"],
)

def check_and_rename_duplicates(menu: RestaurantMenu) -> RestaurantMenu:
    print("Checking for duplicate item names...")
    while True:
        seen_names = set()
        duplicates_found = False
        for category in menu.menu:
            for item in category.items:
                if item.name in seen_names:
                    duplicates_found = True
                    rename_prompt_template = """
                    The item name "{original_name}" is duplicated in the menu category "{category}". 
                    Please provide a different proper food name for this item.
                    """
                    rename_prompt = PromptTemplate(
                        template=rename_prompt_template,
                        input_variables=["original_name", "category"]
                    )
                    rename_chain = rename_prompt | model
                    new_name = rename_chain.invoke({"original_name": item.name, "category": category.category})
                    if isinstance(new_name, AIMessage):
                        new_name = new_name.content  # Extract content from AIMessage
                    item.name = new_name
                seen_names.add(item.name)
        if not duplicates_found:
            break
    return menu

def generate_for_restaurant(restaurant_json):
    print("Generating menu for restaurant...")
    restaurant_name = restaurant_json['name']
    setting = f"Location: {restaurant_json['vicinity']}, Rating: {restaurant_json['rating']}, Price Level: {restaurant_json.get('price_level', 'N/A')}"
    
    details = {
        "restaurant_name": restaurant_name,
        "setting": setting,
        "format_instructions": format_instructions
    }
    
    chain = prompt | model | parser
    print(f"Invoking chain for restaurant: {restaurant_name}")
    result = chain.invoke(details)
    
    restaurant_menu = RestaurantMenu(**result)
    restaurant_json['menu'] = check_and_rename_duplicates(restaurant_menu).dict()
    return restaurant_json

