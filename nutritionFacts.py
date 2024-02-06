# https://github.com/afogarty85/fooddata_central/blob/main/main.py

import requests
import json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import os
import getch
import time

# set API details
api_key = 'M0vNnETsfDcZHzDH1c4XrmNzmODhVFozxZVf0WX3'
USDA_URL = 'https://api.nal.usda.gov/fdc/v1/'
requested_url = 'https://api.nal.usda.gov/fdc/v1/search?api_key='
headers = {'Content-Type': 'application/json'}

# Search each entry in top_products_by_aisle by USDA database through API
def nutritionFacts_getFDCID(food_to_search, api_key=api_key):
    
    '''
    This function uses USDA's REST access API to retrieve
    information from FoodData Central (https://fdc.nal.usda.gov/).
    This function returns the FDCID for the item searched by attempting to
    retrieve the closest match by using Levenshtein distance calculations.
    An API key is required for use and can be acquired for free, here:
    https://fdc.nal.usda.gov/api-key-signup.html

    Parameters
    ----------
    food_to_search : list
        A list of strings of foods
    branded : flag
        Whether or not we want to search branded food

    Returns
    -------
    fdcIDs : list
        The most likely FDCIDs for the food items searched.
    '''
    # initiate pull
    fdcIDs = []  # container for results
    # for each item in the list
    for item in food_to_search:

        # Exceptions
        if item.lower() == "water":
            return [2346283]
        if item.lower() == "banana":
            return [1105073]

        # pull item in list
        data = {"generalSearchInput": item}
        # convert to json format
        data_str = json.dumps(data).encode("utf-8")
        # commit an API request for the item
        response = requests.post(requested_url + api_key, headers=headers, data=data_str)
        # parse the generated data
        parsed = json.loads(response.content)

        # index = -1
        # for idx,i in enumerate(parsed['foods']):       
        #     if i['dataType'] == "Survey (FNDDS)":
        #         index = idx
        #         break

        # set up metrics for eventual item selection
        best_idx = None
        best_ratio = 0

        # for each item in the generated data
        # foundation_index = -1
        # survey_index = -1
        for idx, i in enumerate(parsed['foods']):
            try:
                # if i['dataType'] == "Foundation" and foundation_index == -1:
                #     foundation_index = idx

                # if i['dataType'] == "Survey (FNDDS)" and survey_index == -1:
                #     survey_index = idx   

                curr_ratio = fuzz.token_set_ratio(item, i['description'])
                if curr_ratio > best_ratio:
                    best_idx = idx
                    best_ratio = curr_ratio

                # if survey_index != -1:
                #     best_idx = survey_index

                # if foundation_index != -1:
                #     best_idx = foundation_index
            except:
                pass

        # for i in parsed['foods'][best_idx]:
        #     print(parsed['foods'][best_idx][i])
        #     # print(i)
        # time.sleep(1000)

        # save the best performing item as the most likely match from the db
        fdcIDs.append(parsed['foods'][best_idx]['fdcId'])
    return fdcIDs


