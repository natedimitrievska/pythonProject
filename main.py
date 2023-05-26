import random
import psycopg2

# Set up the necessary libraries and dependencies
# ...

def test_database_connection():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="natasa",
                                      host="127.0.0.1",
                                      port="5433",
                                      database="kitchenuacs")
        cursor = connection.cursor()
        print("Database connection successful.")
        cursor.close()
        connection.close()
    except psycopg2.Error as error:
        print("Error connecting to the database:", error)

def suggest_recipe(ingredients):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="natasa",
                                      host="127.0.0.1",
                                      port="5433",
                                      database="recipes")
        cursor = connection.cursor()
        # Query the recipe table for recipes that can be made with the given ingredients
        query = """
        SELECT name FROM recipes
        WHERE ingredients @> ARRAY[%s]
        """
        cursor.execute(query, (ingredients,))
        suggested_recipes = cursor.fetchall()
        cursor.close()
        connection.close()
        return suggested_recipes
    except psycopg2.Error as error:
        print("Error querying the recipe database:", error)

def suggest_groceries():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="natasa",
                                      host="127.0.0.1",
                                      port="5433",
                                      database="groceries")
        cursor = connection.cursor()
        suggested_groceries = ["Apple", "Pork", "Tortilla", "Ketchup", "Tomato", "Peanuts", "Eggs", "Chicken", "Pasta", "Mushrooms", "Orange", "Lemon", "Ketchup", "Mayo", "Cream", "Chocolate", "Beef", "Hot Dog"]
        cursor.close()
        connection.close()
        return suggested_groceries
    except psycopg2.Error as error:
        print("Error suggesting groceries:", error)


def suggest_similar_recipes(recipe):
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="natasa",
                                      host="127.0.0.1",
                                      port="5433",
                                      database="recipes")
        cursor = connection.cursor()

        # Query for similar recipes based on ingredient matching
        query = """
        SELECT r.name
        FROM recipes r
        INNER JOIN (
            SELECT unnest(ingredients) AS ingredient
            FROM recipes
            WHERE LOWER(name) = LOWER(%s)
        ) t ON t.ingredient = ANY(r.ingredients)
        WHERE LOWER(r.name) != LOWER(%s)
        GROUP BY r.name
        """

        cursor.execute(query, (recipe, recipe))
        similar_recipes = cursor.fetchall()

        cursor.close()
        connection.close()

        return similar_recipes
    except psycopg2.Error as error:
        print("Error suggesting similar recipes:", error)

def suggest_recommendations():
    try:
        connection = psycopg2.connect(user="postgres",
                                      password="natasa",
                                      host="127.0.0.1",
                                      port="5433",
                                      database="suggestrecommendations")
        cursor = connection.cursor()

        query = "SELECT name FROM recommended_recipes"
        cursor.execute(query)
        recommended_recipes = cursor.fetchall()

        cursor.close()
        connection.close()

        return recommended_recipes
    except psycopg2.Error as error:
        print("Error suggesting recommendations:", error)

def main():
    test_database_connection()

    print("Welcome to Kitchen Companion!")
    while True:
        print("Please select an option:")
        print("1. Find a recipe")
        print("2. Get suggested groceries")
        print("3. Find similar recipes")
        print("4. Get recommendations")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            ingredients = input("Enter the ingredients you have (separated by commas): ").split(',')
            suggested_recipes = suggest_recipe(ingredients)
            print("Suggested recipes:")
            for recipe in suggested_recipes:
                print("- " + recipe[0])

        elif choice == "2":
            suggested_groceries = suggest_groceries()
            print("Suggested groceries:")
            for grocery in suggested_groceries:
                print("- " + grocery)

        elif choice == "3":
            recipe = input("Enter a recipe name: ")
            similar_recipes = suggest_similar_recipes(recipe)
            print("Similar recipes:")
            for recipe in similar_recipes:
                print("- " + recipe[0])

        elif choice == "4":
            recommended_recipes = suggest_recommendations()
            print("Recommended recipes:")
            for recipe in recommended_recipes:
                print("- " + recipe)

        elif choice == "0":
            print("Thank you for using Kitchen Companion. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
