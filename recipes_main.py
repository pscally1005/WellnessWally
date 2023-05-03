import os
from fooddata_central import *

def recipes_infoPrint(name="", servings="", foods={}):
    os.system("clear")
    print("RECIPE CREATOR")
    
    if(name == ""): return
    print("\nEnter the name of your recipe:", name)

    if(servings == ""): return
    print("\nEnter the number of servings:", servings)

    if(foods == {}): return
    print('\nEnter the ingredients of your recipe')
    print('Format: <name>,<grams>.  Enter nothing to finish')
    i = 1
    for x in foods:
        print('\t', i, ': ', x, ',', foods[x], sep='')
        i = i+1

# user enters the name of their recipe
def recipes_enterName():
    recipes_infoPrint()
    print("\nEnter the name of your recipe: ", end="")
    name = input()

    if(len(name) == 0 or name.isspace()): name = recipes_enterName()

    return name

# user enters the number of servings of their recipe
def recipes_enterServings(name):
    recipes_infoPrint(name)
    print("\nEnter the number of servings: ", end="")

    try:
        servings = int(input())
    except:
        servings = recipes_enterServings(name)

    return servings

# user enters the ingredients of their recipe
def recipes_enterFood(name,servings):
    recipes_infoPrint(name,servings)

    print("\nEnter the ingredients of your recipe")
    print('Format: <name>,<grams>.  Enter nothing to finish')
    user = "temp"
    food = {}
    
    count = 1
    while(len(user) != 0 and user.isspace() == False):
        print("\t", count, ": ", end="")
        count = count+1
        user = input()

        arr = user.split(',')
        if(len(arr) != 2): 
            count = count-1
            continue
        
        name = arr[0]
        grams = arr[1]
        try:
            grams = int(grams)
        except:
            count = count-1
            continue

        food[name] = grams

    if(len(food) == 0): food = recipes_enterFood(name,servings)
    return food

    # TODO: make sure food is valid
    # TODO: pass in an optional note for each food

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
    food = recipes_enterFood(name,servings)
    recipes_infoPrint(name,servings,food)
    fc_main(name, food, servings)


if __name__ == "__main__" :
    recipes_main()