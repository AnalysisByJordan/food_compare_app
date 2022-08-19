import requests

api_key = 'OdWJF6TM0dfnoMEpY7lgQ97bHhSZYKr9dPTvqO8i'

#Pulls all data relating to a food item search
def get_foods(search_term):
    r = requests.get(
        f'https://api.nal.usda.gov/fdc/v1/foods/search?query={search_term}&pageSize=200&&api_key={api_key}'
    )
    term_dict = r.json()
    return term_dict

#Pulls the list of all foods + id's that were returned in the get_foods function
def get_food_list(food_dict):
    return [{'name': food['description'], 'id': int(food['fdcId'])} for food in food_dict['foods']]

#Gets the food name from the food id
def get_food_name(food_dict, id):
    for food in food_dict['foods']:
        try:
            if food['fdcId'] == int(id):
                name = food['description']
        except:
            return "None"
    return name

#Gets the nutrients needed to display for a selected food id
def get_food_nutrients(food_dict, id):
    key_nutrients= ['Sodium, Na', 'Vitamin C, total ascorbic acid', 'Cholesterol']
    nutrient_profile = {}
    for food in food_dict['foods']:
        if food['fdcId'] == int(id):
            for nutrient in food['foodNutrients']:
                if nutrient['nutrientName'] in key_nutrients:
                    nutrient_profile[nutrient['nutrientName']] = {'value': nutrient['value'], 'unitName': nutrient['unitName']}
    return nutrient_profile