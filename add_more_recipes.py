#!/usr/bin/env python3
"""Add more recipes to the Forkcast user."""

import psycopg2

# Database connection
conn = psycopg2.connect(
    dbname='forkcast_db',
    user='forkcast_user',
    password='secure_password_123',
    host='localhost',
    port='5432'
)
cur = conn.cursor()

# Get Forkcast user ID
cur.execute("SELECT id FROM users WHERE username = 'Forkcast'")
result = cur.fetchone()
if not result:
    print("Error: Forkcast user not found!")
    exit(1)

user_id = result[0]
print(f"Adding recipes for user 'Forkcast' (ID: {user_id})")

# Insert additional recipes (11-35)
recipes = [
    # 11. Baked Ziti
    (user_id, 'Baked Ziti', 'A classic cheesy pasta bake that is a staple for potlucks and family dinners.', 
    '1lb ziti pasta, 1lb ground beef, 2 (26oz) jars spaghetti sauce, 6oz provolone cheese sliced, 1.5 cups ricotta, 6oz mozzarella cheese shredded, 2 tbsp grated Parmesan', 
    '1. Boil ziti until al dente. 2. Brown beef in a pan; add sauce and simmer. 3. Mix ziti with meat sauce. 4. In a 9x13 dish, layer half of the ziti, then provolone, then ricotta. Add remaining ziti and top with mozzarella and parmesan. 5. Bake at 350°F (175°C) for 30 mins.', 
    15, 30, 8, 450, 'Main Dish', 'Italian', 'Easy', 'pasta, cheese, beef, comfort-food', 'https://www.allrecipes.com/thmb/9_M_X_X_j_X_P_U_o_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/11758-baked-ziti-ii-ddmfs-4x3-0382-7f329432d84749f7823521d8b671a7d6.jpg', True, user_id),
    
    # 12. Best Chocolate Chip Cookies
    (user_id, 'Best Chocolate Chip Cookies', 'Over 15,000 5-star reviews. These are soft, chewy, and perfectly balanced.', 
    '1 cup butter softened, 1 cup white sugar, 1 cup brown sugar, 2 eggs, 2 tsp vanilla, 1 tsp baking soda, 2 tsp hot water, 1/2 tsp salt, 3 cups flour, 2 cups chocolate chips', 
    '1. Cream butter and sugars. Beat in eggs and vanilla. 2. Dissolve baking soda in hot water; add to batter with salt. 3. Stir in flour and chocolate chips. 4. Drop large spoonfuls onto ungreased pans. 5. Bake at 350°F (175°C) for 10 mins until edges are brown.', 
    20, 10, 24, 298, 'Dessert', 'American', 'Medium', 'cookies, chocolate, baking, sweet', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/10813-best-chocolate-chip-cookies-mfs-641561-1-be21147f07094ee7a8989b537d998782.jpg', True, user_id),
    
    # 13. Awesome Slow Cooker Pot Roast
    (user_id, 'Awesome Slow Cooker Pot Roast', 'The definitive set-it-and-forget-it meal. The gravy develops a deep, rich flavor.', 
    '3lb chuck roast, 2 (10oz) cans condensed cream of mushroom soup, 1 packet dry onion soup mix, 1 cup water, 4 potatoes chopped, 4 carrots sliced', 
    '1. Place roast in slow cooker. 2. Mix soup, dry soup mix, and water; pour over roast. 3. Add potatoes and carrots around the meat. 4. Cover and cook on Low for 8-10 hours.', 
    10, 480, 6, 520, 'Main Dish', 'American', 'Easy', 'slow-cooker, beef, roast, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/16066-awesome-slow-cooker-pot-roast-ddmfs-3x4-0472-e5658097984144e096f4b6794689626e.jpg', True, user_id),
    
    # 14. Apple Pie by Grandma Ople
    (user_id, 'Apple Pie by Grandma Ople', 'A unique lattice-topped pie where a buttery caramel sauce is poured over the crust before baking.', 
    '1 recipe pastry for a double-crust pie, 1/2 cup butter, 3 tbsp flour, 1/4 cup water, 1/2 cup white sugar, 1/2 cup brown sugar, 8 Granny Smith apples', 
    '1. Melt butter, stir in flour and sugars to form a paste; add water and simmer. 2. Place sliced apples in bottom crust. Lattice the top crust. 3. Pour caramel liquid over the lattice. 4. Bake at 425°F for 15 mins, then lower to 350°F and bake 45 mins.', 
    30, 60, 8, 412, 'Dessert', 'American', 'Hard', 'apple-pie, baking, fruit, dessert', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/12682-apple-pie-by-grandma-ople-mfs-001-c88c7f766e014798b3769ca12f9f8c5b.jpg', True, user_id),
    
    # 15. Baked Teriyaki Chicken
    (user_id, 'Baked Teriyaki Chicken', 'Homemade teriyaki sauce makes these thighs sticky and addictive.', 
    '1 tbsp cornstarch, 1 tbsp cold water, 1/2 cup white sugar, 1/2 cup soy sauce, 1/4 cup cider vinegar, 1 clove garlic minced, 1/2 tsp ginger, 12 skinless chicken thighs', 
    '1. Mix cornstarch and water. In a small pot, combine sugar, soy sauce, vinegar, garlic, and ginger; boil until thick. 2. Place chicken in a baking dish and coat with sauce. 3. Bake at 425°F (220°C) for 30 minutes, turning once.', 
    15, 30, 6, 320, 'Main Dish', 'Japanese-Style', 'Easy', 'chicken, teriyaki, quick, asian', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8930-baked-teriyaki-chicken-ddmfs-4x3-1025-a134f59e66344795b9c030d95015e510.jpg', True, user_id),
    
    # 16. Meatball Nirvana
    (user_id, 'Meatball Nirvana', 'These meatballs are light, fluffy, and tender thanks to a secret ratio of breadcrumbs and parmesan.', 
    '1lb ground beef, 1/2lb ground pork, 1/2 cup breadcrumbs, 1/4 cup milk, 1/2 cup grated Parmesan, 1 egg, 1/2 cup chopped parsley, 2 cloves garlic', 
    '1. Mix all ingredients in a large bowl. 2. Roll into 2-inch balls. 3. Brown in a skillet with olive oil. 4. Finish cooking in your favorite marinara sauce for 20 mins.', 
    20, 25, 6, 310, 'Main Dish', 'Italian-American', 'Medium', 'meatballs, beef, dinner, pasta', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/14603-meatball-nirvana-ddmfs-1x1-1-58479e02c67645e589a66d03d3c8c5c4.jpg', True, user_id),
    
    # 17. To-Die-For Blueberry Muffins
    (user_id, 'To-Die-For Blueberry Muffins', 'Huge bakery-style muffins with a sugary streusel topping.', 
    '1.5 cups flour, 3/4 cup sugar, 1/2 tsp salt, 2 tsp baking powder, 1/3 cup oil, 1 egg, 1/3 cup milk, 1 cup blueberries, Streusel topping: 1/2 cup sugar, 1/3 cup flour, 1/4 cup butter', 
    '1. Mix dry ingredients; add egg, oil, and milk. Fold in berries. 2. Fill muffin cups to the top. 3. Top with mixed streusel (sugar, flour, butter). 4. Bake at 400°F (200°C) for 20-25 mins.', 
    15, 20, 12, 381, 'Breakfast', 'American', 'Easy', 'muffins, blueberry, breakfast, sweet', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/6865-to-die-for-blueberry-muffins-mfs-044-1-6d2466085a67448d8c92a2a7a40b8296.jpg', True, user_id),
    
    # 18. Quinoa and Black Beans
    (user_id, 'Quinoa and Black Beans', 'A high-protein vegan staple that is excellent for meal prep.', 
    '1 tsp oil, 1 onion, 3 cloves garlic, 3/4 cup quinoa, 1.5 cups vegetable broth, 1 tsp cumin, 1/4 tsp cayenne, 1 (15oz) can black beans, 1 cup frozen corn', 
    '1. Sauté onion and garlic. 2. Add quinoa, broth, and spices. Bring to boil, then simmer for 20 mins. 3. Stir in beans and corn; heat through. Garnish with cilantro.', 
    10, 25, 4, 320, 'Healthy', 'International', 'Easy', 'vegan, quinoa, beans, healthy, lunch', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/quinoa-and-black-beans-2151125-4x3-3323-99933096057948339591404c084666f7.jpg', True, user_id),
    
    # 19. Buffalo Chicken Dip
    (user_id, 'Buffalo Chicken Dip', 'The ultimate party snack. Creamy, spicy, and perfect with chips or celery.', 
    '2 cups shredded cooked chicken, 1 (8oz) package cream cheese softened, 1/2 cup Buffalo wing sauce, 1/2 cup ranch dressing, 1.5 cups shredded Monterey Jack cheese', 
    '1. Mix chicken, cream cheese, wing sauce, ranch, and half the Jack cheese in a bowl. 2. Spread in a shallow baking dish. 3. Top with remaining cheese. 4. Bake at 350°F (175°C) for 20 mins until bubbly.', 
    10, 20, 10, 268, 'Appetizer', 'American', 'Easy', 'buffalo-chicken, dip, party, spicy', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/22644-buffalo-chicken-dip-mfs-031-63806c9a9d704d98939c323f49b06297.jpg', True, user_id),
    
    # 20. Chantal's New York Cheesecake
    (user_id, "Chantal's New York Cheesecake", 'Rich, dense, and creamy with a simple graham cracker crust.', 
    '1.5 cups graham cracker crumbs, 2 cups sugar, 1/4 cup butter melted, 4 (8oz) packages cream cheese, 3/4 cup milk, 4 eggs, 1 cup sour cream, 1 tbsp vanilla, 1/4 cup flour', 
    '1. Press crumbs/butter into a springform pan. 2. Cream sugar and cream cheese until smooth. 3. Add milk, then eggs one by one. Stir in sour cream, vanilla, and flour. 4. Bake at 350°F (175°C) for 1 hour. Let cool in oven with door closed for 5 hours.', 
    30, 60, 12, 650, 'Dessert', 'American', 'Hard', 'cheesecake, dessert, classic, baking', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8350-chantals-new-york-cheesecake-ddmfs-4x3-2550-9c8828b6d3a9484ca781b2447950c40e.jpg', True, user_id),
    
    # 21. Baked Tilapia Parmesan
    (user_id, 'Baked Tilapia Parmesan', 'A light, crispy, and savory way to prepare white fish.', 
    '4 tilapia fillets, 1/4 cup butter softened, 3 tbsp mayo, 2 tbsp lemon juice, 1/4 cup Parmesan, 1/4 tsp dried basil, 1/4 tsp onion powder', 
    '1. Broil fillets for 2-3 mins per side. 2. Mix butter, mayo, lemon, cheese, and spices. 3. Spread mixture over fillets. 4. Broil for 2 more mins until brown and bubbly.', 
    10, 10, 4, 215, 'Main Dish', 'Seafood', 'Easy', 'fish, tilapia, seafood, low-carb', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8923-baked-tilapia-parmesan-ddmfs-3x4-0554-e6944062f83141f3918a0058e578330a.jpg', True, user_id),
    
    # 22. Ultimate Twice-Baked Potatoes
    (user_id, 'Ultimate Twice-Baked Potatoes', 'Everything you love about a loaded baked potato in a neat, double-cooked shell.', 
    '4 large russet potatoes, 1/4 cup butter, 1/4 cup sour cream, 1/4 cup milk, 1 cup shredded Cheddar, 4 slices bacon cooked/crumbled, 2 green onions', 
    '1. Bake potatoes at 400°F for 1 hour. 2. Slice in half and scoop out insides. 3. Mash insides with butter, cream, milk, half the cheese, and bacon. 4. Stuff shells and top with remaining cheese. 5. Bake for 15 mins more.', 
    15, 75, 8, 345, 'Side Dish', 'American', 'Medium', 'potatoes, cheese, bacon, side-dish', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20647-ultimate-twice-baked-potatoes-ddmfs-3x4-0599-299f056d607e467d8f58356f9103e302.jpg', True, user_id),
    
    # 23. Hamburger Steak with Onions and Gravy
    (user_id, 'Hamburger Steak with Onions and Gravy', 'The king of "cheap" gourmet. Juicy beef patties smothered in a rich brown gravy.', 
    '1lb ground beef, 1 egg, 1/4 cup breadcrumbs, 1/2 tsp salt, 1 onion sliced, 1 cup mushrooms, 2 tbsp flour, 1.5 cups beef broth', 
    '1. Shape beef, egg, and breadcrumbs into patties; fry in a skillet until brown. 2. Remove patties; sauté onion and mushrooms in the same pan. 3. Stir in flour, then slowly whisk in broth. 4. Return patties to pan and simmer for 15 mins.', 
    15, 20, 4, 385, 'Main Dish', 'Southern American', 'Easy', 'beef, gravy, dinner, budget', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/14595-hamburger-steak-with-onions-and-gravy-mfs-002-39046c82305c48b0a99071358b184252.jpg', True, user_id),
    
    # 24. Slow Cooker Chicken and Dumplings
    (user_id, 'Slow Cooker Chicken and Dumplings', 'Uses refrigerated biscuit dough for the fluffiest, easiest dumplings ever.', 
    '1lb chicken breasts, 2 tbsp butter, 2 cans condensed cream of chicken soup, 1 onion diced, 2 (16oz) cans refrigerated biscuit dough', 
    '1. Place chicken, butter, onion, and soup in slow cooker. Add water to cover. 2. Cook on Low for 6 hours. 3. Shred chicken. Tear biscuit dough into pieces and drop into pot. 4. Cook for 1 more hour until dough is cooked through.', 
    10, 420, 6, 495, 'Main Dish', 'American', 'Easy', 'slow-cooker, chicken, comfort-food', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8941-slow-cooker-chicken-and-dumplings-ddmfs-4x3-0131-081e626e2730456da871f76d498642a8.jpg', True, user_id),
    
    # 25. Sloppy Joes
    (user_id, 'Sloppy Joes', 'A tangy, sweet, and messy American classic that beats the canned sauce every time.', 
    '1lb ground beef, 1/4 cup onion, 1/4 cup green bell pepper, 1 tsp garlic powder, 3/4 cup ketchup, 1 tbsp brown sugar, 1 tsp mustard', 
    '1. Brown beef, onion, and pepper. Drain fat. 2. Stir in garlic powder, ketchup, sugar, and mustard. 3. Simmer for 15 minutes. Serve on toasted buns.', 
    5, 15, 4, 320, 'Main Dish', 'American', 'Easy', 'beef, sloppy-joes, kids, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/24264-sloppy-joes-ii-ddmfs-4x3-0302-572ee91807094056a0273766a2f77977.jpg', True, user_id),
    
    # 26. Marinated Grilled Shrimp
    (user_id, 'Marinated Grilled Shrimp', 'A simple lemon, garlic, and herb marinade that works on the grill or in a pan.', 
    '1lb large shrimp, 3 cloves garlic, 1/3 cup olive oil, 1/4 cup tomato sauce, 2 tbsp red wine vinegar, 1/2 tsp paprika, 1/4 tsp salt/pepper', 
    '1. Whisk all marinade ingredients together. 2. Toss shrimp in marinade and refrigerate for 30 mins. 3. Thread onto skewers and grill for 2-3 mins per side until opaque.', 
    35, 6, 4, 180, 'Main Dish', 'Mediterranean', 'Easy', 'shrimp, seafood, grilled, low-calorie', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/12708-marinated-grilled-shrimp-ddmfs-4x3-1-987-a259c742617f41589139266657c963cc.jpg', True, user_id),
    
    # 27. Awesome Egg Rolls
    (user_id, 'Awesome Egg Rolls', 'Crispy, crunchy, and better than takeout. Includes a recipe for the essential pork filling.', 
    '1lb ground pork, 1 tsp ginger, 1 clove garlic minced, 2 cups shredded cabbage, 1/2 cup shredded carrots, 2 tbsp soy sauce, 1 tsp sesame oil, 1 package egg roll wrappers', 
    '1. Sauté pork, ginger, and garlic. Add vegetables and seasonings until wilted. 2. Place 2 tbsp of filling on a wrapper; roll tightly. 3. Deep fry in 375°F oil until golden brown. Serve with sweet and sour sauce.', 
    30, 15, 12, 145, 'Appetizer', 'Chinese-Style', 'Hard', 'egg-rolls, pork, fried, asian', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/23458-awesome-egg-rolls-ddmfs-4x3-1-581-22442475475e476fb8c575086d8c83e7.jpg', True, user_id),
    
    # 28. Fresh Southern Peach Cobbler
    (user_id, 'Fresh Southern Peach Cobbler', 'The batter rises up through the peaches as it bakes, creating a soft, cake-like crust.', 
    '1/2 cup butter, 1 cup flour, 1 cup sugar, 1 tbsp baking powder, 1 cup milk, 4 cups sliced fresh peaches, 1 cup sugar (for peaches)', 
    '1. Melt butter in a 9x13 pan. 2. Mix flour, 1 cup sugar, baking powder, and milk. Pour over melted butter (do not stir!). 3. Mix peaches with remaining sugar; spoon over batter (do not stir!). 4. Bake at 375°F (190°C) for 45 mins.', 
    15, 45, 8, 388, 'Dessert', 'Southern American', 'Easy', 'peaches, cobbler, dessert, fruit', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/51535-fresh-southern-peach-cobbler-mfs-044-a9df443309194e8a87ca990713a23330.jpg', True, user_id),
    
    # 29. Baked Zucchini Fries
    (user_id, 'Baked Zucchini Fries', 'A healthy alternative to potato fries that are surprisingly crunchy.', 
    '2 zucchini sliced into strips, 1/2 cup breadcrumbs, 1/2 cup Parmesan, 1 tsp Italian seasoning, 2 eggs beaten', 
    '1. Dip zucchini strips in egg, then into a mixture of breadcrumbs and parmesan. 2. Arrange on a baking sheet. 3. Bake at 425°F (220°C) for 20 mins until crisp.', 
    10, 20, 4, 155, 'Side Dish', 'American', 'Easy', 'zucchini, healthy, side-dish, low-carb', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222350-baked-zucchini-fries-ddmfs-4x3-1-352-710893040b7e4125868c222687980277.jpg', True, user_id),
    
    # 30. Clone of a Cinnabon
    (user_id, 'Clone of a Cinnabon', 'Massive, gooey cinnamon rolls that mimic the shopping mall classic.', 
    '1 cup milk, 2 eggs, 1/3 cup butter, 4.5 cups flour, 1 tsp salt, 1/2 cup sugar, 2.5 tsp yeast, 1 cup brown sugar, 2.5 tbsp cinnamon, 1/3 cup butter, Frosting: 3oz cream cheese, 1/4 cup butter, 1.5 cups powdered sugar', 
    '1. Make dough with first 7 ingredients; let rise. 2. Roll out dough; spread with butter, brown sugar, and cinnamon. 3. Roll up and cut into rolls. 4. Bake at 400°F for 15 mins. 5. Frost while warm.', 
    30, 15, 12, 540, 'Breakfast', 'American', 'Hard', 'cinnamon-rolls, baking, sweet, breakfast', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20156-clone-of-a-cinnabon-mfs-012-351792a59a9344e4b51909787e91244e.jpg', True, user_id),
    
    # 31. Awesome Slow Cooker Pulled Pork
    (user_id, 'Awesome Slow Cooker Pulled Pork', 'Perfectly tender pork that shreds effortlessly. Great for sandwiches.', 
    '1 (4lb) pork shoulder, 1 onion, 1 cup root beer, 2 cups BBQ sauce', 
    '1. Place pork, onion, and root beer in slow cooker. 2. Cook on Low for 8-10 hours. 3. Drain liquid and shred pork. 4. Stir in BBQ sauce and serve on buns.', 
    5, 480, 10, 410, 'Main Dish', 'American', 'Easy', 'pulled-pork, bbq, slow-cooker, sandwiches', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/pulled-pork-in-a-slow-cooker-92462-4x3-3769-90604179374c435bb15f5c09e3e7f413.jpg', True, user_id),
    
    # 32. Award Winning Chili
    (user_id, 'Award Winning Chili', 'A thick, hearty chili with multiple types of beans and a deep spice profile.', 
    '1lb ground beef, 1 onion, 3 cloves garlic, 1 can kidney beans, 1 can chili beans, 1 can diced tomatoes, 2 tbsp chili powder, 1 tsp cumin', 
    '1. Brown beef with onion and garlic. 2. Add all other ingredients to a large pot. 3. Simmer for at least 1 hour. Serve with cheese and sour cream.', 
    15, 60, 6, 350, 'Main Dish', 'American', 'Easy', 'chili, beef, spicy, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/16276-award-winning-chili-mfs-024-118e7e17094042898a96e57936a79854.jpg', True, user_id),
    
    # 33. Korean Beef Bowl
    (user_id, 'Korean Beef Bowl', 'A 20-minute meal that uses ground beef to mimic the flavors of Bulgogi.', 
    '1lb ground beef, 1/3 cup brown sugar, 1/4 cup soy sauce, 1 tsp sesame oil, 3 cloves garlic, 1/2 tsp ginger, green onions, sesame seeds', 
    '1. Brown beef in a skillet. 2. Add garlic and cook 1 min. 3. Stir in soy sauce, sugar, sesame oil, and ginger. 4. Simmer 5 mins and serve over rice with onions and seeds.', 
    5, 15, 4, 335, 'Main Dish', 'Korean-Style', 'Easy', 'korean, beef, quick, rice-bowl', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/236230-korean-beef-bowl-ddmfs-3x4-0544-7729227653604f81903932e652467d5e.jpg', True, user_id),
    
    # 34. Creamy Au Gratin Potatoes
    (user_id, 'Creamy Au Gratin Potatoes', 'The ultimate holiday side dish. Thinly sliced potatoes in a rich, cheesy béchamel.', 
    '4 potatoes thinly sliced, 3 tbsp butter, 3 tbsp flour, 1.5 cups milk, 1 cup shredded Cheddar, 1/2 tsp salt', 
    '1. Melt butter; whisk in flour. Gradually add milk to create a sauce. 2. Layer potatoes in a dish. Pour sauce over each layer. 3. Sprinkle with cheese. 4. Bake at 400°F (200°C) for 1 hour until tender.', 
    20, 60, 6, 280, 'Side Dish', 'French-Style', 'Medium', 'potatoes, cheese, side-dish, holiday', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/au-gratin-potatoes-6705602-4x3-3330-0589a194954045f8a00062b9f8450f3c.jpg', True, user_id),
    
    # 35. Japanese Zucchini
    (user_id, 'Japanese Zucchini', 'The classic hibachi side dish made with soy sauce, butter, and sesame seeds.', 
    '2 tbsp butter, 1 tbsp soy sauce, 1 tsp sugar, 2 zucchini sliced, 1/2 onion sliced, 1 tbsp sesame seeds', 
    '1. Melt butter in a large skillet. 2. Add onions and zucchini; sauté for 5 mins until tender-crisp. 3. Add soy sauce, sugar, and sesame seeds. 4. Toss for 2 mins and serve.', 
    5, 10, 4, 85, 'Side Dish', 'Japanese-Style', 'Easy', 'zucchini, hibachi, asian, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222350-japanese-zucchini-ddmfs-4x3-1-352-710893040b7e4125868c222687980277.jpg', True, user_id),
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
print(f"\n✅ Successfully added 25 more recipes (total: 35 recipes)!")