def nutritionFacts_getNutrition(fdcIDs, api_key=api_key):
    ''' This function collects nutritional data for each FDCID.
    It does so by making calls to the USDA database,
    FoodData Central (https://fdc.nal.usda.gov/), and it
    then retrieves the returned JSON data for the relevant nutritional data.

    Parameters
    ----------
    fdcIDs : list
        A list of FDCIDs that we want nutrition data for
    api_key : string
        Our API key

    Returns
    -------
    nutrient_df : pandas data frame
        A data frame containing our results
    '''

    # Set container storage and ordering
    nutrient_container = []
    nutrient_list = [
                        'name', 
                        'kcal', 
                        'grams', 
                        'total_fat', 
                        'sat_fat', 
                        'cholesterol', 
                        'sodium',
                        'carbs', 
                        'fiber',
                        'sugars', 
                        'protein', 
                        'fdcID'
                    ]
    nutrient_container.append(nutrient_list)

    # Loop over each FDCID; commit a API request for each
    l = len(fdcIDs)
    barLength = 50
    count = 1
    nutrient_df = pd.DataFrame()
    for i in fdcIDs:
        fdcId = str(i)
        requested_url = USDA_URL + fdcId + '?api_key=' + api_key
        response = requests.get(requested_url, headers=headers)
        parsed = json.loads(response.content)
        name = parsed['description'][0:40]
        kcal = 0
        grams = 100
        total_fat = 0
        sat_fat = 0
        cholesterol = 0
        sodium = 0
        carbs = 0
        fiber = 0
        sugars = 0
        protein = 0
        fdc_id = i

        try:
            name = name + " " + parsed['brandOwner']
            name = name + " " + parsed['brandName']
        except:
            name = name

        nameLength = 40
        s = 'Complete\tFinding nutrition information for ' + name[0:nameLength] + '...' + ''.ljust(nameLength)
        nutritionFacts_progressBar(count, l, prefix = 'Progress:', suffix = s, length = barLength)

        # Loop over dictionary length to look for desired data
        for j in range(0, len(parsed)):
            try:            
                if parsed['foodNutrients'][j]['nutrient']['id'] == 1008:
                    kcal = parsed['foodNutrients'][j]['amount']

                # calName = parsed['foodNutrients'][j]['nutrient']['name']
                # if (calName == "Energy" or calName == "Energy (Atwater Specific Factors)") and kcal == 0:
                #     kcal = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1004:
                    total_fat = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1258:
                    sat_fat = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1253:
                    cholesterol = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1093:
                    sodium = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1005:
                    carbs = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1079:
                    fiber = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 2000:
                    sugars = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1003:
                    protein = parsed['foodNutrients'][j]['amount']

            # In case of nutrition not found; continue anyways
            except:
                    pass        

        # append data
        nutrient_container.append( [
                                    name, 
                                    kcal, 
                                    grams, 
                                    total_fat, 
                                    sat_fat, 
                                    cholesterol,
                                    sodium, 
                                    carbs, 
                                    fiber, 
                                    sugars, 
                                    protein, 
                                    fdc_id
                                   ]
                                )

        # turn nutrient_list into df for preprocessing
        nutrient_df = pd.DataFrame  (data=nutrient_container[1::],
                                     columns=   [
                                                    'name', 
                                                    'kcal', 
                                                    'grams', 
                                                    'total_fat [g]', 
                                                    'sat_fat [g]',
                                                    'cholesterol [mg]', 
                                                    'sodium [mg]', 
                                                    'carbs [g]',
                                                    'fiber [g]', 
                                                    'sugars [g]', 
                                                    'protein [g]',
                                                    'fdcID'
                                                ]
                                    )

        count = count+1

    return nutrient_df


# Preprocess the nutrient data
def nutritionFacts_nutrientPreprocessing(dataframe, amount):
    ''' This function preprocesses the nutrient data by converting each
    nutrient to amount[i] g of each item

    Parameters
    ----------
    dataframe : pandas data frame
        A data frame containing un-scaled nutritional data
    amount : list of ints
        A list of int containing gram amount of every ingredient

    Returns
    -------
    dataframe : pandas data frame
        A data frame containing scaled nutritional data
    '''

    # Convert nutrients to amount of grams specified
    for i in range(0,len(amount)):
        for j in dataframe.columns:
            if(j == 'fdcID' or j == 'name'): continue
            dataframe.loc[i, (j, i)] = dataframe[j][i] * (amount[i]/100)

        del dataframe[dataframe.columns[-1]]

    return dataframe


# Print iterations progress
def nutritionFacts_progressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()


# info line printing for recipes_main.py
def nutritionFacts_infoPrint(name="", servings="", foods={}, comments=[], productNames=[]):
    os.system("clear")
    print("RECIPE CREATOR")
    
    print("\nEnter the name of your recipe:", name, end="")
    if(name == ""): return
    print()

    print("\nEnter the number of servings:", servings, end="")
    if(servings == ""): return
    print()

    print('\nEnter the ingredients of your recipe')
    print('Format: <name>,<grams>,<optional comment>.  Enter nothing to finish')
    if(foods == {}): return
    assert(len(foods) == len(comments))
    i = 1
    for x in foods:
        if(comments[i-1] != ""): print('\t', i, ' : ', x, ',', foods[x], ',', comments[i-1][0:40], " -- ", productNames[i-1], sep='')
        else: print('\t', i, ' : ', x, ',', foods[x], " -- ", productNames[i-1], sep='')
        i = i+1


