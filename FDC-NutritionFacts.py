# Credit:  https://github.com/afogarty85/fooddata_central/blob/main/main.py
#
# TESTER: Calls FDC APIs to print FDC ID and Name from Response structure
#
import requests
import json
import numpy as np
import pandas as pd
import unicodedata

api_key = 'QBaAYhZWW7gUNHZryKozHvwtIg3PxQRDg1Owc0UM'

# Read CSV file into recipe dataframe
recipe_df = pd.read_csv ('recipe.csv')

# Get fdcIDs
fdcIDs = recipe_df.iloc[2]
fdcIDs_list_temp = fdcIDs.tolist()
fdcIDs_list = [el.replace('\xa0', ' ') for el in fdcIDs_list_temp]
fdcIDs_list.pop(0)
fdcIDs_df = pd.DataFrame(data=fdcIDs_list, columns=['FDC IDs'])

# Get Ingredients
ingredients_list = list(recipe_df.columns.values)
ingredients_list.pop(0)
ingredients_list_df = pd.DataFrame(data=ingredients_list[::],
                                   columns=['Ingredients'])

# Get Recipe Amounts
recipe_amounts = recipe_df.iloc[0].tolist()
recipe_amounts_list = list((np.array(recipe_amounts[1::],dtype=float)))

# Calculate Recipe Multiplier and build column array
recipe_amounts_list2 = [[i/100] for i in recipe_amounts_list]
recipe_multiplier = np.array(recipe_amounts_list2)


print("This is wnat we read from your file:  Ingredients, FDC IDs, and Amounts")
print(" ")

for x, y, z in zip(fdcIDs,ingredients_list, recipe_amounts):
    print(' {} \t {} \t\t\t{}'.format(x, y, z))

# Set API details
USDA_URL = 'https://api.nal.usda.gov/fdc/v1/'
headers = {'Content-Type': 'application/json'}

################################################################################################
def nutrition_retrieval(fdcIDs, api_key=api_key):

    # Set container storage and ordering
    nutrient_container = []
    nutrient_units_container = []

    nutrient_list = ['energy', 'protein', 'total lipids', 'carbs', 'fiber',
    'sugars', 'sugars_added', 'calcium', 'iron', 'potassium', 'sodium', 'vit_c', 'vit_a',
    'fa_tot_sat', 'fa_tot_mono', 'fa_tot_poly', 'fa_tot_trans', 'cholesterol',
    'phosph', 'zinc', 'manga', 'vit_d']
    
    nutrient_container.append(nutrient_list)
    
    # set API details
    USDA_URL = 'https://api.nal.usda.gov/fdc/v1/'
    headers = {'Content-Type': 'application/json'}
    # Loop over each FDCID; commit a API request for each
    for i in fdcIDs:
        fdcId = str(i)
        requested_url = USDA_URL + fdcId + '?api_key=' + api_key
        response = requests.get(requested_url, headers=headers)
        parsed = json.loads(response.content)
        energy = 0
        protein = 0
        total_lipid = 0
        carbs = 0
        fiber = 0
        sugars = 0
        sugars_added = 0
        calcium = 0
        iron = 0
        potassium = 0
        sodium = 0
        vit_c = 0
        vit_a = 0
        fa_tot_sat = 0
        fa_tot_mono = 0
        fa_tot_poly = 0
        fa_tot_trans = 0
        cholesterol = 0
        phosph = 0
        zinc = 0
        manga = 0
        vit_d = 0

        # Loop over dictionary length to look for desired data
        for j in range(0, len(parsed)):
            try:
                if parsed['foodNutrients'][j]['nutrient']['id'] == 1004:
                    total_lipid = parsed['foodNutrients'][j]['amount']              
                
                if parsed['foodNutrients'][j]['nutrient']['id'] == 1257:
                    fa_tot_trans = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1293:
                    fa_tot_poly = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1292:
                    fa_tot_mono = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1258:
                    fa_tot_sat = parsed['foodNutrients'][j]['amount']

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

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1235:
                    sugars_added = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1003:
                    protein = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1104:
                    vit_a = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1162:
                    vit_c = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1087:
                    calcium = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1089:
                    iron = parsed['foodNutrients'][j]['amount']

                if parsed['foodNutrients'][j]['nutrient']['id'] == 1008:
                    energy = parsed['foodNutrients'][j]['amount']
            # In case of nutrition not found; continue anyways
            except:
                    pass

        nutrient_container.append([energy, protein, total_lipid, carbs, fiber, sugars, sugars_added, calcium, iron, potassium, 
                                   sodium, vit_c, vit_a, fa_tot_sat, fa_tot_mono, fa_tot_poly, fa_tot_trans, cholesterol,
                                   phosph, zinc, manga, vit_d])


        # turn nutrient_list into df for preprocessing
        nutrient_df = pd.DataFrame(data=nutrient_container[1::],
                                   columns=['energy', 'protein', 'total_lipid', 'carbs', 'fiber',
                                            'sugars', 'sugars_added',  'calcium', 'iron', 'potassium', 'sodium', 'vit_c', 'vit_a',
                                            'fa_tot_sat', 'fa_tot_mono', 'fa_tot_poly', 'fa_tot_trans', 'cholesterol',
                                            'phosph', 'zinc', 'manga', 'vit_d'])

    return nutrient_df

