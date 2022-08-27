import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
datatype = 'Survey (FNDDS)'

#Pulls all data relating to a food item search
def get_foods(search_term):
    r = requests.get(
        f'https://api.nal.usda.gov/fdc/v1/foods/search?query={search_term}&dataType={datatype}&requireAllWords=true&pageSize=211&api_key={api_key}'
    )
    foods_dict = r.json()
    return foods_dict['foods']

#Pulls the list of all foods + id's that were returned in the get_foods function
def get_food_list(food_dict):
    foods_with_brand = []
    for food in food_dict:
        if food['additionalDescriptions'] is not "":
            foods_with_brand.append({'name': food['description'], 'description': ' | ' + food['additionalDescriptions'].split(';')[0], 'id': food['fdcId']})
        else:
            foods_with_brand.append({'name': food['description'], 'description': '', 'id': food['fdcId']})
    return foods_with_brand #[{'name': food['description'], 'id': int(food['fdcId'])} for food in food_dict]

#Gets the food name from the food id
def get_food_name(food_dict, id):
    for food in food_dict:
        try:
            if food['fdcId'] == int(id):
                name = food['description']
        except:
            return "None"
    return name

#Gets the nutrients needed to display for a selected food id
def get_food_nutrients(food_dict, id):
    key_nutrients= [{'name': 'Energy', 'dv': 1}, {'name': 'Protein', 'dv': 51},{'name': 'Total lipid (fat)', 'dv': 78}, {'name': 'Fiber, total dietary', 'dv': 28}, 
    {'name': 'Carbohydrate, by difference', 'dv': 275}, {'name': 'Sugars, total including NLEA', 'dv': 1}, {'name': 'Cholesterol', 'dv': 311},
    {'name': 'Fatty acids, total saturated', 'dv': 21}, {'name': 'Fatty acids, total trans', 'dv': 1}, {'name': 'Sodium, Na', 'dv': 2311}, {'name': 'Vitamin C, total ascorbic acid', 'dv': 1}, 
    {'name': 'Vitamin A, RAE', 'dv': 1}, {'name':'Vitamin D (D2 + D3)', 'dv': 1}, {'name':'Vitamin E (alpha-tocopherol)', 'dv': 1}, {'name':'Calcium, Ca', 'dv': 1}, {'name':'Iron, Fe', 'dv': 1}, 
    {'name':'Potassium, K', 'dv': 1}, {'name':'Folate, total', 'dv': 1}]
    nutrient_profile = {}
    for food in food_dict:
        if food['fdcId'] == int(id):
            nutrient_profile['foodCategory'] = food['foodCategory']
            for nutrient in key_nutrients:
                nutrient_profile[nutrient['name']] = {'value': 0, 'unitName': 'g', 'percentage': 1}    
                for nutr in food['foodNutrients']:
                    if nutr['nutrientName'] == nutrient['name']:
                        nutrient_profile[nutrient['name']] = {'value': nutr['value'], 'unitName': nutr['unitName'].lower(), 'percentage': int((nutr['value'] / nutrient['dv'])*100)}           
            nutrient_profile['calories from fat'] =  int(nutrient_profile['Total lipid (fat)']['value'] * 9)
    return nutrient_profile