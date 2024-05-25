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




def process_menu_text(menu_text: str):
  # Initialize ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")

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
    \n
    Under no circumstances should the JSON schema be altered or extra COMMENTS be added.\n
    It should only contain the data given to you as the menu_text.\n
    If you do not find the restaurant name, for example. Just write "Name not found" in the JSON schema.\n
    Do not forget the food items.\n
    Make sure to include ALL the menu, do not forget items.
    Under no circumstances should you translate the menu items. They should be in the same language as the menu_text.\n
    Just respond with the json, do not ask any questions.\n

    """

    # examples = """

    # YOU HAVE TO PRINT SOMETHING LIKE THIS, THIS IS JUST AN EXAMPLE. POPULATE THE ENTRIES WITH THE DATA OF THE MENU GIVEN:\n
    # ```json
    # {
    #     "menu": [
    #         {
    #             "category": "LUNCH MENU",
    #             "items": [
    #                 {
    #                     "description": "ROASTED ALMONDS",
    #                     "name": "BROCCOLI-COCONUT-CREAM SOUP (VG) A.C.",
    #                     "price": "7,80"
    #                 },
    #                 {
    #                     "description": "WHEAT TORTILLA | GUACAMOLE | BELL PEPPER | SWEET CORN | KIDNEY BEANS | PEAS | LEEK JALAPENOS | SRIRACHA | CORIANDER",
    #                     "name": "MEXICAN WRAP (VG) A.C.G",
    #                     "price": "14,90"
    #                 },
    #                 {
    #                     "description": "BIG SEASONAL SALAD | TUNA | RED ONIONS | BOILED ORGANIC EGG | OLIVES | CAPERS BALSAMIC DRESSING",
    #                     "name": "SALAD WITH TUNA A.C.G",
    #                     "price": "15,40"
    #                 },
    #                 {
    #                     "description": "ASPARAGUS | CHERRY TOMATOES | SPRING ONIONS | TRUFFLE SAUCE",
    #                     "name": "FRESH LINGUINE (V) A.C.G",
    #                     "price": "16,50"
    #                 },
    #                 {
    #                     "description": "ROASTED POTATOE DUMPLINGS | PLUM SAUCE",
    #                     "name": "GRILLED TENDER PORK LOIN A.C.G.",
    #                     "price": "17,20"
    #                 },
    #                 {
    #                     "description": "FRESH VEGETABLES | BASMATI RICE | CORIANDER",
    #                     "name": "TERIYAKI VEGETABLES (VG) I.F.M",
    #                     "price": "12,80"
    #                 },
    #                 {
    #                     "description": "APPLE STRUDEL (V) | VANILLA ICE CREAM | WHIPPED CREAM",
    #                     "name": "DESSERT",
    #                     "price": "8,50"
    #                 }
    #             ]
    #         },
    #         {
    #             "category": "EVENING- & WEEKENDMENU",
    #             "items": [
    #                 {
    #                     "description": "ROSTED CASHEWS",
    #                     "name": "SPINACH-PEAS-COCONUT SOUP (VG) A.C.",
    #                     "price": "7,80"
    #                 },
    #                 {
    #                     "description": "QUINOA | ARUGOLA | GRILLED CHEESE | CHERRY TOMATOES | SPRING ONIONS | BELL PEPPER CUCUMBER | OLIVES | EDAMAME | GOJIBERRIES | HEMP SEEDS | BALSAMIC DRESSING",
    #                     "name": "HALLOUMI BOWL (V) A.C.G",
    #                     "price": "17,20"
    #                 },
    #                 {
    #                     "description": "ASPARAGUS | SPRING ONIONS | CHERRY TOMATOES | ARUGOLA | PARMESAN",
    #                     "name": "SAFFRON RISOTTO (V) A,C,G,N,A1",
    #                     "price": "17,50"
    #                 },
    #                 {
    #                     "description": "JUICY BREADED CHICKEN BREAST | CHEDDAR CHEESE | GUACAMOLE | JALAPENOS | ICEBERG LETTUCE | TOMATOES | RED ONIONS | WHEAT BRIOCHE BUN | BURGER SAUCE",
    #                     "name": "MEXICAN CRISPY CHICKEN BURGER A.C.G",
    #                     "price": "17,80"
    #                 },
    #                 {
    #                     "description": "PEAR-WALNUT-GORGONZOLA SAUCE | BABY SPINACH | PARMESAN",
    #                     "name": "FRESH PAPPARDELLE (V) A.C.G.",
    #                     "price": "17,50"
    #                 },
    #                 {
    #                     "description": "TRADITIONAL SPINACH NOODLES | CREAMY MUSHROOM SAUCE | ROASTED ONIONS",
    #                     "name": "GRILLED PORK TENDERLOIN A.C.G.",
    #                     "price": "20,90"
    #                 },
    #                 {
    #                     "description": "FRESH VEGETABLES ASIA STYLE | BASMATI RICE | CORIANDER",
    #                     "name": "FISCH CURRY A,C,G,N,A1",
    #                     "price": "21,90"
    #                 },
    #                 {
    #                     "description": "HOMEMADE RHUBARB COMPOTE (V) | MASCARPONE CREAM",
    #                     "name": "DESSERT",
    #                     "price": "8,50"
    #                 }
    #             ]
    #         },
    #         {
    #             "category": "MITTAGSKARTE",
    #             "items": [
    #                 {
    #                     "description": "GERÖSTETE MANDELN",
    #                     "name": "BROKKOLI-KOKOS-CREMESUPPE (VG) A.C.",
    #                     "price": "7,80"
    #                 },
    #                 {
    #                     "description": "WEIZEN TORTILLA | GUACAMOLE | PAPRIKA | MAIS | KIDNEY BOHNEN | ERBSEN | LAUCH JALAPENOS | SRIRACHA | KORIANDER",
    #                     "name": "MEXICAN WRAP (VG) A.C.G",
    #                     "price": "14,90"
    #                 },
    #                 {
    #                     "description": "GROSSER FRÜHLINGSSALAT | THUNFISCH | ROTE ZWIEBELN | GEKOCHTES BIO EI OLIVEN | KAPERN | BALSAMICO DRESSING",
    #                     "name": "SALAT AL TONNO A.C.G",
    #                     "price": "15,40"
    #                 },
    #                 {
    #                     "description": "SPARGEL | KIRSCHTOMATEN | LAUCHZWIEBELN | TRÜFFELSAUCE",
    #                     "name": "FRISCHE LINGUINE (V) A.C.G",
    #                     "price": "16,50"
    #                 },
    #                 {
    #                     "description": "GEBRATENE KARTOFFELKNÖDEL | PFLAUMENSAUCE",
    #                     "name": "GEGRILLTE SCHWEINELENDE A.C.G.",
    #                     "price": "17,20"
    #                 },
    #                 {
    #                     "description": "FRISCHES GEMÜSE | BASMATIREIS | KORIANDER",
    #                     "name": "TERIYAKI GEMÜSE (VG) I.F.M",
    #                     "price": "12,80"
    #                 },
    #                 {
    #                     "description": "APFELSTRUDEL (V) | VANILLEEIS | SAHNE",
    #                     "name": "DESSERT",
    #                     "price": "8,50"
    #                 }
    #             ]
    #         }
    #     ],
    #     "restaurant_name": "Name not found"
    # }
    # ```
    # """

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
    # Invoke the chain with the menu query
    try:
      result = chain.invoke({"menu_text": menu_text, "format_instructions": format_instructions})
    except Exception as e:
      print(f"Error processing menu text: {e}")
      return None
    
    # Return the parsed JSON result
    return result

# Example usage
# For an example take the markdown in the aetna_neufahrn.json file inside the static folder 
# with open('app/static/aetna_neufahrn.json', 'r', encoding='utf-8') as file:
#     json_data = json.load(file)
# menu_text = json_data[0]['menu_text_markdown']
# result = process_menu_text(menu_text)
# print(result)
