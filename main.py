import requests, collections

api = "https://www.thecocktaildb.com/api/json/v1/1/search.php?s="
alcohols = ["vodka", "whiskey", "rum", "tequila", "brandy", "gin"]
response = requests.get("https://www.thecocktaildb.com/api/json/v1/1/search.php?s=")
drinks = response.json()['drinks']
hashmap = {}

for alc in alcohols:
    hashmap[alc] = requests.get(api + alc)

'''
    Adding this method to setup the lookup tables needed to match cocktails
'''


def set_up_drinks_lookup():
    cocktails_ingredients = {}
    ingredients_to_cocktails = collections.defaultdict(set)
    # compatible ingredients are any ingredients that are found in a recipe together
    compatible_ingredients = {}
    recipes = {}
    for alc in hashmap.keys():
        for drink in hashmap[alc].json()["drinks"]:
            cocktail_recipe = drink["strInstructions"]

            cocktail_name = drink["strDrink"]
            recipes[cocktail_name] = cocktail_recipe
            ingredients = [drink["strIngredient" + str(i)] for i in range(1, 16)]
            cocktails_ingredients[cocktail_name] = set(ingredients)
            cocktails_ingredients[cocktail_name].remove(None)
            for ingredient in (ingredients):
                ingredients_to_cocktails[ingredient].add(cocktail_name)
                if ingredient not in compatible_ingredients:
                    compatible_ingredients[ingredient] = set([i for i in ingredients if i != ingredient])
                else:
                    compatible_ingredients[ingredient].update([i for i in ingredients if i != ingredient])
    return cocktails_ingredients, ingredients_to_cocktails, compatible_ingredients, recipes


def match_ingredients(ingredients_so_far):
    for cocktail, recipe_ingredients in cocktails_ingredients.items():
        if ingredients_so_far == recipe_ingredients:
            cocktail_matches.add(cocktail)
            return True
    return False


def search_cocktail():
    for ingredient in ingredients:
        if ingredient not in compatible_ingredients:
            print("can't find {} in any recipe - skipping".format(ingredient))
        else:
            cocktail_recipe = set()
            cocktail_recipe.add(ingredient)
            dfs(cocktail_recipe, compatible_ingredients[ingredient])
    return


'''
    DFS Method to form possible cocktail ingredients formations and match them with the coctail lookup table
'''


def dfs(cocktail_recipe, potential_ingredients):
    if str(sorted(cocktail_recipe)) in visited:
        return
    visited.add(str(sorted(cocktail_recipe)))
    for ing in potential_ingredients:
        if ing in ingredients:
            cocktail_recipe.add(ing)
            # check to see if it's a recipe match
            found_match = match_ingredients(cocktail_recipe)
            # if found_match:
            #     print("Found a match")
            dfs(cocktail_recipe, compatible_ingredients[ing].intersection(potential_ingredients))
            cocktail_recipe.remove(ing)


'''
    Initial setup
'''


visited = set()
cocktail_matches = set()
partial_cocktails = {}
cocktails_ingredients, ingredients_to_cocktails, compatible_ingredients, recipes = set_up_drinks_lookup()
all_ingredients = set([j for i in cocktails_ingredients.values() for j in i])
with open('ingredients.txt', 'w') as f:
    for i in sorted(all_ingredients):
        f.write(str(i))
        f.write("\n")

'''
    Driver program
'''

if __name__ == "__main__":
    print("Please look into the ingredients text file input ingredients that you would want to search for. \n Type "
          "exit to stop entering")
    ingredients = []
    ing = None
    while True:
        ing = input()
        if ing.lower() == "exit":
            break
        if ing not in all_ingredients:
            print("Please enter a valid ingredient")
            continue
        ingredients.append(ing)
    print("Ingredients entered are", ingredients)
    search_cocktail()
    print("\n The coctails you can make with these ingredients are", cocktail_matches)
    print("\n The recipes are in possible_recipes.txt file")

    with open('ingredients.txt', 'w') as f:
        for i in cocktail_matches:
            f.write(str(i) + ": " + "\t" + recipes[i] + "\n")
