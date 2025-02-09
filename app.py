from requests_cache import CachedSession
from requests.adapters import HTTPAdapter
import requests
import logging
import sqlite3
import os

DB_FILENAME = "db/fridge.db"

# Get Logging (Can be set to DEBUG, WARN or ERROR & more?)
logging.basicConfig(level=logging.WARN)

# Initialize requests_cache (cache expires after 30min)
cached_session = CachedSession("themealdb_cache", backend="sqlite", expire_after=1800)

# ************************************************************************** //
#                                  Getters                                   //
# ************************************************************************** //


def get_random_meal(url):
  print("Getting meal...")
  try:
    url = "https://www.themealdb.com/api/json/v1/1/random.php"
    adapter = HTTPAdapter(max_retries=3)
    cached_session.mount("https://", adapter)
    cached_session.mount("http://", adapter)

    response = cached_session.get(url)
    response.raise_for_status()  # Raise for HTTP errors
    data = response.json()
    if not data:
      logging.error("response is empty")

    return data

  except Exception as e:
    logging.error(f"Error getting random meal: {e}")
    return None


# ************************************************************************** //
#                                  Database                                  //
# ************************************************************************** //


def setup_db():
  print("Setting up database...")
  # Make sure the directory exists
  os.makedirs(os.path.dirname(DB_FILENAME), exist_ok=True)

  conn = sqlite3.connect(DB_FILENAME)
  cursor = conn.cursor()

  # Create the table
  cursor.execute("""
CREATE TABLE IF NOT EXISTS meals (
    idMeal TEXT PRIMARY KEY,
    strMeal TEXT,
    strDrinkAlternate TEXT,
    strCategory TEXT,
    strArea TEXT,
    strInstructions TEXT,
    strMealThumb TEXT,
    strTags TEXT,
    strYoutube TEXT,
    strSource TEXT,
    strImageSource TEXT,
    strCreativeCommonsConfirmed TEXT,
    dateModified TEXT,
    ingredients TEXT,
    measures TEXT
);
  """)
  # Commit the changes
  conn.commit()
  # Close the connection
  conn.close()


def insert_meal(meal):
  print("Inserting meal into db...")

  conn = sqlite3.connect(DB_FILENAME)
  cursor = conn.cursor()

# Extract ingredients and measures from the meal data
  ingredients = []
  measures = []
  for i in range(1, 21):  # Check up to strIngredient20/strMeasure20
    ingredient = meal.get(f"strIngredient{i}", "")
    if ingredient and ingredient.strip():
      ingredients.append(ingredient.strip())
    measure = meal.get(f"strMeasure{i}", "")
    if measure and measure.strip():
      measures.append(measure.strip())

  # Insert meal into db
  cursor.execute(
    """
    INSERT INTO meals (
      idMeal,
      strMeal,
      strDrinkAlternate,
      strCategory,
      strArea, 
      strInstructions,
      strMealThumb, 
      strTags, 
      strYoutube, 
      strSource, 
      strImageSource, 
      strCreativeCommonsConfirmed, 
      dateModified, 
      ingredients, 
      measures
    )

    VALUES (
      ?, ?, ?, ?, ?,
      ?, ?, ?, ?, ?,
      ?, ?, ?, ?, ?
    )
    """,
    (
      meal.get("idMeal"),
      meal.get("strMeal"),
      meal.get("strDrinkAlternate"),
      meal.get("strCategory"),
      meal.get("strArea"),
      meal.get("strInstructions"),
      meal.get("strMealThumb"),
      meal.get("strTags"),
      meal.get("strYoutube"),
      meal.get("strSource"),
      meal.get("strImageSource"),
      meal.get("strCreativeCommonsConfirmed"),
      meal.get("dateModified"),
      ", ".join(ingredients),  # Store as comma-separated string
      ", ".join(measures),
    ),
  )

  conn.commit()
  conn.close()
  print(f"{meal.get('strMeal')} was added to the fridge.db")


# ************************************************************************** //
#                                    App                                     //
# ************************************************************************** //


def main():
  print("\nyo Luigi!")
  print("Sup' Zedro!\n")
  print("I is Friiiiiidge!!!!\n")

  setup_db()

  meal = get_random_meal("https://www.themealdb.com/api/json/v1/1/random.php")
  insert_meal(meal)


# Entry point for the script
if __name__ == "__main__":
  main()
