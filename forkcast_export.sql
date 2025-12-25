-- Users
INSERT INTO users (id, username, email, password_hash, full_name, bio, profile_image, created_at, updated_at) VALUES (1, 'Forkcast', 'forkcast@forkcast.com', 'scrypt:32768:8:1$bfXw6hlULY1JjrGZ$7eb9c286f17656b909d6aaeaf2983cceff99c0c10b5a82d0b2792ce374b8aca4145a3bb41cc79ce1596f45906b7baa587c5a78767b554760dd1e4ee7f935fec1', 'Forkcast Team', 'Official Forkcast recipe collection', '/static/uploads/profiles/f32020de1d904d8c8f468bf3db3cae43_main_logo.png', '2025-12-25 13:40:38.473172', '2025-12-25 14:06:05.203289');

-- Recipes
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (1, 1, 'World''s Best Lasagna', 'The most popular recipe on Allrecipes with over 20,000 reviews. A rich, meaty, multi-layered masterpiece.', '1lb sweet Italian sausage
3/4lb lean ground beef
1/2 cup minced onion
2 cloves garlic crushed
1 (28oz) can crushed tomatoes
2 (6oz) cans tomato paste
2 (6.5oz) cans canned tomato sauce
1/2 cup water
2 tbsp white sugar
1.5 tsp dried basil leaves
1/2 tsp fennel seeds
1 tsp Italian seasoning
1 tbsp salt
1/4 tsp black pepper
4 tbsp chopped fresh parsley
12 lasagna noodles
16oz ricotta cheese
1 egg
3/4lb mozzarella cheese sliced
3/4 cup grated Parmesan cheese', '1. Cook sausage, beef, onion, and garlic over medium heat until browned.
2. Stir in tomatoes, paste, sauce, and water. Season with sugar, basil, fennel, Italian seasoning, salt, pepper, and 2 tbsp parsley. Simmer 1.5 hours.
3. Boil noodles until al dente.
4. Mix ricotta, egg, and remaining parsley.
5. Layer sauce, noodles, ricotta mixture, mozzarella, and Parmesan in a 9x13 dish. Repeat.
6. Bake at 375°F (190°C) for 25 mins covered, then 25 mins uncovered.', 0, 180, 12, 690, '', '', '', 'lasagna, pasta, dinner, classic, beef', '/static/uploads/recipes/1_20251225_140510_Worlds_Best_Lasagna.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 14:05:10.827990');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (2, 1, 'Chef John''s Drunken Noodles', 'Known as Pad Kee Mao, this spicy, savory Thai street food classic is a favorite for late-night cravings.', '8oz dried rice noodles
1/4 cup oyster sauce
1/4 cup soy sauce
1 tbsp fish sauce
1 tbsp maple syrup
1 tsp sugar
2 tbsp water
2 tbsp vegetable oil
1 tsp sesame oil
1 cup sliced shallots
6 tsp sliced bird''s eye chiles
4 cloves garlic
2.5lb chicken thighs cut into strips
1lb Chinese broccoli
4 scallions
1 cup fresh Thai basil', '1. Soak noodles in hot water for 15 mins until flexible.
2. Whisk oyster sauce, soy, fish sauce, syrup, sugar, and water.
3. Sauté shallots, chiles, and garlic in oils.
4. Add chicken and sear.
5. Toss in broccoli stems, then leaves.
6. Pour in sauce and scallions; add noodles.
7. Toss for 2 mins until sauce is absorbed.
8. Stir in basil and serve.', 0, 30, 4, 1287, '', '', '', 'spicy, noodles, street food, chicken, chef john', '/static/uploads/recipes/1_20251225_140253_Chef_Johns_Drunken_Noodles.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 14:02:53.824392');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (3, 1, 'Curry Stand Chicken Tikka Masala', 'A "nuclear-orange" tikka masala that mimics the best British-Indian curry stand flavors.', '2 tbsp ghee
1 onion chopped
4 cloves garlic
1 tbsp cumin
1 tsp ginger
1 tsp cayenne
1/2 tsp cinnamon
1/4 tsp turmeric
14oz tomato sauce
1 cup heavy cream
1 tbsp sugar
2 tsp paprika
4 chicken breasts diced
1/2 tsp curry powder', '1. Sauté onion in ghee until translucent; add garlic.
2. Stir in dry spices (cumin to turmeric) and fry until fragrant.
3. Stir in tomato sauce; simmer 10 mins.
4. Mix in cream, sugar, and paprika; simmer until thickened.
5. In a separate pan, sear chicken with curry powder.
6. Transfer chicken to sauce and simmer for 30 mins.', 0, 80, 6, 474, '', '', '', 'curry, chicken, spicy, creamy, tikka masala', '/static/uploads/recipes/1_20251225_140331_Curry_Stand_Chicken_Tikka_Masala.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 14:03:31.594485');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (4, 1, 'Good Old-Fashioned Pancakes', 'Simple, fluffy, and dependable. The quintessential American breakfast.', '1.5 cups all-purpose flour
3.5 tsp baking powder
1 tsp salt
1 tbsp white sugar
1.25 cups milk
1 egg
3 tbsp butter melted', '1. Sift flour, baking powder, salt, and sugar in a large bowl.
2. Make a well in the center and pour in milk, egg, and melted butter; mix until smooth.
3. Heat a lightly oiled griddle over medium-high heat.
4. Pour scoop of batter onto the griddle; brown on both sides.', 0, 20, 8, 765, '', '', '', 'pancakes, breakfast, brunch, quick', '/static/uploads/recipes/1_20251225_140347_Good_Old-Fashioned_Pancakes.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 14:03:47.623592');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (5, 1, 'Banana Banana Bread', 'The highest-rated banana bread on the site. Using more bananas is the secret to its popularity.', '2 cups all-purpose flour
1 tsp baking soda
1/4 tsp salt
1/2 cup butter
3/4 cup brown sugar
2 eggs beaten
2.33 cups mashed overripe bananas', '1. Preheat oven to 350°F (175°C). Grease a 9x5 inch loaf pan.
2. Cream butter and sugar. Add eggs and mashed bananas.
3. Combine flour, soda, and salt; stir into banana mixture until just moistened.
4. Bake for 60 to 65 minutes.', 0, 75, 12, 1127, '', '', '', 'baking, bread, bananas, snack, sweet', '/static/uploads/recipes/1_20251225_140402_Banana_Banana_Bread.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 14:04:02.848137');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (6, 1, 'Scott Hibb''s Amazing Whisky Grilled Ribs', 'Finger-licking baby back ribs with a unique whisky-infused glaze.', '2 racks baby back pork ribs
salt/pepper
1 cup whisky
1 cup ketchup
1/2 cup brown sugar
1/4 cup vinegar
1 tbsp onion powder
1 tbsp garlic powder', '1. Season ribs; pre-cook in oven at 300°F wrapped in foil for 2 hours.
2. Combine glaze ingredients in a pan; simmer until thick.
3. Grill ribs over medium heat, basting generously with glaze for 10-15 mins until charred and sticky.', 0, 155, 4, 405, '', '', '', 'bbq, ribs, pork, grilling, whisky', '/static/uploads/recipes/1_20251225_140421_Scott_Hibbs_Amazing_Whisky_Grilled_Ribs.webp', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 14:04:21.631206');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (7, 1, 'Mom''s Chicken Pot Pie', 'The ultimate comfort food. Creamy chicken and vegetable filling in a flaky crust.', '1lb skinless chicken breast diced
1 cup sliced carrots
1 cup frozen peas
1/2 cup sliced celery
1/3 cup butter
1/3 cup onion
1/3 cup flour
1/2 tsp salt
1/4 tsp pepper
1/4 tsp celery seed
1.75 cups chicken broth
2/3 cup milk
2 (9 inch) unbaked pie crusts', '1. Boil chicken, carrots, peas, and celery for 15 mins.
2. Cook onions in butter until soft; stir in flour and seasonings.
3. Gradually add broth and milk; simmer until thick.
4. Place chicken/veg in bottom pie crust; pour sauce over.
5. Top with second crust; bake at 425°F for 30-35 mins.', 20, 35, 8, 415, 'Main Dish', 'American', 'Medium', 'comfort food, chicken, pie, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/26317-moms-chicken-pot-pie-mfs_010-02558f339178465b89a8ef153f318991.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 13:40:38.473172');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (8, 1, 'Marry Me Chicken Soup', 'A viral 2024 sensation. A creamy, sun-dried tomato and parmesan-based soup that is incredibly cozy.', '2 tbsp olive oil
1lb chicken breasts
1 onion
3 cloves garlic
1/2 cup sun-dried tomatoes
1 tsp oregano
1/2 tsp red pepper flakes
4 cups chicken broth
1/2 cup heavy cream
1/2 cup grated Parmesan
2 cups spinach', '1. Brown chicken in oil; remove and shred.
2. Sauté onion, garlic, and sun-dried tomatoes.
3. Add spices and broth; simmer 10 mins.
4. Stir in shredded chicken, cream, and parmesan.
5. Add spinach at the end until wilted.', 15, 25, 4, 380, 'Soup', 'American', 'Easy', 'viral, soup, chicken, creamy, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8711470-marry-me-chicken-soup-4x3-1-7918451842094200a747065997235222.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 13:40:38.473172');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (9, 1, 'Oven-Roasted Greek Potatoes', 'Crispy on the outside, tender on the inside, with bright lemon and oregano flavors.', '4 large potatoes peeled and wedged
1/2 cup olive oil
1/2 cup water
1 tsp dried oregano
1 tsp salt
1/4 tsp black pepper
2 cloves garlic minced
1 lemon juiced', '1. Preheat oven to 400°F (200°C).
2. Place potato wedges in a baking tin.
3. Mix olive oil, water, oregano, salt, pepper, garlic, and lemon juice; pour over potatoes.
4. Bake for 60 mins, turning once, until golden and crisp.', 10, 60, 6, 210, 'Side Dish', 'Greek', 'Easy', 'potatoes, lemon, vegan, gluten-free, mediterranean', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/95030-oven-roasted-greek-potatoes-ddmfs-3x4-0518-9125439a838541a7985338f0d84c6604.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 13:40:38.473172');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (10, 1, 'Taco Bake Casserole', 'A family-favorite weeknight meal that combines all the best parts of a taco into an easy bake.', '1lb ground beef
1 packet taco seasoning
1 (16oz) can refried beans
1 cup salsa
2 cups shredded Mexican cheese blend
1 bag corn chips
lettuce/tomato for garnish', '1. Brown beef and drain; stir in taco seasoning.
2. In a baking dish, layer refried beans, then beef, then salsa.
3. Top with a thick layer of cheese.
4. Bake at 350°F for 20 mins.
5. Serve over a bed of corn chips and top with fresh lettuce and tomato.', 10, 20, 6, 450, 'Main Dish', 'Mexican-Style', 'Easy', 'taco, casserole, beef, family, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/17131-taco-bake-mfs-103-f366e6b5413149869687483842c54f5c.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:40:38.473172', '2025-12-25 13:40:38.473172');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (11, 1, 'Baked Ziti', 'A classic cheesy pasta bake that is a staple for potlucks and family dinners.', '1lb ziti pasta
1lb ground beef
2 (26oz) jars spaghetti sauce
6oz provolone cheese sliced
1.5 cups ricotta
6oz mozzarella cheese shredded
2 tbsp grated Parmesan', '1. Boil ziti until al dente.
2. Brown beef in a pan; add sauce and simmer.
3. Mix ziti with meat sauce.
4. In a 9x13 dish, layer half of the ziti, then provolone, then ricotta. Add remaining ziti and top with mozzarella and parmesan.
5. Bake at 350°F (175°C) for 30 mins.', 15, 30, 8, 450, 'Main Dish', 'Italian', 'Easy', 'pasta, cheese, beef, comfort-food', 'https://www.allrecipes.com/thmb/9_M_X_X_j_X_P_U_o_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/11758-baked-ziti-ii-ddmfs-4x3-0382-7f329432d84749f7823521d8b671a7d6.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (12, 1, 'Best Chocolate Chip Cookies', 'Over 15,000 5-star reviews. These are soft, chewy, and perfectly balanced.', '1 cup butter softened
1 cup white sugar
1 cup brown sugar
2 eggs
2 tsp vanilla
1 tsp baking soda
2 tsp hot water
1/2 tsp salt
3 cups flour
2 cups chocolate chips', '1. Cream butter and sugars. Beat in eggs and vanilla.
2. Dissolve baking soda in hot water; add to batter with salt.
3. Stir in flour and chocolate chips.
4. Drop large spoonfuls onto ungreased pans.
5. Bake at 350°F (175°C) for 10 mins until edges are brown.', 20, 10, 24, 298, 'Dessert', 'American', 'Medium', 'cookies, chocolate, baking, sweet', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/10813-best-chocolate-chip-cookies-mfs-641561-1-be21147f07094ee7a8989b537d998782.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (13, 1, 'Awesome Slow Cooker Pot Roast', 'The definitive set-it-and-forget-it meal. The gravy develops a deep, rich flavor.', '3lb chuck roast
2 (10oz) cans condensed cream of mushroom soup
1 packet dry onion soup mix
1 cup water
4 potatoes chopped
4 carrots sliced', '1. Place roast in slow cooker.
2. Mix soup, dry soup mix, and water; pour over roast.
3. Add potatoes and carrots around the meat.
4. Cover and cook on Low for 8-10 hours.', 10, 480, 6, 520, 'Main Dish', 'American', 'Easy', 'slow-cooker, beef, roast, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/16066-awesome-slow-cooker-pot-roast-ddmfs-3x4-0472-e5658097984144e096f4b6794689626e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (14, 1, 'Apple Pie by Grandma Ople', 'A unique lattice-topped pie where a buttery caramel sauce is poured over the crust before baking.', '1 recipe pastry for a double-crust pie
1/2 cup butter
3 tbsp flour
1/4 cup water
1/2 cup white sugar
1/2 cup brown sugar
8 Granny Smith apples', '1. Melt butter, stir in flour and sugars to form a paste; add water and simmer.
2. Place sliced apples in bottom crust. Lattice the top crust.
3. Pour caramel liquid over the lattice.
4. Bake at 425°F for 15 mins, then lower to 350°F and bake 45 mins.', 30, 60, 8, 412, 'Dessert', 'American', 'Hard', 'apple-pie, baking, fruit, dessert', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/12682-apple-pie-by-grandma-ople-mfs-001-c88c7f766e014798b3769ca12f9f8c5b.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (15, 1, 'Baked Teriyaki Chicken', 'Homemade teriyaki sauce makes these thighs sticky and addictive.', '1 tbsp cornstarch
1 tbsp cold water
1/2 cup white sugar
1/2 cup soy sauce
1/4 cup cider vinegar
1 clove garlic minced
1/2 tsp ginger
12 skinless chicken thighs', '1. Mix cornstarch and water. In a small pot, combine sugar, soy sauce, vinegar, garlic, and ginger; boil until thick.
2. Place chicken in a baking dish and coat with sauce.
3. Bake at 425°F (220°C) for 30 minutes, turning once.', 15, 30, 6, 320, 'Main Dish', 'Japanese-Style', 'Easy', 'chicken, teriyaki, quick, asian', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8930-baked-teriyaki-chicken-ddmfs-4x3-1025-a134f59e66344795b9c030d95015e510.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (16, 1, 'Meatball Nirvana', 'These meatballs are light, fluffy, and tender thanks to a secret ratio of breadcrumbs and parmesan.', '1lb ground beef
1/2lb ground pork
1/2 cup breadcrumbs
1/4 cup milk
1/2 cup grated Parmesan
1 egg
1/2 cup chopped parsley
2 cloves garlic', '1. Mix all ingredients in a large bowl.
2. Roll into 2-inch balls.
3. Brown in a skillet with olive oil.
4. Finish cooking in your favorite marinara sauce for 20 mins.', 20, 25, 6, 310, 'Main Dish', 'Italian-American', 'Medium', 'meatballs, beef, dinner, pasta', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/14603-meatball-nirvana-ddmfs-1x1-1-58479e02c67645e589a66d03d3c8c5c4.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (17, 1, 'To-Die-For Blueberry Muffins', 'Huge bakery-style muffins with a sugary streusel topping.', '1.5 cups flour
3/4 cup sugar
1/2 tsp salt
2 tsp baking powder
1/3 cup oil
1 egg
1/3 cup milk
1 cup blueberries
Streusel topping: 1/2 cup sugar
1/3 cup flour
1/4 cup butter', '1. Mix dry ingredients; add egg, oil, and milk. Fold in berries.
2. Fill muffin cups to the top.
3. Top with mixed streusel (sugar, flour, butter).
4. Bake at 400°F (200°C) for 20-25 mins.', 15, 20, 12, 381, 'Breakfast', 'American', 'Easy', 'muffins, blueberry, breakfast, sweet', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/6865-to-die-for-blueberry-muffins-mfs-044-1-6d2466085a67448d8c92a2a7a40b8296.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (18, 1, 'Quinoa and Black Beans', 'A high-protein vegan staple that is excellent for meal prep.', '1 tsp oil
1 onion
3 cloves garlic
3/4 cup quinoa
1.5 cups vegetable broth
1 tsp cumin
1/4 tsp cayenne
1 (15oz) can black beans
1 cup frozen corn', '1. Sauté onion and garlic.
2. Add quinoa, broth, and spices. Bring to boil, then simmer for 20 mins.
3. Stir in beans and corn; heat through. Garnish with cilantro.', 10, 25, 4, 320, 'Healthy', 'International', 'Easy', 'vegan, quinoa, beans, healthy, lunch', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/quinoa-and-black-beans-2151125-4x3-3323-99933096057948339591404c084666f7.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (19, 1, 'Buffalo Chicken Dip', 'The ultimate party snack. Creamy, spicy, and perfect with chips or celery.', '2 cups shredded cooked chicken
1 (8oz) package cream cheese softened
1/2 cup Buffalo wing sauce
1/2 cup ranch dressing
1.5 cups shredded Monterey Jack cheese', '1. Mix chicken, cream cheese, wing sauce, ranch, and half the Jack cheese in a bowl.
2. Spread in a shallow baking dish.
3. Top with remaining cheese.
4. Bake at 350°F (175°C) for 20 mins until bubbly.', 10, 20, 10, 268, 'Appetizer', 'American', 'Easy', 'buffalo-chicken, dip, party, spicy', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/22644-buffalo-chicken-dip-mfs-031-63806c9a9d704d98939c323f49b06297.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (20, 1, 'Chantal''s New York Cheesecake', 'Rich, dense, and creamy with a simple graham cracker crust.', '1.5 cups graham cracker crumbs
2 cups sugar
1/4 cup butter melted
4 (8oz) packages cream cheese
3/4 cup milk
4 eggs
1 cup sour cream
1 tbsp vanilla
1/4 cup flour', '1. Press crumbs/butter into a springform pan.
2. Cream sugar and cream cheese until smooth.
3. Add milk, then eggs one by one. Stir in sour cream, vanilla, and flour.
4. Bake at 350°F (175°C) for 1 hour. Let cool in oven with door closed for 5 hours.', 30, 60, 12, 650, 'Dessert', 'American', 'Hard', 'cheesecake, dessert, classic, baking', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8350-chantals-new-york-cheesecake-ddmfs-4x3-2550-9c8828b6d3a9484ca781b2447950c40e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (21, 1, 'Baked Tilapia Parmesan', 'A light, crispy, and savory way to prepare white fish.', '4 tilapia fillets
1/4 cup butter softened
3 tbsp mayo
2 tbsp lemon juice
1/4 cup Parmesan
1/4 tsp dried basil
1/4 tsp onion powder', '1. Broil fillets for 2-3 mins per side.
2. Mix butter, mayo, lemon, cheese, and spices.
3. Spread mixture over fillets.
4. Broil for 2 more mins until brown and bubbly.', 10, 10, 4, 215, 'Main Dish', 'Seafood', 'Easy', 'fish, tilapia, seafood, low-carb', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8923-baked-tilapia-parmesan-ddmfs-3x4-0554-e6944062f83141f3918a0058e578330a.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (22, 1, 'Ultimate Twice-Baked Potatoes', 'Everything you love about a loaded baked potato in a neat, double-cooked shell.', '4 large russet potatoes
1/4 cup butter
1/4 cup sour cream
1/4 cup milk
1 cup shredded Cheddar
4 slices bacon cooked/crumbled
2 green onions', '1. Bake potatoes at 400°F for 1 hour.
2. Slice in half and scoop out insides.
3. Mash insides with butter, cream, milk, half the cheese, and bacon.
4. Stuff shells and top with remaining cheese.
5. Bake for 15 mins more.', 15, 75, 8, 345, 'Side Dish', 'American', 'Medium', 'potatoes, cheese, bacon, side-dish', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20647-ultimate-twice-baked-potatoes-ddmfs-3x4-0599-299f056d607e467d8f58356f9103e302.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (23, 1, 'Hamburger Steak with Onions and Gravy', 'The king of "cheap" gourmet. Juicy beef patties smothered in a rich brown gravy.', '1lb ground beef
1 egg
1/4 cup breadcrumbs
1/2 tsp salt
1 onion sliced
1 cup mushrooms
2 tbsp flour
1.5 cups beef broth', '1. Shape beef, egg, and breadcrumbs into patties; fry in a skillet until brown.
2. Remove patties; sauté onion and mushrooms in the same pan.
3. Stir in flour, then slowly whisk in broth.
4. Return patties to pan and simmer for 15 mins.', 15, 20, 4, 385, 'Main Dish', 'Southern American', 'Easy', 'beef, gravy, dinner, budget', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/14595-hamburger-steak-with-onions-and-gravy-mfs-002-39046c82305c48b0a99071358b184252.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (24, 1, 'Slow Cooker Chicken and Dumplings', 'Uses refrigerated biscuit dough for the fluffiest, easiest dumplings ever.', '1lb chicken breasts
2 tbsp butter
2 cans condensed cream of chicken soup
1 onion diced
2 (16oz) cans refrigerated biscuit dough', '1. Place chicken, butter, onion, and soup in slow cooker. Add water to cover.
2. Cook on Low for 6 hours.
3. Shred chicken. Tear biscuit dough into pieces and drop into pot.
4. Cook for 1 more hour until dough is cooked through.', 10, 420, 6, 495, 'Main Dish', 'American', 'Easy', 'slow-cooker, chicken, comfort-food', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8941-slow-cooker-chicken-and-dumplings-ddmfs-4x3-0131-081e626e2730456da871f76d498642a8.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (25, 1, 'Sloppy Joes', 'A tangy, sweet, and messy American classic that beats the canned sauce every time.', '1lb ground beef
1/4 cup onion
1/4 cup green bell pepper
1 tsp garlic powder
3/4 cup ketchup
1 tbsp brown sugar
1 tsp mustard', '1. Brown beef, onion, and pepper. Drain fat.
2. Stir in garlic powder, ketchup, sugar, and mustard.
3. Simmer for 15 minutes. Serve on toasted buns.', 5, 15, 4, 320, 'Main Dish', 'American', 'Easy', 'beef, sloppy-joes, kids, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/24264-sloppy-joes-ii-ddmfs-4x3-0302-572ee91807094056a0273766a2f77977.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (26, 1, 'Marinated Grilled Shrimp', 'A simple lemon, garlic, and herb marinade that works on the grill or in a pan.', '1lb large shrimp
3 cloves garlic
1/3 cup olive oil
1/4 cup tomato sauce
2 tbsp red wine vinegar
1/2 tsp paprika
1/4 tsp salt/pepper', '1. Whisk all marinade ingredients together.
2. Toss shrimp in marinade and refrigerate for 30 mins.
3. Thread onto skewers and grill for 2-3 mins per side until opaque.', 35, 6, 4, 180, 'Main Dish', 'Mediterranean', 'Easy', 'shrimp, seafood, grilled, low-calorie', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/12708-marinated-grilled-shrimp-ddmfs-4x3-1-987-a259c742617f41589139266657c963cc.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (27, 1, 'Awesome Egg Rolls', 'Crispy, crunchy, and better than takeout. Includes a recipe for the essential pork filling.', '1lb ground pork
1 tsp ginger
1 clove garlic minced
2 cups shredded cabbage
1/2 cup shredded carrots
2 tbsp soy sauce
1 tsp sesame oil
1 package egg roll wrappers', '1. Sauté pork, ginger, and garlic. Add vegetables and seasonings until wilted.
2. Place 2 tbsp of filling on a wrapper; roll tightly.
3. Deep fry in 375°F oil until golden brown. Serve with sweet and sour sauce.', 30, 15, 12, 145, 'Appetizer', 'Chinese-Style', 'Hard', 'egg-rolls, pork, fried, asian', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/23458-awesome-egg-rolls-ddmfs-4x3-1-581-22442475475e476fb8c575086d8c83e7.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (28, 1, 'Fresh Southern Peach Cobbler', 'The batter rises up through the peaches as it bakes, creating a soft, cake-like crust.', '1/2 cup butter
1 cup flour
1 cup sugar
1 tbsp baking powder
1 cup milk
4 cups sliced fresh peaches
1 cup sugar (for peaches)', '1. Melt butter in a 9x13 pan.
2. Mix flour, 1 cup sugar, baking powder, and milk. Pour over melted butter (do not stir!).
3. Mix peaches with remaining sugar; spoon over batter (do not stir!).
4. Bake at 375°F (190°C) for 45 mins.', 15, 45, 8, 388, 'Dessert', 'Southern American', 'Easy', 'peaches, cobbler, dessert, fruit', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/51535-fresh-southern-peach-cobbler-mfs-044-a9df443309194e8a87ca990713a23330.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (29, 1, 'Baked Zucchini Fries', 'A healthy alternative to potato fries that are surprisingly crunchy.', '2 zucchini sliced into strips
1/2 cup breadcrumbs
1/2 cup Parmesan
1 tsp Italian seasoning
2 eggs beaten', '1. Dip zucchini strips in egg, then into a mixture of breadcrumbs and parmesan.
2. Arrange on a baking sheet.
3. Bake at 425°F (220°C) for 20 mins until crisp.', 10, 20, 4, 155, 'Side Dish', 'American', 'Easy', 'zucchini, healthy, side-dish, low-carb', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222350-baked-zucchini-fries-ddmfs-4x3-1-352-710893040b7e4125868c222687980277.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (30, 1, 'Clone of a Cinnabon', 'Massive, gooey cinnamon rolls that mimic the shopping mall classic.', '1 cup milk
2 eggs
1/3 cup butter
4.5 cups flour
1 tsp salt
1/2 cup sugar
2.5 tsp yeast
1 cup brown sugar
2.5 tbsp cinnamon
1/3 cup butter
Frosting: 3oz cream cheese
1/4 cup butter
1.5 cups powdered sugar', '1. Make dough with first 7 ingredients; let rise.
2. Roll out dough; spread with butter, brown sugar, and cinnamon.
3. Roll up and cut into rolls.
4. Bake at 400°F for 15 mins.
5. Frost while warm.', 30, 15, 12, 540, 'Breakfast', 'American', 'Hard', 'cinnamon-rolls, baking, sweet, breakfast', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20156-clone-of-a-cinnabon-mfs-012-351792a59a9344e4b51909787e91244e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (31, 1, 'Awesome Slow Cooker Pulled Pork', 'Perfectly tender pork that shreds effortlessly. Great for sandwiches.', '1 (4lb) pork shoulder
1 onion
1 cup root beer
2 cups BBQ sauce', '1. Place pork, onion, and root beer in slow cooker.
2. Cook on Low for 8-10 hours.
3. Drain liquid and shred pork.
4. Stir in BBQ sauce and serve on buns.', 5, 480, 10, 410, 'Main Dish', 'American', 'Easy', 'pulled-pork, bbq, slow-cooker, sandwiches', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/pulled-pork-in-a-slow-cooker-92462-4x3-3769-90604179374c435bb15f5c09e3e7f413.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (32, 1, 'Award Winning Chili', 'A thick, hearty chili with multiple types of beans and a deep spice profile.', '1lb ground beef
1 onion
3 cloves garlic
1 can kidney beans
1 can chili beans
1 can diced tomatoes
2 tbsp chili powder
1 tsp cumin', '1. Brown beef with onion and garlic.
2. Add all other ingredients to a large pot.
3. Simmer for at least 1 hour. Serve with cheese and sour cream.', 15, 60, 6, 350, 'Main Dish', 'American', 'Easy', 'chili, beef, spicy, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/16276-award-winning-chili-mfs-024-118e7e17094042898a96e57936a79854.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (33, 1, 'Korean Beef Bowl', 'A 20-minute meal that uses ground beef to mimic the flavors of Bulgogi.', '1lb ground beef
1/3 cup brown sugar
1/4 cup soy sauce
1 tsp sesame oil
3 cloves garlic
1/2 tsp ginger
green onions
sesame seeds', '1. Brown beef in a skillet.
2. Add garlic and cook 1 min.
3. Stir in soy sauce, sugar, sesame oil, and ginger.
4. Simmer 5 mins and serve over rice with onions and seeds.', 5, 15, 4, 335, 'Main Dish', 'Korean-Style', 'Easy', 'korean, beef, quick, rice-bowl', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/236230-korean-beef-bowl-ddmfs-3x4-0544-7729227653604f81903932e652467d5e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (34, 1, 'Creamy Au Gratin Potatoes', 'The ultimate holiday side dish. Thinly sliced potatoes in a rich, cheesy béchamel.', '4 potatoes thinly sliced
3 tbsp butter
3 tbsp flour
1.5 cups milk
1 cup shredded Cheddar
1/2 tsp salt', '1. Melt butter; whisk in flour. Gradually add milk to create a sauce.
2. Layer potatoes in a dish. Pour sauce over each layer.
3. Sprinkle with cheese.
4. Bake at 400°F (200°C) for 1 hour until tender.', 20, 60, 6, 280, 'Side Dish', 'French-Style', 'Medium', 'potatoes, cheese, side-dish, holiday', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/au-gratin-potatoes-6705602-4x3-3330-0589a194954045f8a00062b9f8450f3c.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (35, 1, 'Japanese Zucchini', 'The classic hibachi side dish made with soy sauce, butter, and sesame seeds.', '2 tbsp butter
1 tbsp soy sauce
1 tsp sugar
2 zucchini sliced
1/2 onion sliced
1 tbsp sesame seeds', '1. Melt butter in a large skillet.
2. Add onions and zucchini; sauté for 5 mins until tender-crisp.
3. Add soy sauce, sugar, and sesame seeds.
4. Toss for 2 mins and serve.', 5, 10, 4, 85, 'Side Dish', 'Japanese-Style', 'Easy', 'zucchini, hibachi, asian, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222350-japanese-zucchini-ddmfs-4x3-1-352-710893040b7e4125868c222687980277.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:47:45.718501', '2025-12-25 13:47:45.718501');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (36, 1, 'Baked Ziti', 'A classic cheesy pasta bake that is a staple for potlucks and family dinners.', '1lb ziti pasta
1lb ground beef
2 (26oz) jars spaghetti sauce
6oz provolone cheese sliced
1.5 cups ricotta
6oz mozzarella cheese shredded
2 tbsp grated Parmesan', '1. Boil ziti until al dente.
2. Brown beef in a pan; add sauce and simmer.
3. Mix ziti with meat sauce.
4. In a 9x13 dish, layer half of the ziti, then provolone, then ricotta. Add remaining ziti and top with mozzarella and parmesan.
5. Bake at 350°F (175°C) for 30 mins.', 15, 30, 8, 450, 'Main Dish', 'Italian', 'Easy', 'pasta, cheese, beef, comfort-food', 'https://www.allrecipes.com/thmb/9_M_X_X_j_X_P_U_o_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/11758-baked-ziti-ii-ddmfs-4x3-0382-7f329432d84749f7823521d8b671a7d6.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (37, 1, 'Best Chocolate Chip Cookies', 'Over 15,000 5-star reviews. These are soft, chewy, and perfectly balanced.', '1 cup butter softened
1 cup white sugar
1 cup brown sugar
2 eggs
2 tsp vanilla
1 tsp baking soda
2 tsp hot water
1/2 tsp salt
3 cups flour
2 cups chocolate chips', '1. Cream butter and sugars. Beat in eggs and vanilla.
2. Dissolve baking soda in hot water; add to batter with salt.
3. Stir in flour and chocolate chips.
4. Drop large spoonfuls onto ungreased pans.
5. Bake at 350°F (175°C) for 10 mins until edges are brown.', 20, 10, 24, 298, 'Dessert', 'American', 'Medium', 'cookies, chocolate, baking, sweet', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/10813-best-chocolate-chip-cookies-mfs-641561-1-be21147f07094ee7a8989b537d998782.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (38, 1, 'Awesome Slow Cooker Pot Roast', 'The definitive set-it-and-forget-it meal. The gravy develops a deep, rich flavor.', '3lb chuck roast
2 (10oz) cans condensed cream of mushroom soup
1 packet dry onion soup mix
1 cup water
4 potatoes chopped
4 carrots sliced', '1. Place roast in slow cooker.
2. Mix soup, dry soup mix, and water; pour over roast.
3. Add potatoes and carrots around the meat.
4. Cover and cook on Low for 8-10 hours.', 10, 480, 6, 520, 'Main Dish', 'American', 'Easy', 'slow-cooker, beef, roast, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/16066-awesome-slow-cooker-pot-roast-ddmfs-3x4-0472-e5658097984144e096f4b6794689626e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (39, 1, 'Apple Pie by Grandma Ople', 'A unique lattice-topped pie where a buttery caramel sauce is poured over the crust before baking.', '1 recipe pastry for a double-crust pie
1/2 cup butter
3 tbsp flour
1/4 cup water
1/2 cup white sugar
1/2 cup brown sugar
8 Granny Smith apples', '1. Melt butter, stir in flour and sugars to form a paste; add water and simmer.
2. Place sliced apples in bottom crust. Lattice the top crust.
3. Pour caramel liquid over the lattice.
4. Bake at 425°F for 15 mins, then lower to 350°F and bake 45 mins.', 30, 60, 8, 412, 'Dessert', 'American', 'Hard', 'apple-pie, baking, fruit, dessert', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/12682-apple-pie-by-grandma-ople-mfs-001-c88c7f766e014798b3769ca12f9f8c5b.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (40, 1, 'Baked Teriyaki Chicken', 'Homemade teriyaki sauce makes these thighs sticky and addictive.', '1 tbsp cornstarch
1 tbsp cold water
1/2 cup white sugar
1/2 cup soy sauce
1/4 cup cider vinegar
1 clove garlic minced
1/2 tsp ginger
12 skinless chicken thighs', '1. Mix cornstarch and water. In a small pot, combine sugar, soy sauce, vinegar, garlic, and ginger; boil until thick.
2. Place chicken in a baking dish and coat with sauce.
3. Bake at 425°F (220°C) for 30 minutes, turning once.', 15, 30, 6, 320, 'Main Dish', 'Japanese-Style', 'Easy', 'chicken, teriyaki, quick, asian', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8930-baked-teriyaki-chicken-ddmfs-4x3-1025-a134f59e66344795b9c030d95015e510.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (41, 1, 'Meatball Nirvana', 'These meatballs are light, fluffy, and tender thanks to a secret ratio of breadcrumbs and parmesan.', '1lb ground beef
1/2lb ground pork
1/2 cup breadcrumbs
1/4 cup milk
1/2 cup grated Parmesan
1 egg
1/2 cup chopped parsley
2 cloves garlic', '1. Mix all ingredients in a large bowl.
2. Roll into 2-inch balls.
3. Brown in a skillet with olive oil.
4. Finish cooking in your favorite marinara sauce for 20 mins.', 20, 25, 6, 310, 'Main Dish', 'Italian-American', 'Medium', 'meatballs, beef, dinner, pasta', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/14603-meatball-nirvana-ddmfs-1x1-1-58479e02c67645e589a66d03d3c8c5c4.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (42, 1, 'To-Die-For Blueberry Muffins', 'Huge bakery-style muffins with a sugary streusel topping.', '1.5 cups flour
3/4 cup sugar
1/2 tsp salt
2 tsp baking powder
1/3 cup oil
1 egg
1/3 cup milk
1 cup blueberries
Streusel topping: 1/2 cup sugar
1/3 cup flour
1/4 cup butter', '1. Mix dry ingredients; add egg, oil, and milk. Fold in berries.
2. Fill muffin cups to the top.
3. Top with mixed streusel (sugar, flour, butter).
4. Bake at 400°F (200°C) for 20-25 mins.', 15, 20, 12, 381, 'Breakfast', 'American', 'Easy', 'muffins, blueberry, breakfast, sweet', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/6865-to-die-for-blueberry-muffins-mfs-044-1-6d2466085a67448d8c92a2a7a40b8296.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (43, 1, 'Quinoa and Black Beans', 'A high-protein vegan staple that is excellent for meal prep.', '1 tsp oil
1 onion
3 cloves garlic
3/4 cup quinoa
1.5 cups vegetable broth
1 tsp cumin
1/4 tsp cayenne
1 (15oz) can black beans
1 cup frozen corn', '1. Sauté onion and garlic.
2. Add quinoa, broth, and spices. Bring to boil, then simmer for 20 mins.
3. Stir in beans and corn; heat through. Garnish with cilantro.', 10, 25, 4, 320, 'Healthy', 'International', 'Easy', 'vegan, quinoa, beans, healthy, lunch', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/quinoa-and-black-beans-2151125-4x3-3323-99933096057948339591404c084666f7.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (44, 1, 'Buffalo Chicken Dip', 'The ultimate party snack. Creamy, spicy, and perfect with chips or celery.', '2 cups shredded cooked chicken
1 (8oz) package cream cheese softened
1/2 cup Buffalo wing sauce
1/2 cup ranch dressing
1.5 cups shredded Monterey Jack cheese', '1. Mix chicken, cream cheese, wing sauce, ranch, and half the Jack cheese in a bowl.
2. Spread in a shallow baking dish.
3. Top with remaining cheese.
4. Bake at 350°F (175°C) for 20 mins until bubbly.', 10, 20, 10, 268, 'Appetizer', 'American', 'Easy', 'buffalo-chicken, dip, party, spicy', 'https://www.allrecipes.com/thmb/X9_4_v_4_w_X_y_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/22644-buffalo-chicken-dip-mfs-031-63806c9a9d704d98939c323f49b06297.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (45, 1, 'Chantal''s New York Cheesecake', 'Rich, dense, and creamy with a simple graham cracker crust.', '1.5 cups graham cracker crumbs
2 cups sugar
1/4 cup butter melted
4 (8oz) packages cream cheese
3/4 cup milk
4 eggs
1 cup sour cream
1 tbsp vanilla
1/4 cup flour', '1. Press crumbs/butter into a springform pan.
2. Cream sugar and cream cheese until smooth.
3. Add milk, then eggs one by one. Stir in sour cream, vanilla, and flour.
4. Bake at 350°F (175°C) for 1 hour. Let cool in oven with door closed for 5 hours.', 30, 60, 12, 650, 'Dessert', 'American', 'Hard', 'cheesecake, dessert, classic, baking', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8350-chantals-new-york-cheesecake-ddmfs-4x3-2550-9c8828b6d3a9484ca781b2447950c40e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (46, 1, 'Baked Tilapia Parmesan', 'A light, crispy, and savory way to prepare white fish.', '4 tilapia fillets
1/4 cup butter softened
3 tbsp mayo
2 tbsp lemon juice
1/4 cup Parmesan
1/4 tsp dried basil
1/4 tsp onion powder', '1. Broil fillets for 2-3 mins per side.
2. Mix butter, mayo, lemon, cheese, and spices.
3. Spread mixture over fillets.
4. Broil for 2 more mins until brown and bubbly.', 10, 10, 4, 215, 'Main Dish', 'Seafood', 'Easy', 'fish, tilapia, seafood, low-carb', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8923-baked-tilapia-parmesan-ddmfs-3x4-0554-e6944062f83141f3918a0058e578330a.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (47, 1, 'Ultimate Twice-Baked Potatoes', 'Everything you love about a loaded baked potato in a neat, double-cooked shell.', '4 large russet potatoes
1/4 cup butter
1/4 cup sour cream
1/4 cup milk
1 cup shredded Cheddar
4 slices bacon cooked/crumbled
2 green onions', '1. Bake potatoes at 400°F for 1 hour.
2. Slice in half and scoop out insides.
3. Mash insides with butter, cream, milk, half the cheese, and bacon.
4. Stuff shells and top with remaining cheese.
5. Bake for 15 mins more.', 15, 75, 8, 345, 'Side Dish', 'American', 'Medium', 'potatoes, cheese, bacon, side-dish', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20647-ultimate-twice-baked-potatoes-ddmfs-3x4-0599-299f056d607e467d8f58356f9103e302.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (48, 1, 'Hamburger Steak with Onions and Gravy', 'The king of "cheap" gourmet. Juicy beef patties smothered in a rich brown gravy.', '1lb ground beef
1 egg
1/4 cup breadcrumbs
1/2 tsp salt
1 onion sliced
1 cup mushrooms
2 tbsp flour
1.5 cups beef broth', '1. Shape beef, egg, and breadcrumbs into patties; fry in a skillet until brown.
2. Remove patties; sauté onion and mushrooms in the same pan.
3. Stir in flour, then slowly whisk in broth.
4. Return patties to pan and simmer for 15 mins.', 15, 20, 4, 385, 'Main Dish', 'Southern American', 'Easy', 'beef, gravy, dinner, budget', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/14595-hamburger-steak-with-onions-and-gravy-mfs-002-39046c82305c48b0a99071358b184252.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (49, 1, 'Slow Cooker Chicken and Dumplings', 'Uses refrigerated biscuit dough for the fluffiest, easiest dumplings ever.', '1lb chicken breasts
2 tbsp butter
2 cans condensed cream of chicken soup
1 onion diced
2 (16oz) cans refrigerated biscuit dough', '1. Place chicken, butter, onion, and soup in slow cooker. Add water to cover.
2. Cook on Low for 6 hours.
3. Shred chicken. Tear biscuit dough into pieces and drop into pot.
4. Cook for 1 more hour until dough is cooked through.', 10, 420, 6, 495, 'Main Dish', 'American', 'Easy', 'slow-cooker, chicken, comfort-food', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/8941-slow-cooker-chicken-and-dumplings-ddmfs-4x3-0131-081e626e2730456da871f76d498642a8.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (50, 1, 'Sloppy Joes', 'A tangy, sweet, and messy American classic that beats the canned sauce every time.', '1lb ground beef
1/4 cup onion
1/4 cup green bell pepper
1 tsp garlic powder
3/4 cup ketchup
1 tbsp brown sugar
1 tsp mustard', '1. Brown beef, onion, and pepper. Drain fat.
2. Stir in garlic powder, ketchup, sugar, and mustard.
3. Simmer for 15 minutes. Serve on toasted buns.', 5, 15, 4, 320, 'Main Dish', 'American', 'Easy', 'beef, sloppy-joes, kids, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/24264-sloppy-joes-ii-ddmfs-4x3-0302-572ee91807094056a0273766a2f77977.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (51, 1, 'Marinated Grilled Shrimp', 'A simple lemon, garlic, and herb marinade that works on the grill or in a pan.', '1lb large shrimp
3 cloves garlic
1/3 cup olive oil
1/4 cup tomato sauce
2 tbsp red wine vinegar
1/2 tsp paprika
1/4 tsp salt/pepper', '1. Whisk all marinade ingredients together.
2. Toss shrimp in marinade and refrigerate for 30 mins.
3. Thread onto skewers and grill for 2-3 mins per side until opaque.', 35, 6, 4, 180, 'Main Dish', 'Mediterranean', 'Easy', 'shrimp, seafood, grilled, low-calorie', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/12708-marinated-grilled-shrimp-ddmfs-4x3-1-987-a259c742617f41589139266657c963cc.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (52, 1, 'Awesome Egg Rolls', 'Crispy, crunchy, and better than takeout. Includes a recipe for the essential pork filling.', '1lb ground pork
1 tsp ginger
1 clove garlic minced
2 cups shredded cabbage
1/2 cup shredded carrots
2 tbsp soy sauce
1 tsp sesame oil
1 package egg roll wrappers', '1. Sauté pork, ginger, and garlic. Add vegetables and seasonings until wilted.
2. Place 2 tbsp of filling on a wrapper; roll tightly.
3. Deep fry in 375°F oil until golden brown. Serve with sweet and sour sauce.', 30, 15, 12, 145, 'Appetizer', 'Chinese-Style', 'Hard', 'egg-rolls, pork, fried, asian', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/23458-awesome-egg-rolls-ddmfs-4x3-1-581-22442475475e476fb8c575086d8c83e7.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (53, 1, 'Fresh Southern Peach Cobbler', 'The batter rises up through the peaches as it bakes, creating a soft, cake-like crust.', '1/2 cup butter
1 cup flour
1 cup sugar
1 tbsp baking powder
1 cup milk
4 cups sliced fresh peaches
1 cup sugar (for peaches)', '1. Melt butter in a 9x13 pan.
2. Mix flour, 1 cup sugar, baking powder, and milk. Pour over melted butter (do not stir!).
3. Mix peaches with remaining sugar; spoon over batter (do not stir!).
4. Bake at 375°F (190°C) for 45 mins.', 15, 45, 8, 388, 'Dessert', 'Southern American', 'Easy', 'peaches, cobbler, dessert, fruit', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/51535-fresh-southern-peach-cobbler-mfs-044-a9df443309194e8a87ca990713a23330.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (54, 1, 'Baked Zucchini Fries', 'A healthy alternative to potato fries that are surprisingly crunchy.', '2 zucchini sliced into strips
1/2 cup breadcrumbs
1/2 cup Parmesan
1 tsp Italian seasoning
2 eggs beaten', '1. Dip zucchini strips in egg, then into a mixture of breadcrumbs and parmesan.
2. Arrange on a baking sheet.
3. Bake at 425°F (220°C) for 20 mins until crisp.', 10, 20, 4, 155, 'Side Dish', 'American', 'Easy', 'zucchini, healthy, side-dish, low-carb', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222350-baked-zucchini-fries-ddmfs-4x3-1-352-710893040b7e4125868c222687980277.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (55, 1, 'Clone of a Cinnabon', 'Massive, gooey cinnamon rolls that mimic the shopping mall classic.', '1 cup milk
2 eggs
1/3 cup butter
4.5 cups flour
1 tsp salt
1/2 cup sugar
2.5 tsp yeast
1 cup brown sugar
2.5 tbsp cinnamon
1/3 cup butter
Frosting: 3oz cream cheese
1/4 cup butter
1.5 cups powdered sugar', '1. Make dough with first 7 ingredients; let rise.
2. Roll out dough; spread with butter, brown sugar, and cinnamon.
3. Roll up and cut into rolls.
4. Bake at 400°F for 15 mins.
5. Frost while warm.', 30, 15, 12, 540, 'Breakfast', 'American', 'Hard', 'cinnamon-rolls, baking, sweet, breakfast', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/20156-clone-of-a-cinnabon-mfs-012-351792a59a9344e4b51909787e91244e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (56, 1, 'Awesome Slow Cooker Pulled Pork', 'Perfectly tender pork that shreds effortlessly. Great for sandwiches.', '1 (4lb) pork shoulder
1 onion
1 cup root beer
2 cups BBQ sauce', '1. Place pork, onion, and root beer in slow cooker.
2. Cook on Low for 8-10 hours.
3. Drain liquid and shred pork.
4. Stir in BBQ sauce and serve on buns.', 5, 480, 10, 410, 'Main Dish', 'American', 'Easy', 'pulled-pork, bbq, slow-cooker, sandwiches', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/pulled-pork-in-a-slow-cooker-92462-4x3-3769-90604179374c435bb15f5c09e3e7f413.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (57, 1, 'Award Winning Chili', 'A thick, hearty chili with multiple types of beans and a deep spice profile.', '1lb ground beef
1 onion
3 cloves garlic
1 can kidney beans
1 can chili beans
1 can diced tomatoes
2 tbsp chili powder
1 tsp cumin', '1. Brown beef with onion and garlic.
2. Add all other ingredients to a large pot.
3. Simmer for at least 1 hour. Serve with cheese and sour cream.', 15, 60, 6, 350, 'Main Dish', 'American', 'Easy', 'chili, beef, spicy, dinner', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/16276-award-winning-chili-mfs-024-118e7e17094042898a96e57936a79854.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (58, 1, 'Korean Beef Bowl', 'A 20-minute meal that uses ground beef to mimic the flavors of Bulgogi.', '1lb ground beef
1/3 cup brown sugar
1/4 cup soy sauce
1 tsp sesame oil
3 cloves garlic
1/2 tsp ginger
green onions
sesame seeds', '1. Brown beef in a skillet.
2. Add garlic and cook 1 min.
3. Stir in soy sauce, sugar, sesame oil, and ginger.
4. Simmer 5 mins and serve over rice with onions and seeds.', 5, 15, 4, 335, 'Main Dish', 'Korean-Style', 'Easy', 'korean, beef, quick, rice-bowl', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/236230-korean-beef-bowl-ddmfs-3x4-0544-7729227653604f81903932e652467d5e.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (59, 1, 'Creamy Au Gratin Potatoes', 'The ultimate holiday side dish. Thinly sliced potatoes in a rich, cheesy béchamel.', '4 potatoes thinly sliced
3 tbsp butter
3 tbsp flour
1.5 cups milk
1 cup shredded Cheddar
1/2 tsp salt', '1. Melt butter; whisk in flour. Gradually add milk to create a sauce.
2. Layer potatoes in a dish. Pour sauce over each layer.
3. Sprinkle with cheese.
4. Bake at 400°F (200°C) for 1 hour until tender.', 20, 60, 6, 280, 'Side Dish', 'French-Style', 'Medium', 'potatoes, cheese, side-dish, holiday', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/au-gratin-potatoes-6705602-4x3-3330-0589a194954045f8a00062b9f8450f3c.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');
INSERT INTO recipes (id, user_id, title, description, ingredients, instructions, prep_time, cook_time, servings, calories_per_serving, category, cuisine, difficulty, tags, image_url, is_public, is_favorite, forked_from_id, original_author_id, created_at, updated_at) VALUES (60, 1, 'Japanese Zucchini', 'The classic hibachi side dish made with soy sauce, butter, and sesame seeds.', '2 tbsp butter
1 tbsp soy sauce
1 tsp sugar
2 zucchini sliced
1/2 onion sliced
1 tbsp sesame seeds', '1. Melt butter in a large skillet.
2. Add onions and zucchini; sauté for 5 mins until tender-crisp.
3. Add soy sauce, sugar, and sesame seeds.
4. Toss for 2 mins and serve.', 5, 10, 4, 85, 'Side Dish', 'Japanese-Style', 'Easy', 'zucchini, hibachi, asian, quick', 'https://www.allrecipes.com/thmb/v_p7Y5V5V0X9Y9y1_8_4_0_0_=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/222350-japanese-zucchini-ddmfs-4x3-1-352-710893040b7e4125868c222687980277.jpg', TRUE, FALSE, NULL, 1, '2025-12-25 13:48:53.788053', '2025-12-25 13:48:53.788053');

-- Reset sequences
SELECT setval('users_id_seq', 1, true);
SELECT setval('recipes_id_seq', 60, true);