################################################################################################
#
# Build Nutrients per 100 array
nutrient_df = nutrition_retrieval(fdcIDs=fdcIDs_list, api_key=api_key)
print(" ")
print("-------------------------------------------------------------------------------")
print("|                      Kotopaxi Nutrition Analysis                            |")
print("-------------------------------------------------------------------------------")
print("TABLE 1 - Nutrient Ingredient values per 100 grams - nutrient_df")
print(" ")

nutrients100_print_df = pd.concat([ingredients_list_df, nutrient_df], axis=1)
pd.set_option('display.max_columns', None)
print(nutrients100_print_df.round(2))

# Convert df to array so we can do math
nutrients_100gr_array = nutrient_df.to_numpy()

# Create array with Ingredients nutrition values
nutrients_recipe_array = nutrients_100gr_array * recipe_multiplier


nutrients_recipe_df = pd.DataFrame(data=nutrients_recipe_array,
                                   columns=['energy', 'protein', 'total_lipid', 'carbs', 'fiber',
                                            'sugars', 'sugars_added', 'calcium', 'iron', 'potassium', 'sodium', 'vit_c', 'vit_a',
                                            'fa_tot_sat', 'fa_tot_mono', 'fa_tot_poly', 'fa_tot_trans', 'cholesterol',
                                            'phosph', 'zinc', 'manga', 'vit_d'])

print(" ")
print("TABLE 2 - Nutrients in Recipe Ingredients - nutrients_recipe_df")
print(" ")

nutrients_recipe_print_df = pd.concat([ingredients_list_df, nutrients_recipe_df], axis=1)
print(nutrients_recipe_print_df.round(2))

# Calculate Totals

nutrients_recipe_df.loc['Total']= nutrients_recipe_df.sum()



fdcIDs_df = pd.DataFrame(data=fdcIDs_list, columns=['FDC IDs'])

nutrients_final = pd.concat([ingredients_list_df,fdcIDs_df, nutrients_recipe_df], axis=1)


print(" ")
print("TABLE 3 - Recipe Nutrition Analysis.  Output sent to file: koto-recipe-nutrition.csv")
print(" ")
print(nutrients_final)

# Print data to Excel
# nutrients_final.to_csv("koto-recipe-nutrition.csv", encoding='utf-8')

xlwriter = pd.ExcelWriter('Koto-Recipe-Nutrition.xlsx')
nutrients_final.to_excel(xlwriter, sheet_name='Nutrition', index=False)
nutrients100_print_df.to_excel(xlwriter, sheet_name='100 Grams', index=False)
recipe_df.to_excel(xlwriter, sheet_name='Recipe', index=False)

xlwriter.close()
