import os
from fooddata_central import *

api_key = 'M0vNnETsfDcZHzDH1c4XrmNzmODhVFozxZVf0WX3'
USDA_URL = 'https://api.nal.usda.gov/fdc/v1/'
headers = {'Content-Type': 'application/json'}

# info line printing for recipes_main.py
def recipes_infoPrint(name="", servings="", foods={}, comments=[], productName=""):
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
        if(comments[i-1] != ""): print('\t', i, ' : ', x, ',', foods[x], ',', comments[i-1], "\t\t", productName, sep='')
        else: print('\t', i, ' : ', x, ',', foods[x], "\t\t\t", productName, sep='')
        i = i+1

    # TODO: have it print the full name of the item so the user can confirm it is correct
    # name as in the name retrived from the fdcID, not the string name the user entered
    # example "banana" comes in as banana peanut butter, so BPB should be printed, because it corresponds to the found fdcID
    # this would be so the user can check if the item they entered was correctly found

# user enters the name of their recipe
# returns the name of the recipe
def recipes_enterName():
    recipes_infoPrint()
    name = input()

    if(len(name) == 0 or name.isspace()): name = recipes_enterName()

    return name

# user enters the number of servings of their recipe
# returns the entered number of servings of the recipe
def recipes_enterServings(name):
    recipes_infoPrint(name)

    try:
        servings = int(input())
    except:
        servings = recipes_enterServings(name)

    return servings

# user enters the ingredients of their recipe
# checks if food is valid, or if amount is an integer
# returns the list of foods, list of their fdcIDs, and optional comments about each item
def recipes_enterFood(name,servings):
    recipes_infoPrint(name,servings)

    user = "temp"
    food = {}
    ids = {}
    comments = {}
    productName = ""
    
    count = 1
    while(len(user) != 0 and user.isspace() == False):
        print("\t", count, ": ", end="")
        count = count+1
        user = input()

        arr = user.split(',')
        comment = ""
        if(len(arr) != 2 and len(arr) != 3): 
            count = count-1
            continue
        if(len(arr) == 3): comment = arr[2]
        
        name = arr[0]
        grams = arr[1]
        isLst = []
        try:
            grams = int(grams)
            foodList = [name]
            idLst = fdcID_retrieval(foodList)
            id = int(idLst[0])
        except:
            count = count-1
            continue

        food[name] = grams
        ids[name] = id
        comments[name] = comment

        fdcId = str(idLst[0])
        requested_url = USDA_URL + fdcId + '?api_key=' + api_key
        response = requests.get(requested_url, headers=headers)
        df = nutrition_retrieval(fdcIDs=isLst, api_key=api_key)
        parsed = json.loads(response.content)
        productName = parsed['description'][0:40]

    if(len(food) == 0): food = recipes_enterFood(name,servings)
    return food, ids.values(),list(comments.values()), productName

# combines above methods and sends foods/servings to fooddate_centray.py to print a set of nutrition facts
def recipes_main():

    # food = {'peanut butter': 32, 'banana': 110}
    # servings = 1

    # food = {'quick oats': 40,
    #          'powdered peanut butter': 13,
    #          'vanilla casein protein powder': 15,
    #          'chia seeds': 10,
    #          'cocoa powder': 10,
    #          'salt': 0.15,
    #          'plain non-fat greek yogurt': 100,
    #          'unsweetened applesauce': 50,
    #          'unsweetened vanilla almond milk': 100}
    # servings = 1

    # food = {'boneless skinless chicken breasts': 908,
    #         'carrots': 250,
    #         'celery': 200,
    #         'garlic': 22,
    #         'onion': 100,
    #         'yukon gold potatoes': 750,
    #         'peas': 170,
    #         'milk': 60,
    #         'unsalted butter': 28,
    #         'cornstarch': 30,
    #         'water': 30,
    #         'extra virgin olive oil': 30,
    #         'granulated chicken bouillion': 8,
    #         'salt': 3,
    #         'black pepper': 3}
    # servings = 5
    
    name = recipes_enterName()
    servings = recipes_enterServings(name)
    food,ids,comments,productName = recipes_enterFood(name,servings)
    recipes_infoPrint(name,servings,food,comments,productName)
    fc_main(name, food, servings, ids)


if __name__ == "__main__" :
    recipes_main()