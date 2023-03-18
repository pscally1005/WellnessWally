import os
from fooddata_central import *

def recipes_main():
    os.system("clear")

    oatmeal = {'quick oats': 40,
             'powdered peanut butter': 13,
             'vanilla casein protein powder': 15,
             'chia seeds': 10,
             'cocoa powder': 10,
             'salt': 0.15,
             'plain non-fat greek yogurt': 100,
             'unsweetened applesauce': 50,
             'unsweetened vanilla almond milk': 100}
    
    fc_main(oatmeal)


if __name__ == "__main__" :
    recipes_main()