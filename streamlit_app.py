import streamlit as st
import json
import random
from datetime import datetime

# Load recipes from a JSON file
def load_recipes():
    with open("recipes.json", "r") as f:
        return json.load(f)

# Generate a random menu for each meal of the day based on suitable recipes
def generate_random_menu(recipes):
    return {
        "Breakfast": random.choice([name for name, details in recipes.items() if "Breakfast" in details["meal_type"]]),
        "Lunch": {"main": random.choice([name for name, details in recipes.items() if "Lunch" in details["meal_type"]]), "side": "None"},
        "Dinner": {"main": random.choice([name for name, details in recipes.items() if "Dinner" in details["meal_type"]]), "side": "None"}
    }

# Save the finalized menu to a JSON file (recording each time it's confirmed)
def record_menu(menu, file_name="recorded_menus.json"):
    try:
        with open(file_name, "r") as f:
            recorded_menus = json.load(f)
    except FileNotFoundError:
        recorded_menus = []

    # Add a timestamp and record the menu
    menu_with_time = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "menu": menu
    }
    recorded_menus.append(menu_with_time)

    # Save the updated recorded menus back to the JSON file
    with open(file_name, "w") as f:
        json.dump(recorded_menus, f, indent=4)

# Generate a shopping list from the selected menu
def generate_shopping_list(selected_menus, recipes):
    shopping_list = set()  # Use a set to ensure unique ingredients
    for day_menu in selected_menus:
        for meal, recipe_details in day_menu.items():
            if isinstance(recipe_details, dict):
                # Main dish ingredients
                main_recipe = recipe_details.get("main")
                if main_recipe and main_recipe in recipes:
                    ingredients = recipes[main_recipe]["ingredients"]
                    shopping_list.update(ingredients)
                
                # Side dish ingredients
                side_recipe = recipe_details.get("side")
                if side_recipe and side_recipe != "None" and side_recipe in recipes:
                    ingredients = recipes[side_recipe]["ingredients"]
                    shopping_list.update(ingredients)
                    
            else:
                # For Breakfast or other direct entries
                if recipe_details in recipes:
                    ingredients = recipes[recipe_details]["ingredients"]
                    shopping_list.update(ingredients)
    
    return sorted(list(shopping_list))  # Return a sorted list for easier readability

# Load the meal data (recipes) from JSON file
recipes = load_recipes()

# Define the days of the week and meals of the day
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Initialize the weekly menu
if 'weekly_menus' not in st.session_state:
    st.session_state['weekly_menus'] = {
        day: generate_random_menu(recipes) for day in days_of_week  # Ensure each day gets a random menu
    }

# Button to randomly regenerate the weekly menu
if st.button("Regenerate Weekly Menu"):
    st.session_state['weekly_menus'] = {
        day: generate_random_menu(recipes) for day in days_of_week  # Randomize independently for each day
    }

# Create UI for generating and adjusting the weekly menu (1-column layout)
st.header("Weekly Menu Planner")

for day in days_of_week:
    st.subheader(day)  # Just show the day, no meal headers
    
    # Use columns for Breakfast, Lunch, and Dinner
    col1, col2, col3 = st.columns(3)

    # Breakfast
    with col1:
        selected_recipe = st.selectbox(
            "",
            options=sorted([name for name, details in recipes.items() if "Breakfast" in details["meal_type"]]),
            index=0 if not st.session_state['weekly_menus'][day]["Breakfast"] or st.session_state['weekly_menus'][day]["Breakfast"] not in [name for name, details in recipes.items() if "Breakfast" in details["meal_type"]] else sorted([name for name, details in recipes.items() if "Breakfast" in details["meal_type"]]).index(st.session_state['weekly_menus'][day]["Breakfast"]),
            key=f"{day}_Breakfast"  # Unique key to avoid duplicate element IDs
        )
        st.session_state['weekly_menus'][day]["Breakfast"] = selected_recipe

    # Lunch - Main and Side (organized in columns)
    with col2:
        selected_lunch_main = st.selectbox(
            "",
            options=sorted([name for name, details in recipes.items() if "Lunch" in details["meal_type"]]),
            index=0 if not st.session_state['weekly_menus'][day]["Lunch"]["main"] or st.session_state['weekly_menus'][day]["Lunch"]["main"] not in [name for name, details in recipes.items() if "Lunch" in details["meal_type"]] else sorted([name for name, details in recipes.items() if "Lunch" in details["meal_type"]]).index(st.session_state['weekly_menus'][day]["Lunch"]["main"]),
            key=f"{day}_Lunch_main"
        )
        st.session_state['weekly_menus'][day]["Lunch"]["main"] = selected_lunch_main

        # Select any side for lunch from all sides
        selected_lunch_side = st.selectbox(
            "",
            options=["None"] + sorted([name for name, details in recipes.items() if "Side" in details["meal_type"]]),
            index=0 if not st.session_state['weekly_menus'][day]["Lunch"]["side"] or st.session_state['weekly_menus'][day]["Lunch"]["side"] not in [name for name, details in recipes.items() if "Side" in details["meal_type"]] else sorted(["None"] + [name for name, details in recipes.items() if "Side" in details["meal_type"]]).index(st.session_state['weekly_menus'][day]["Lunch"]["side"]),
            key=f"{day}_Lunch_side"
        )
        st.session_state['weekly_menus'][day]["Lunch"]["side"] = selected_lunch_side

    # Dinner - Main and Side (organized in columns)
    with col3:
        selected_dinner_main = st.selectbox(
            "",
            options=sorted([name for name, details in recipes.items() if "Dinner" in details["meal_type"]]),
            index=0 if not st.session_state['weekly_menus'][day]["Dinner"]["main"] or st.session_state['weekly_menus'][day]["Dinner"]["main"] not in [name for name, details in recipes.items() if "Dinner" in details["meal_type"]] else sorted([name for name, details in recipes.items() if "Dinner" in details["meal_type"]]).index(st.session_state['weekly_menus'][day]["Dinner"]["main"]),
            key=f"{day}_Dinner_main"
        )
        st.session_state['weekly_menus'][day]["Dinner"]["main"] = selected_dinner_main

        # Select any side for dinner from all sides
        selected_dinner_side = st.selectbox(
            "",
            options=["None"] + sorted([name for name, details in recipes.items() if "Side" in details["meal_type"]]),
            index=0 if not st.session_state['weekly_menus'][day]["Dinner"]["side"] or st.session_state['weekly_menus'][day]["Dinner"]["side"] not in [name for name, details in recipes.items() if "Side" in details["meal_type"]] else sorted(["None"] + [name for name, details in recipes.items() if "Side" in details["meal_type"]]).index(st.session_state['weekly_menus'][day]["Dinner"]["side"]),
            key=f"{day}_Dinner_side"
        )
        st.session_state['weekly_menus'][day]["Dinner"]["side"] = selected_dinner_side

    st.markdown("---")  # Add spacing between days

# Button to save the finalized menu and generate a shopping list
if st.button("Create Menu and Generate Shopping List"):
    # Record the finalized menu
    record_menu(st.session_state['weekly_menus'])

    # Generate the shopping list from the confirmed menu
    shopping_list = generate_shopping_list(st.session_state['weekly_menus'].values(), recipes)
    
    # Display the shopping list as a clean copy-paste format
    st.subheader("Shopping List (Copy-Paste Friendly)")
    shopping_list_text = "\n".join(shopping_list)  # Join items with newlines for easy copying
    st.text_area("Shopping List", shopping_list_text, height=200)
    
    st.success("Menu has been saved and shopping list generated!")
