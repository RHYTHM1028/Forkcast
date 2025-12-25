#!/usr/bin/env python3
"""Export database to plain SQL file that can be imported on the server."""

import psycopg2
from psycopg2.extras import RealDictCursor

# Connect to local database
conn = psycopg2.connect(
    dbname='forkcast_db',
    user='forkcast_user',
    password='secure_password_123',
    host='localhost',
    port='5432'
)

output_file = 'a:/A/Documents/CSE471/forkcast1/forkcast_export.sql'

def sql_escape(value):
    """Convert Python values to SQL format"""
    if value is None:
        return 'NULL'
    elif isinstance(value, bool):
        return 'TRUE' if value else 'FALSE'
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # Escape single quotes by doubling them
        return "'" + str(value).replace("'", "''") + "'"

with open(output_file, 'w', encoding='utf-8') as f:
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Export users
    f.write("-- Users\n")
    cur.execute("SELECT * FROM users ORDER BY id")
    users = cur.fetchall()
    for user in users:
        f.write(f"INSERT INTO users (id, username, email, password_hash, full_name, bio, profile_image, created_at, updated_at) VALUES ")
        f.write(f"({user['id']}, {sql_escape(user['username'])}, {sql_escape(user['email'])}, {sql_escape(user['password_hash'])}, ")
        f.write(f"{sql_escape(user['full_name'])}, {sql_escape(user['bio'])}, {sql_escape(user['profile_image'])}, ")
        f.write(f"{sql_escape(str(user['created_at']))}, {sql_escape(str(user['updated_at']))});\n")
    
    # Export recipes
    f.write("\n-- Recipes\n")
    cur.execute("SELECT * FROM recipes ORDER BY id")
    recipes = cur.fetchall()
    for recipe in recipes:
        f.write(f"INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES ")
        f.write(f"({recipe['id']}, {recipe['user_id']}, {sql_escape(recipe['title'])}, {sql_escape(recipe['description'])}, ")
        f.write(f"{sql_escape(recipe['ingredients'])}, {sql_escape(recipe['instructions'])}, {recipe['prep_time']}, {recipe['cook_time']}, ")
        f.write(f"{recipe['servings']}, {recipe['calories_per_serving']}, {sql_escape(recipe['category'])}, {sql_escape(recipe['cuisine'])}, ")
        f.write(f"{sql_escape(recipe['difficulty'])}, {sql_escape(recipe['tags'])}, {sql_escape(recipe['image_url'])}, {sql_escape(recipe['is_public'])}, ")
        f.write(f"{sql_escape(recipe['is_favorite'])}, {sql_escape(recipe['forked_from_id'])}, {sql_escape(recipe['original_author_id'])}, ")
        f.write(f"{sql_escape(str(recipe['created_at']))}, {sql_escape(str(recipe['updated_at']))});\n")
    
    # Reset sequences
    f.write("\n-- Reset sequences\n")
    f.write(f"SELECT setval('users_id_seq', {len(users)}, true);\n")
    f.write(f"SELECT setval('recipes_id_seq', {len(recipes)}, true);\n")
    
    cur.close()

conn.close()

print(f"✅ Database exported to: {output_file}")
print(f"   - {len(users)} users")
print(f"   - {len(recipes)} recipes")
print("\nNow upload this file to your server and import it using:")
print("\\i /home/container/forkcast_export.sql")
