import json
import mysql.connector

# Open json
with open("testing.json") as f:
    data = json.load(f)

# Sql connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="privatepassword",
  database="foodoramix"
)

mycursor = mydb.cursor()
mycursor.execute("DROP TABLE IF EXISTS ingredients;")
mycursor.execute("DROP TABLE IF EXISTS instructions;")
mycursor.execute("DROP TABLE IF EXISTS recipes;")
mycursor.execute("DROP TABLE IF EXISTS recipe_ingredient;")
mycursor.execute("DROP TABLE IF EXISTS recipe_instruction;")

mycursor.execute("CREATE TABLE ingredients (id_ingredient INTEGER, text VARCHAR(255));")
mycursor.execute("CREATE TABLE instructions (id_instruction INTEGER, text VARCHAR(255));")
mycursor.execute("CREATE TABLE recipes (id_recipe VARCHAR(255), title VARCHAR(255), url VARCHAR(255));")
mycursor.execute("CREATE TABLE recipe_ingredient (id_recipe VARCHAR(255), id_ingredient INTEGER);")
mycursor.execute("CREATE TABLE recipe_instruction (id_recipe VARCHAR(255), id_instruction INTEGER);")

dict_ingredients = {}
id_ingredient = 1
dict_instructions = {}
id_instruction = 1

for recipe in data:
    sql = "INSERT INTO recipes (id_recipe, title, url) VALUES ('" + recipe["id"] + "', '" + recipe["title"] + "', '" + recipe["url"] + "');"
    mycursor.execute(sql)

    for ingredient in recipe["ingredients"]:
        if ingredient['text'] not in dict_ingredients.keys():
            dict_ingredients[ingredient['text']] = id_ingredient
            sql = "INSERT INTO ingredients (id_ingredient, text) VALUES ('" + str(id_ingredient) + "', '" + ingredient['text'] + "');"
            mycursor.execute(sql)
            sql = "INSERT INTO recipe_ingredient (id_recipe, id_ingredient) VALUES ('" + recipe["id"] + "', '" + str(id_ingredient) + "');"
            mycursor.execute(sql)
            id_ingredient += 1
        else:
            sql = "INSERT INTO recipe_ingredient (id_recipe, id_ingredient) VALUES ('" + recipe["id"] + "', '" + str(dict_ingredients[ingredient['text']]) + "');"
            mycursor.execute(sql)

    for instruction in recipe["instructions"]:
        if instruction['text'] not in dict_instructions.keys():
            dict_instructions[instruction['text']] = id_instruction
            sql = "INSERT INTO instructions (id_instruction, text) VALUES ('" + str(id_instruction) + "', '" + instruction['text'] + "');"
            mycursor.execute(sql)
            sql = "INSERT INTO recipe_instruction (id_recipe, id_instruction) VALUES ('" + recipe["id"] + "', '" + str(id_instruction) + "');"
            mycursor.execute(sql)
            id_instruction += 1
        else:
            sql = "INSERT INTO recipe_instruction (id_recipe, id_instruction) VALUES ('" + recipe["id"] + "', '" + str(dict_instructions[instruction['text']]) + "');"
            mycursor.execute(sql)

mydb.commit()

# issue with recipe_instruction and recipe_ingredients, it seems reversed.
