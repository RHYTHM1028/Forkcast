#!/usr/bin/env python3
"""Fix recipe formatting - split ingredients and instructions into separate lines."""

import psycopg2
import re

# Database connection
conn = psycopg2.connect(
    dbname='forkcast_db',
    user='forkcast_user',
    password='secure_password_123',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Get all recipes from Forkcast user
cur.execute("SELECT id, title, ingredients, instructions FROM recipes WHERE user_id = 1")
recipes = cur.fetchall()

print(f"Found {len(recipes)} recipes to update\n")

for recipe_id, title, ingredients, instructions in recipes:
    print(f"Updating: {title}")
    
    # Fix ingredients - split by commas
    # Already has commas between ingredients
    fixed_ingredients = ingredients.replace(', ', '\n')
    
    # Fix instructions - split by numbered steps
    # Instructions are like "1. Step one 2. Step two 3. Step three"
    # Split by pattern like "2. " "3. " etc but keep the step
    fixed_instructions = instructions
    # Replace patterns like " 2. " with newline
    for i in range(20, 0, -1):  # Go backwards to avoid issues
        fixed_instructions = fixed_instructions.replace(f' {i}. ', f'\n{i}. ')
    
    # Update the recipe
    cur.execute("""
        UPDATE recipes 
        SET ingredients = %s, instructions = %s 
        WHERE id = %s
    """, (fixed_ingredients, fixed_instructions, recipe_id))
    
    print(f"  ✓ Updated ingredients and instructions")

conn.commit()
cur.close()
conn.close()
print(f"\n✅ Successfully formatted all {len(recipes)} recipes!")
