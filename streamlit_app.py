import streamlit as st
import json
import random
from datetime import datetime
import pandas as pd


# Load recipes from a JSON file
def load_recipes():
    with open("recipes.json", "r") as f:
        return json.load(f)


# Function to get all side dishes from recipes, excluding "None"
def get_all_side_dishes(recipes):
    return sorted(
        [name for name, details in recipes.items() if "Side" in details["meal_type"]]
    )


# Generate a random menu for each meal of the day based on suitable recipes (excluding "None")
def generate_random_menu(recipes, side_dishes):
    return {
        "Breakfast": random.choice(
            [
                name
                for name, details in recipes.items()
                if "Breakfast" in details["meal_type"]
            ]
        ),
        "Lunch": {
            "main": random.choice(
                [
                    name
                    for name, details in recipes.items()
                    if "Lunch" in details["meal_type"]
                ]
            ),
            "side": random.choice(side_dishes),  # Exclude "None"
        },
        "Dinner": {
            "main": random.choice(
                [
                    name
                    for name, details in recipes.items()
                    if "Dinner" in details["meal_type"]
                ]
            ),
            "side": random.choice(side_dishes),  # Exclude "None"
        },
    }


# Create a menu with all options set to None
def clear_menu():
    return {
        "Breakfast": "None",
        "Lunch": {"main": "None", "side": "None"},
        "Dinner": {"main": "None", "side": "None"},
    }


# Display the weekly menu on screen as a table
def display_menu_as_table(weekly_menus):
    data = {
        "Breakfast": [weekly_menus[day]["Breakfast"] for day in weekly_menus],
        "Lunch": [weekly_menus[day]["Lunch"]["main"] for day in weekly_menus],
        "Lunch Side": [weekly_menus[day]["Lunch"]["side"] for day in weekly_menus],
        "Dinner": [weekly_menus[day]["Dinner"]["main"] for day in weekly_menus],
        "Dinner Side": [weekly_menus[day]["Dinner"]["side"] for day in weekly_menus],
    }
    df = pd.DataFrame(data, index=weekly_menus.keys())
    st.table(df)


# Save the finalized menu to a JSON file (recording each time it's confirmed)
def record_menu(menu, file_name="recorded_menus.json"):
    try:
        with open(file_name, "r") as f:
            recorded_menus = json.load(f)
    except FileNotFoundError:
        recorded_menus = []

    menu_with_time = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "menu": menu,
    }
    recorded_menus.append(menu_with_time)

    with open(file_name, "w") as f:
        json.dump(recorded_menus, f, indent=4)


# Generate a shopping list from the selected menu
def generate_shopping_list(selected_menus, recipes):
    shopping_list = set()  # Use a set to ensure unique ingredients
    for day_menu in selected_menus:
        for meal, recipe_details in day_menu.items():
            if isinstance(recipe_details, dict):
                main_recipe = recipe_details.get("main")
                if main_recipe and main_recipe in recipes:
                    ingredients = recipes[main_recipe]["ingredients"]
                    shopping_list.update(ingredients)

                side_recipe = recipe_details.get("side")
                if side_recipe and side_recipe != "None" and side_recipe in recipes:
                    ingredients = recipes[side_recipe]["ingredients"]
                    shopping_list.update(ingredients)

            else:
                if recipe_details in recipes:
                    ingredients = recipes[recipe_details]["ingredients"]
                    shopping_list.update(ingredients)

    return sorted(list(shopping_list))


# Load the meal data (recipes) from JSON file
recipes = load_recipes()

# Get all possible side dishes (excluding "None")
side_dishes = get_all_side_dishes(recipes)

# Define the days of the week and meals of the day
days_of_week = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

# Initialize the weekly menu with None for all options
if "weekly_menus" not in st.session_state:
    st.session_state["weekly_menus"] = {day: clear_menu() for day in days_of_week}

# Button to generate a random menu
if st.button("Generate Random Menu"):
    st.session_state["weekly_menus"] = {
        day: generate_random_menu(recipes, side_dishes) for day in days_of_week
    }

# Button to clear the menu (set all options to None)
if st.button("Clear Menu"):
    st.session_state["weekly_menus"] = {day: clear_menu() for day in days_of_week}

# Create UI for generating and adjusting the weekly menu
st.header("Weekly Menu Planner")

for day in days_of_week:
    st.subheader(day)

    # Use columns for Breakfast, Lunch, and Dinner
    col1, col2, col3 = st.columns(3)

    # Breakfast
    with col1:
        breakfast_options = ["None"] + sorted(
            [
                name
                for name, details in recipes.items()
                if "Breakfast" in details["meal_type"]
            ]
        )
        selected_recipe = st.selectbox(
            "Breakfast",
            options=breakfast_options,
            index=breakfast_options.index(
                st.session_state["weekly_menus"][day]["Breakfast"]
            ),
            key=f"{day}_Breakfast",
        )
        st.session_state["weekly_menus"][day]["Breakfast"] = selected_recipe

    # Lunch - Main and Side
    with col2:
        lunch_main_options = ["None"] + sorted(
            [
                name
                for name, details in recipes.items()
                if "Lunch" in details["meal_type"]
            ]
        )
        selected_lunch_main = st.selectbox(
            "Lunch Main",
            options=lunch_main_options,
            index=lunch_main_options.index(
                st.session_state["weekly_menus"][day]["Lunch"]["main"]
            ),
            key=f"{day}_Lunch_main",
        )
        st.session_state["weekly_menus"][day]["Lunch"]["main"] = selected_lunch_main

        selected_lunch_side = st.selectbox(
            "Lunch Side",
            options=["None"] + side_dishes,
            index=(["None"] + side_dishes).index(
                st.session_state["weekly_menus"][day]["Lunch"]["side"]
            ),
            key=f"{day}_Lunch_side",
        )
        st.session_state["weekly_menus"][day]["Lunch"]["side"] = selected_lunch_side

    # Dinner - Main and Side
    with col3:
        dinner_main_options = ["None"] + sorted(
            [
                name
                for name, details in recipes.items()
                if "Dinner" in details["meal_type"]
            ]
        )
        selected_dinner_main = st.selectbox(
            "Dinner Main",
            options=dinner_main_options,
            index=dinner_main_options.index(
                st.session_state["weekly_menus"][day]["Dinner"]["main"]
            ),
            key=f"{day}_Dinner_main",
        )
        st.session_state["weekly_menus"][day]["Dinner"]["main"] = selected_dinner_main

        selected_dinner_side = st.selectbox(
            "Dinner Side",
            options=["None"] + side_dishes,
            index=(["None"] + side_dishes).index(
                st.session_state["weekly_menus"][day]["Dinner"]["side"]
            ),
            key=f"{day}_Dinner_side",
        )
        st.session_state["weekly_menus"][day]["Dinner"]["side"] = selected_dinner_side

    st.markdown("---")

# Button to save the finalized menu and generate a shopping list
if st.button("Create Menu and Generate Shopping List"):
    record_menu(st.session_state["weekly_menus"])

    # Display the weekly menu as a table
    display_menu_as_table(st.session_state["weekly_menus"])

    # Generate the shopping list from the confirmed menu
    shopping_list = generate_shopping_list(
        st.session_state["weekly_menus"].values(), recipes
    )

    # Display the shopping list
    st.subheader("Shopping List")
    shopping_list_text = "\n".join(shopping_list)
    st.text_area("Shopping List", shopping_list_text, height=200)
