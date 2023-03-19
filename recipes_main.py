import os
from fooddata_central import *

def recipes_main():
    os.system("clear")

    food = {'quick oats': 40,
             'powdered peanut butter': 13,
             'vanilla casein protein powder': 15,
             'chia seeds': 10,
             'cocoa powder': 10,
             'salt': 0.15,
             'plain non-fat greek yogurt': 100,
             'unsweetened applesauce': 50,
             'unsweetened vanilla almond milk': 100}

    # food = {'boneless skinless chicken breasts': 908/5,
    #         'carrots': 250/5,
    #         'celery': 200/5,
    #         'garlic': 22/5,
    #         'onion': 100/5,
    #         'yukon gold potatoes': 750/5,
    #         'peas': 170/5,
    #         'milk': 60/5,
    #         'unsalted butter': 28/5,
    #         'cornstarch': 30/5,
    #         'water': 30/5,
    #         'extra virgin olive oil': 30/5,
    #         'granulated chicken bouillion': 8/5,
    #         'salt': 1,
    #         'black pepper': 1}

    # TODO: input amount of servings
    
    fc_main(food)


if __name__ == "__main__" :
    recipes_main()