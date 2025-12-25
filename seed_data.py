#!/usr/bin/env python3
"""Seed database with Forkcast user and popular recipes."""

import psycopg2
from werkzeug.security import generate_password_hash

# Database connection
conn = psycopg2.connect(
    dbname='forkcast_db',
    user='forkcast_user',
    password='secure_password_123',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Create Forkcast user
password_hash = generate_password_hash('forkcastadmin')
cur.execute("""
    INSERT INTO users (username, email, password_hash, full_name, bio)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING id
""", ('Forkcast', 'forkcast@forkcast.com', password_hash, 'Forkcast Team', 'Official Forkcast recipe collection'))

user_id = cur.fetchone()[0]
print(f"Created user 'Forkcast' with ID: {user_id}")

# Insert recipes
recipes = [
    # 1. World's Best Lasagna
    (user_id, "World's Best Lasagna", 'The most popular recipe on Allrecipes with over 20,000 reviews. A rich, meaty, multi-layered masterpiece.', 
    '1lb sweet Italian sausage, 3/4lb lean ground beef, 1/2 cup minced onion, 2 cloves garlic crushed, 1 (28oz) can crushed tomatoes, 2 (6oz) cans tomato paste, 2 (6.5oz) cans canned tomato sauce, 1/2 cup water, 2 tbsp white sugar, 1.5 tsp dried basil leaves, 1/2 tsp fennel seeds, 1 tsp Italian seasoning, 1 tbsp salt, 1/4 tsp black pepper, 4 tbsp chopped fresh parsley, 12 lasagna noodles, 16oz ricotta cheese, 1 egg, 3/4lb mozzarella cheese sliced, 3/4 cup grated Parmesan cheese', 
    '1. Cook sausage, beef, onion, and garlic over medium heat until browned. 2. Stir in tomatoes, paste, sauce, and water. Season with sugar, basil, fennel, Italian seasoning, salt, pepper, and 2 tbsp parsley. Simmer 1.5 hours. 3. Boil noodles until al dente. 4. Mix ricotta, egg, and remaining parsley. 5. Layer sauce, noodles, ricotta mixture, mozzarella, and Parmesan in a 9x13 dish. Repeat. 6. Bake at 375°F (190°C) for 25 mins covered, then 25 mins uncovered.', 
    30, 150, 12, 448, 'Main Dish', 'Italian-American', 'Medium', 'lasagna, pasta, dinner, classic, beef', 'https://www.allrecipes.com/thmb/MkKfYU4o9_S_9_T_6_X_0_8_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/23600-worlds-best-lasagna-DDMFS-4x3-1196-24c54011ca0541d29ef19ec6d6389f41.jpg', True, user_id),
    
    # 2. Chef John's Drunken Noodles
    (user_id, "Chef John's Drunken Noodles", 'Known as Pad Kee Mao, this spicy, savory Thai street food classic is a favorite for late-night cravings.', 
    '8oz dried rice noodles, 1/4 cup oyster sauce, 1/4 cup soy sauce, 1 tbsp fish sauce, 1 tbsp maple syrup, 1 tsp sugar, 2 tbsp water, 2 tbsp vegetable oil, 1 tsp sesame oil, 1 cup sliced shallots, 6 tsp sliced bird\'s eye chiles, 4 cloves garlic, 2.5lb chicken thighs cut into strips, 1lb Chinese broccoli, 4 scallions, 1 cup fresh Thai basil', 
    '1. Soak noodles in hot water for 15 mins until flexible. 2. Whisk oyster sauce, soy, fish sauce, syrup, sugar, and water. 3. Sauté shallots, chiles, and garlic in oils. 4. Add chicken and sear. 5. Toss in broccoli stems, then leaves. 6. Pour in sauce and scallions; add noodles. 7. Toss for 2 mins until sauce is absorbed. 8. Stir in basil and serve.', 
    15, 15, 4, 341, 'Main Dish', 'Thai', 'Medium', 'spicy, noodles, street food, chicken, chef john', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8385585-chef-johns-drunken-noodles-4x3-1-08147774e6f44f5092a953922369650d.jpg', True, user_id),
    
    # 3. Curry Stand Chicken Tikka Masala
    (user_id, 'Curry Stand Chicken Tikka Masala', 'A "nuclear-orange" tikka masala that mimics the best British-Indian curry stand flavors.', 
    '2 tbsp ghee, 1 onion chopped, 4 cloves garlic, 1 tbsp cumin, 1 tsp ginger, 1 tsp cayenne, 1/2 tsp cinnamon, 1/4 tsp turmeric, 14oz tomato sauce, 1 cup heavy cream, 1 tbsp sugar, 2 tsp paprika, 4 chicken breasts diced, 1/2 tsp curry powder', 
    '1. Sauté onion in ghee until translucent; add garlic. 2. Stir in dry spices (cumin to turmeric) and fry until fragrant. 3. Stir in tomato sauce; simmer 10 mins. 4. Mix in cream, sugar, and paprika; simmer until thickened. 5. In a separate pan, sear chicken with curry powder. 6. Transfer chicken to sauce and simmer for 30 mins.', 
    15, 65, 6, 480, 'Main Dish', 'Indian', 'Medium', 'curry, chicken, spicy, creamy, tikka masala', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/239867-curry-stand-chicken-tikka-masala-sauce-ddmfs-4x3-0544-0b44576307304f3299a9e34a2e87902d.jpg', True, user_id),
    
    # 4. Good Old-Fashioned Pancakes
    (user_id, 'Good Old-Fashioned Pancakes', 'Simple, fluffy, and dependable. The quintessential American breakfast.', 
    '1.5 cups all-purpose flour, 3.5 tsp baking powder, 1 tsp salt, 1 tbsp white sugar, 1.25 cups milk, 1 egg, 3 tbsp butter melted', 
    '1. Sift flour, baking powder, salt, and sugar in a large bowl. 2. Make a well in the center and pour in milk, egg, and melted butter; mix until smooth. 3. Heat a lightly oiled griddle over medium-high heat. 4. Pour scoop of batter onto the griddle; brown on both sides.', 
    5, 15, 8, 158, 'Breakfast', 'American', 'Easy', 'pancakes, breakfast, brunch, quick', 'https://www.allrecipes.com/thmb/Wq0n_g_y_8_X_9_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/21014-Good-old-Fashioned-Pancakes-mfs_001-1fa26dec577f4e42ad746f1f610a9092.jpg', True, user_id),
    
    # 5. Banana Banana Bread
    (user_id, 'Banana Banana Bread', 'The highest-rated banana bread on the site. Using more bananas is the secret to its popularity.', 
    '2 cups all-purpose flour, 1 tsp baking soda, 1/4 tsp salt, 1/2 cup butter, 3/4 cup brown sugar, 2 eggs beaten, 2.33 cups mashed overripe bananas', 
    '1. Preheat oven to 350°F (175°C). Grease a 9x5 inch loaf pan. 2. Cream butter and sugar. Add eggs and mashed bananas. 3. Combine flour, soda, and salt; stir into banana mixture until just moistened. 4. Bake for 60 to 65 minutes.', 
    15, 60, 12, 229, 'Dessert', 'American', 'Easy', 'baking, bread, bananas, snack, sweet', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20144-banana-banana-bread-mfs-60-93a8e98363714b1a8d11_0235d9435b6c4e0980209930f7ca6.jpg', True, user_id),
    
    # 6. Scott Hibb's Amazing Whisky Grilled Ribs
    (user_id, "Scott Hibb's Amazing Whisky Grilled Ribs", 'Finger-licking baby back ribs with a unique whisky-infused glaze.', 
    '2 racks baby back pork ribs, salt/pepper, 1 cup whisky, 1 cup ketchup, 1/2 cup brown sugar, 1/4 cup vinegar, 1 tbsp onion powder, 1 tbsp garlic powder', 
    '1. Season ribs; pre-cook in oven at 300°F wrapped in foil for 2 hours. 2. Combine glaze ingredients in a pan; simmer until thick. 3. Grill ribs over medium heat, basting generously with glaze for 10-15 mins until charred and sticky.', 
    20, 135, 4, 750, 'Main Dish', 'American', 'Hard', 'bbq, ribs, pork, grilling, whisky', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/22469-scott-hibbs-amazing-whisky-grilled-baby-back-ribs-ddmfs-4x3-1081-3067e4369a23402484c2f10b784a958e.jpg', True, user_id),
    
    # 7. Mom's Chicken Pot Pie
    (user_id, "Mom's Chicken Pot Pie", 'The ultimate comfort food. Creamy chicken and vegetable filling in a flaky crust.', 
    '1lb skinless chicken breast diced, 1 cup sliced carrots, 1 cup frozen peas, 1/2 cup sliced celery, 1/3 cup butter, 1/3 cup onion, 1/3 cup flour, 1/2 tsp salt, 1/4 tsp pepper, 1/4 tsp celery seed, 1.75 cups chicken broth, 2/3 cup milk, 2 (9 inch) unbaked pie crusts', 
    '1. Boil chicken, carrots, peas, and celery for 15 mins. 2. Cook onions in butter until soft; stir in flour and seasonings. 3. Gradually add broth and milk; simmer until thick. 4. Place chicken/veg in bottom pie crust; pour sauce over. 5. Top with second crust; bake at 425°F for 30-35 mins.', 
    20, 35, 8, 415, 'Main Dish', 'American', 'Medium', 'comfort food, chicken, pie, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/26317-moms-chicken-pot-pie-mfs_010-02558f339178465b89a8ef153f318991.jpg', True, user_id),
    
    # 8. Marry Me Chicken Soup
    (user_id, 'Marry Me Chicken Soup', 'A viral 2024 sensation. A creamy, sun-dried tomato and parmesan-based soup that is incredibly cozy.', 
    '2 tbsp olive oil, 1lb chicken breasts, 1 onion, 3 cloves garlic, 1/2 cup sun-dried tomatoes, 1 tsp oregano, 1/2 tsp red pepper flakes, 4 cups chicken broth, 1/2 cup heavy cream, 1/2 cup grated Parmesan, 2 cups spinach', 
    '1. Brown chicken in oil; remove and shred. 2. Sauté onion, garlic, and sun-dried tomatoes. 3. Add spices and broth; simmer 10 mins. 4. Stir in shredded chicken, cream, and parmesan. 5. Add spinach at the end until wilted.', 
    15, 25, 4, 380, 'Soup', 'American', 'Easy', 'viral, soup, chicken, creamy, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8711470-marry-me-chicken-soup-4x3-1-7918451842094200a747065997235222.jpg', True, user_id),
    
    # 9. Oven-Roasted Greek Potatoes
    (user_id, 'Oven-Roasted Greek Potatoes', 'Crispy on the outside, tender on the inside, with bright lemon and oregano flavors.', 
    '4 large potatoes peeled and wedged, 1/2 cup olive oil, 1/2 cup water, 1 tsp dried oregano, 1 tsp salt, 1/4 tsp black pepper, 2 cloves garlic minced, 1 lemon juiced', 
    '1. Preheat oven to 400°F (200°C). 2. Place potato wedges in a baking tin. 3. Mix olive oil, water, oregano, salt, pepper, garlic, and lemon juice; pour over potatoes. 4. Bake for 60 mins, turning once, until golden and crisp.', 
    10, 60, 6, 210, 'Side Dish', 'Greek', 'Easy', 'potatoes, lemon, vegan, gluten-free, mediterranean', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/95030-oven-roasted-greek-potatoes-ddmfs-3x4-0518-9125439a838541a7985338f0d84c6604.jpg', True, user_id),
    
    # 10. Taco Bake Casserole
    (user_id, 'Taco Bake Casserole', 'A family-favorite weeknight meal that combines all the best parts of a taco into an easy bake.', 
    '1lb ground beef, 1 packet taco seasoning, 1 (16oz) can refried beans, 1 cup salsa, 2 cups shredded Mexican cheese blend, 1 bag corn chips, lettuce/tomato for garnish', 
    '1. Brown beef and drain; stir in taco seasoning. 2. In a baking dish, layer refried beans, then beef, then salsa. 3. Top with a thick layer of cheese. 4. Bake at 350°F for 20 mins. 5. Serve over a bed of corn chips and top with fresh lettuce and tomato.', 
    10, 20, 6, 450, 'Main Dish', 'Mexican-Style', 'Easy', 'taco, casserole, beef, family, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/17131-taco-bake-mfs-103-f366e6b5413149869687483842c54f5c.jpg', True, user_id),
]

for recipe in recipes:
    cur.execute("""
        INSERT INTO recipes (
            user_id, title, description, ingredients, instructions, prep_time, cook_time, 
            servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, 
            is_public, original_author_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, recipe)
    print(f"Inserted recipe: {recipe[1]}")

conn.commit()
cur.close()
conn.close()
print("\n✅ Successfully seeded database with Forkcast user and 10 recipes!")