# user enters the name of their recipe
# returns the name of the recipe
def nutritionFacts_enterName():
    nutritionFacts_infoPrint()
    name = input()

    if(len(name) == 0 or name.isspace()): name = nutritionFacts_enterName()

    return name


# user enters the number of servings of their recipe
# returns the entered number of servings of the recipe
def nutritionFacts_enterServings(name):
    nutritionFacts_infoPrint(name)

    try:
        servings = int(input())
    except:
        servings = nutritionFacts_enterServings(name)

    return servings


# user enters the ingredients of their recipe
# checks if food is valid, or if amount is an integer
# returns the list of foods, list of their fdcIDs, and optional comments about each item
def nutritionFacts_enterFood(name,servings):
    nutritionFacts_infoPrint(name,servings)

    user = "temp"
    food = {}
    ids = {}
    comments = {}
    productNames = []
    
    count = 1
    while(len(user) != 0 and user.isspace() == False):
        print("\t", count, " : ", end="", sep='')
        count = count+1
        user = input()

        arr = user.split(',')
        comment = ""
        if(len(arr) != 2 and len(arr) != 3): 
            count = count-1
            nutritionFacts_infoPrint(name,servings,food,list(comments.values()),productNames)
            continue
        if(len(arr) == 3): comment = arr[2]
        
        enteredName = arr[0]
        grams = arr[1]
        isLst = []
        try:
            grams = int(grams)
            foodList = [enteredName]
            idLst = nutritionFacts_getFDCID(foodList)
            id = int(idLst[0])
        except:
            count = count-1
            nutritionFacts_infoPrint(name,servings,food,list(comments.values()),productNames)
            continue

        food[enteredName] = grams
        ids[enteredName] = id
        comments[enteredName] = comment

        fdcId = str(idLst[0])
        requested_url = USDA_URL + fdcId + '?api_key=' + api_key
        response = requests.get(requested_url, headers=headers)
        df = nutritionFacts_getNutrition(fdcIDs=isLst, api_key=api_key)
        parsed = json.loads(response.content)
        productName = parsed['description']
        try:
            productName = productName + " " + parsed['brandOwner']
            productName = productName + " " + parsed['brandName']
        except:
            productName = productName
        
        productNames.append(productName)

        nutritionFacts_infoPrint(name,servings,food,list(comments.values()),productNames)

    if(len(food) == 0): food = nutritionFacts_enterFood(name,servings)
    return food, ids.values(),list(comments.values()), productNames


# Gives user option to return to main menu or stay
def nutritionFacts_end():
    print("\nEnter \'Y\' to to stay on this screen, or anything else to return")
    exit = getch.getch()

    if exit == "Y" or exit == "y":
        return nutritionFacts_main()
    else:
        return


def nutritionFacts_main():
    name = nutritionFacts_enterName()
    servings = nutritionFacts_enterServings(name)
    food,ids,comments,productName = nutritionFacts_enterFood(name,servings)
    nutritionFacts_infoPrint(name,servings,food,comments,productName)

    print("\nNutritional information for 1 serving of", name.upper(), "\n")

    food_list = list(food.keys())
    amount = list(food.values())
    for i in range(0,len(amount)): amount[i] = amount[i] / servings
    
    fdcIDs = ids
    nutrient_df = nutritionFacts_getNutrition(fdcIDs=fdcIDs, api_key=api_key)
    nutrient_df = nutritionFacts_nutrientPreprocessing(nutrient_df, amount)

    print("FOR EACH INGREDIENT")
    print(nutrient_df.to_string(index=False))
    print('\nTOTALS')
    print(nutrient_df.drop(['grams', 'fdcID', 'name'], axis=1).sum().to_string())

    nutritionFacts_end()

if __name__ == "__main__":
    nutritionFacts_main()