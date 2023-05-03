# https://github.com/afogarty85/fooddata_central/blob/main/main.py

import requests
import json
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
import os

from recipes_main import *
from loadingBar import*

api_key = 'M0vNnETsfDcZHzDH1c4XrmNzmODhVFozxZVf0WX3'

# Search each entry in top_products_by_aisle by USDA database through API
def fdcID_retrieval(food_to_search, branded=True, api_key=api_key):
    
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

    # Progress Bar
    # l = len(food_to_search)+1
    # barLength = 50
    # printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete\tLocating fdcIDs...', length = barLength)

    # set API details
    requested_url = 'https://api.nal.usda.gov/fdc/v1/search?api_key='
    headers = {'Content-Type': 'application/json'}
    # onitiate pull
    fdcIDs = []  # container for results
    # for each item in the list
    for item in food_to_search:
        # pull item in list
        data = {"generalSearchInput": item}
        # convert to json format
        data_str = json.dumps(data).encode("utf-8")
        # commit an API request for the item
        response = requests.post(requested_url + api_key, headers=headers, data=data_str)
        # parse the generated data
        parsed = json.loads(response.content)
        # set up metrics for eventual item selection
        best_idx = None
        best_ratio = 0
        # for each item in the generated data
        for idx, i in enumerate(parsed['foods']):
            # if we are looking for a branded item
            if branded is True:
                # try condition for non-branded food
                try:
                    # use a flexibile levenshtein distance to compare
                    curr_ratio = fuzz.token_set_ratio(item, i['brandOwner'] + ' ' + i['description'])
                    # if we find better matches for what we are looking for
                    if curr_ratio > best_ratio:
                        # record them
                        best_idx = idx
                        best_ratio = curr_ratio
                except:
                    # in case of error/no result, pass
                    pass
            # if we are not looking for a branded item
            if branded is False:
                # do the same as above
                try:
                    curr_ratio = fuzz.token_set_ratio(item, i['description'])
                    if curr_ratio > best_ratio:
                        best_idx = idx
                        best_ratio = curr_ratio
                except:
                    pass
        # save the best performing item as the most likely match from the db
        fdcIDs.append(parsed['foods'][best_idx]['fdcId'])
    return fdcIDs


def nutrition_retrieval(fdcIDs, api_key=api_key):
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
                        # 'added_sugar', 
                        'protein', 
                        'fdcID'
                    ]
    nutrient_container.append(nutrient_list)

    # set API details
    USDA_URL = 'https://api.nal.usda.gov/fdc/v1/'
    headers = {'Content-Type': 'application/json'}

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
        # added_sugar = 0
        protein = 0
        fdc_id = i

        nameLength = 40
        s = 'Complete\tFinding nutrition information for ' + name[0:nameLength] + '...' + ''.ljust(nameLength)
        printProgressBar(count, l, prefix = 'Progress:', suffix = s, length = barLength)

        # file = open("test.txt", "w")
        # file.write(str(parsed))
        # file.close

        # print('---------')
        # for j in range(0, len(parsed)):
        #     print(parsed['foodNutrients'][j]['nutrient']['id'], " ", parsed['foodNutrients'][j]['amount'])
        # print('---------')

        # Loop over dictionary length to look for desired data
        for j in range(0, len(parsed)):
            try:
                # print(parsed['foodNutrients'][j]['nutrient']['id'], " ", parsed['foodNutrients'][j]['amount'])
                
                if parsed['foodNutrients'][j]['nutrient']['id'] == 1008:
                    kcal = parsed['foodNutrients'][j]['amount']

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

                # if parsed['foodNutrients'][j]['nutrient']['id'] == 1167:
                #     added_sugar = parsed['foodNutrients'][j]['amount']

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
                                    # added_sugar, 
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
                                                    # 'added sugar [g]', 
                                                    'protein [g]',
                                                    'fdcID'
                                                ]
                                    )

        count = count+1

    # printProgressBar(count, l, prefix = 'Progress:', suffix = 'Complete', length = barLength)
    # print()
    return nutrient_df





# Preprocess the nutrient data
def nutrient_preprocessing(dataframe, amount):
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

def fc_main(name, foods, servings, ids):
    print("\nNutritional information for 1 serving of", name.upper(), "\n")

    food_list = list(foods.keys())
    amount = list(foods.values())
    for i in range(0,len(amount)): amount[i] = amount[i] / servings
    
    # fdcIDs = fdcID_retrieval(food_list)
    fdcIDs = ids
    nutrient_df = nutrition_retrieval(fdcIDs=fdcIDs, api_key=api_key)
    nutrient_df = nutrient_preprocessing(nutrient_df, amount)

    print("FOR EACH INGREDIENT")
    print(nutrient_df.to_string(index=False))
    print('\nTOTALS')
    print(nutrient_df.drop(['grams', 'fdcID', 'name'], axis=1).sum().to_string())


if __name__ == "__main__" :
    fc_main()