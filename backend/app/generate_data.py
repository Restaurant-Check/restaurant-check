import os
import json
from random import randint, choice
from pydantic import BaseModel
from typing import List
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage  # Import AIMessage to handle the response

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
{details}
Format it into the following JSON schema:
{format_instructions}
GIVE THE ITEMS PROPER FOOD NAMES AND NOT ITEM 1, ITEM 2, ETC.
DO NOT NAME MULTIPLE ITEMS IN THE SAME CATEGORY THE SAME NAME.
DO NOT RESTRICT YOURSELF TO A SPECIFIC CUISINE; BE CREATIVE.
Also choose a creative restaurant name.
"""

prompt = PromptTemplate(
    template=menu_query_template,
    input_variables=["details", "format_instructions"],
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

def generate_random_menu():
    print("Generating random menu...")
    categories = ["Appetizers", "Main Courses", "Desserts", "Beverages"]
    selected_categories = [categories[i] for i in range(randint(2, len(categories)))]
    menu = []

    # Choose a specific cuisine from the provided list
    cuisines = [
        "Italian", "Mexican", "Japanese", "Chinese", "Indian", "Thai", "French", "Spanish", "Greek", "Lebanese",
        "Korean", "Vietnamese", "Moroccan", "Turkish", "Brazilian", "Peruvian", "Ethiopian", "Indonesian", "Malaysian",
        "Russian", "German", "British", "American (Southern)", "Cajun", "Caribbean", "Argentine", "Chilean", "Australian",
        "Swedish", "Egyptian", "Israeli", "Irish", "Portuguese", "South African", "Filipino", "Hungarian", "Belgian",
        "Austrian", "Swiss", "Danish", "Norwegian", "Finnish", "Polish", "Czech", "Slovak", "Ukrainian", "Armenian",
        "Georgian", "Persian", "Iraqi", "Saudi Arabian", "Kuwaiti", "Emirati", "Omani", "Bahraini", "Qatari", "Jordanian",
        "Syrian", "Iraqi", "Tunisian", "Algerian", "Libyan", "Sudanese", "Kenyan", "Nigerian", "Ghanaian", "Senegalese",
        "Malian", "Malagasy", "Mozambican", "Angolan", "Zambian", "Zimbabwean", "Botswanan", "Namibian", "Mauritian",
        "Seychellois", "Maldivian", "Bangladeshi", "Sri Lankan", "Nepalese", "Bhutanese", "Tibetan", "Afghan", "Uzbek",
        "Tajik", "Kazakh", "Kyrgyz", "Turkmen", "Mongolian", "Bhutanese", "Timorese", "Papua New Guinean", "Fijian",
        "Solomon Islander", "Tuvaluan", "Tongan", "Samoan", "Marshallese"
    ]
    cuisine = choice(cuisines)

    for category in selected_categories:
        items = []
        for _ in range(randint(1, 5)):
            details = f"Category: {category}\nCuisine: {cuisine}"
            chain = prompt | model | parser
            print(f"Invoking chain for category: {category} with cuisine: {cuisine}")
            result = chain.invoke({"details": details, "format_instructions": format_instructions})
            items.append(MenuItem(**result['menu'][0]['items'][0]))
        menu.append(MenuCategory(category=category, items=items))
    restaurant_menu = RestaurantMenu(restaurant_name=f"{cuisine} Restaurant", menu=menu)
    return check_and_rename_duplicates(restaurant_menu)

def save_menu_to_json(menu, filename):
    print(f"Saving menu to JSON file: {filename}")
    os.makedirs('menu_json', exist_ok=True)
    with open(f'menu_json/{filename}', 'w', encoding='utf-8') as f:
        json.dump(menu.dict(), f, ensure_ascii=False, indent=4)

# Generate and save 5 random menus
for i in range(30):
    print(f"Generating menu {i+1}...")
    random_menu = generate_random_menu()
    save_menu_to_json(random_menu, f'menu_{i+1}.json')
    print(f"Menu {i+1} saved successfully.")
