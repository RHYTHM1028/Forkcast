"""
Ingredient Parser - Parse and aggregate ingredients from recipes.

This module handles:
    - Parsing ingredient strings from recipes
    - Extracting quantities, units, and ingredient names
    - Aggregating identical ingredients
    - Categorizing ingredients
"""

import re
from fractions import Fraction
from typing import Dict, List, Tuple, Optional


# Common ingredient categories
INGREDIENT_CATEGORIES = {
    'Vegetables': [
        'tomato', 'onion', 'garlic', 'pepper', 'carrot', 'celery', 'lettuce', 'spinach',
        'broccoli', 'cauliflower', 'cabbage', 'zucchini', 'cucumber', 'potato', 'sweet potato',
        'mushroom', 'avocado', 'bean', 'pea', 'corn', 'kale', 'arugula', 'chard', 'eggplant',
        'squash', 'pumpkin', 'radish', 'beet', 'turnip', 'parsnip', 'leek', 'shallot'
    ],
    'Fruits': [
        'apple', 'banana', 'orange', 'lemon', 'lime', 'strawberry', 'blueberry', 'raspberry',
        'grape', 'mango', 'pineapple', 'watermelon', 'melon', 'peach', 'pear', 'plum',
        'cherry', 'kiwi', 'papaya', 'coconut', 'fig', 'date', 'apricot', 'cranberry'
    ],
    'Meat & Seafood': [
        'chicken', 'beef', 'pork', 'lamb', 'turkey', 'duck', 'fish', 'salmon', 'tuna',
        'shrimp', 'prawn', 'crab', 'lobster', 'scallop', 'mussel', 'clam', 'bacon',
        'sausage', 'ham', 'steak', 'ground beef', 'ground turkey', 'ground pork'
    ],
    'Dairy & Eggs': [
        'milk', 'cream', 'butter', 'cheese', 'yogurt', 'sour cream', 'egg', 'mozzarella',
        'cheddar', 'parmesan', 'feta', 'goat cheese', 'ricotta', 'cottage cheese',
        'cream cheese', 'buttermilk', 'heavy cream', 'half and half', 'whipping cream'
    ],
    'Grains & Pasta': [
        'rice', 'pasta', 'noodle', 'bread', 'flour', 'oat', 'quinoa', 'couscous', 'barley',
        'bulgur', 'wheat', 'rye', 'cornmeal', 'tortilla', 'pita', 'bagel', 'roll',
        'spaghetti', 'fettuccine', 'penne', 'macaroni', 'lasagna', 'ravioli'
    ],
    'Pantry': [
        'oil', 'olive oil', 'vegetable oil', 'coconut oil', 'vinegar', 'balsamic', 'soy sauce',
        'worcestershire', 'mustard', 'ketchup', 'mayonnaise', 'honey', 'sugar', 'salt',
        'pepper', 'stock', 'broth', 'tomato sauce', 'tomato paste', 'can', 'canned'
    ],
    'Herbs & Spices': [
        'basil', 'oregano', 'thyme', 'rosemary', 'parsley', 'cilantro', 'mint', 'dill',
        'sage', 'bay leaf', 'cumin', 'paprika', 'chili', 'cayenne', 'turmeric', 'cinnamon',
        'nutmeg', 'ginger', 'curry', 'coriander', 'cardamom', 'clove', 'vanilla'
    ],
    'Baking': [
        'flour', 'sugar', 'brown sugar', 'powdered sugar', 'baking powder', 'baking soda',
        'yeast', 'vanilla extract', 'almond extract', 'cocoa powder', 'chocolate chip',
        'chocolate', 'cornstarch', 'gelatin', 'molasses', 'syrup'
    ],
    'Nuts & Seeds': [
        'almond', 'walnut', 'pecan', 'cashew', 'peanut', 'pistachio', 'hazelnut', 'macadamia',
        'sunflower seed', 'pumpkin seed', 'sesame seed', 'chia seed', 'flax seed', 'pine nut'
    ],
    'Other': []
}

# Common units and their conversions to base units
UNIT_CONVERSIONS = {
    # Volume
    'cup': 1.0, 'cups': 1.0, 'c': 1.0,
    'tablespoon': 1/16, 'tablespoons': 1/16, 'tbsp': 1/16, 'tb': 1/16,
    'teaspoon': 1/48, 'teaspoons': 1/48, 'tsp': 1/48, 't': 1/48,
    'fluid ounce': 1/8, 'fluid ounces': 1/8, 'fl oz': 1/8, 'floz': 1/8,
    'pint': 2.0, 'pints': 2.0, 'pt': 2.0,
    'quart': 4.0, 'quarts': 4.0, 'qt': 4.0,
    'gallon': 16.0, 'gallons': 16.0, 'gal': 16.0,
    'liter': 4.22675, 'liters': 4.22675, 'l': 4.22675,
    'milliliter': 0.00422675, 'milliliters': 0.00422675, 'ml': 0.00422675,
    
    # Weight
    'pound': 1.0, 'pounds': 1.0, 'lb': 1.0, 'lbs': 1.0,
    'ounce': 1/16, 'ounces': 1/16, 'oz': 1/16,
    'gram': 0.00220462, 'grams': 0.00220462, 'g': 0.00220462,
    'kilogram': 2.20462, 'kilograms': 2.20462, 'kg': 2.20462,
    
    # Count
    'piece': 1.0, 'pieces': 1.0, 'pc': 1.0,
    'whole': 1.0, 'item': 1.0, 'items': 1.0,
    'clove': 1.0, 'cloves': 1.0,
    'slice': 1.0, 'slices': 1.0,
    'can': 1.0, 'cans': 1.0,
    'package': 1.0, 'packages': 1.0, 'pkg': 1.0,
    'bunch': 1.0, 'bunches': 1.0,
}


def parse_fraction(text: str) -> float:
    """Parse a fraction or mixed number (e.g., '1 1/2', '3/4') to float."""
    text = text.strip()
    if not text:
        return 0.0
    
    # Handle mixed numbers (e.g., "1 1/2")
    if ' ' in text:
        parts = text.split()
        if len(parts) == 2:
            try:
                whole = float(parts[0])
                frac = float(Fraction(parts[1]))
                return whole + frac
            except:
                pass
    
    # Handle simple fractions (e.g., "3/4")
    if '/' in text:
        try:
            return float(Fraction(text))
        except:
            pass
    
    # Handle decimals and whole numbers
    try:
        return float(text)
    except:
        return 0.0


# Size descriptors with approximate gram estimates (for calorie calculation)
SIZE_DESCRIPTORS = {
    'small': 0.5, 'medium': 1.0, 'large': 1.5, 'extra-large': 2.0, 'xl': 2.0,
    'whole': 1.0, 'half': 0.5, 'quarter': 0.25
}

# All recognized units including size descriptors
ALL_UNITS = list(UNIT_CONVERSIONS.keys()) + list(SIZE_DESCRIPTORS.keys())


def parse_ingredient(line: str) -> Dict[str, any]:
    """
    Parse a single ingredient line using multiple pattern strategies.
    
    Handles:
        - "2 cups flour"
        - "1/2 teaspoon salt"  
        - "1 1/2 cups sugar"
        - "2-3 medium tomatoes" (ranges)
        - "100g chicken" (direct weight)
        - "3 large eggs"
    
    Returns:
        dict with keys: quantity, unit, name, name_for_category, original
    """
    line = line.strip()
    if not line:
        return None
    
    original = line
    text = line.lower()
    
    quantity = 1.0
    unit = ''
    name = ''
    
    # Build unit pattern for regex
    unit_pattern = '|'.join(sorted(ALL_UNITS, key=len, reverse=True))
    
    # Pattern 1: Direct weight/volume attached to number (e.g., "100g", "250ml")
    direct_match = re.match(r'^(\d+\.?\d*)\s*(g|gram|grams|kg|ml|l|oz|lb|lbs)\b\s*(.*)$', text, re.IGNORECASE)
    if direct_match:
        quantity = float(direct_match.group(1))
        unit = direct_match.group(2).lower()
        name = direct_match.group(3).strip()
        if name.startswith('of '):
            name = name[3:]
    
    # Pattern 2: Range with unit (e.g., "2-3 cups flour")
    elif re.match(r'^\d+\.?\d*\s*-\s*\d+\.?\d*', text):
        range_match = re.match(r'^(\d+\.?\d*)\s*-\s*(\d+\.?\d*)\s*(' + unit_pattern + r')?\s*(.*)$', text, re.IGNORECASE)
        if range_match:
            # Use average of range
            low = float(range_match.group(1))
            high = float(range_match.group(2))
            quantity = (low + high) / 2
            unit = (range_match.group(3) or '').lower()
            name = (range_match.group(4) or '').strip()
    
    # Pattern 3: Mixed number with unit (e.g., "1 1/2 cups flour")
    elif re.match(r'^\d+\s+\d+/\d+', text):
        mixed_match = re.match(r'^(\d+)\s+(\d+/\d+)\s*(' + unit_pattern + r')?\s*(.*)$', text, re.IGNORECASE)
        if mixed_match:
            whole = float(mixed_match.group(1))
            frac = float(Fraction(mixed_match.group(2)))
            quantity = whole + frac
            unit = (mixed_match.group(3) or '').lower()
            name = (mixed_match.group(4) or '').strip()
    
    # Pattern 4: Fraction with unit (e.g., "1/2 cup flour")
    elif re.match(r'^\d+/\d+', text):
        frac_match = re.match(r'^(\d+/\d+)\s*(' + unit_pattern + r')?\s*(.*)$', text, re.IGNORECASE)
        if frac_match:
            quantity = float(Fraction(frac_match.group(1)))
            unit = (frac_match.group(2) or '').lower()
            name = (frac_match.group(3) or '').strip()
    
    # Pattern 5: Number with unit (e.g., "2 cups flour", "3 large eggs")
    elif re.match(r'^\d+\.?\d*', text):
        num_match = re.match(r'^(\d+\.?\d*)\s*(' + unit_pattern + r')?\s*(.*)$', text, re.IGNORECASE)
        if num_match:
            quantity = float(num_match.group(1))
            unit = (num_match.group(2) or '').lower()
            name = (num_match.group(3) or '').strip()
    
    # Pattern 6: No quantity (e.g., "salt to taste", "fresh basil")
    else:
        name = text
    
    # Clean up the ingredient name
    if not name:
        name = text
    
    # Remove "of" prefix (e.g., "of flour" -> "flour")
    if name.startswith('of '):
        name = name[3:]
    
    # Remove trailing commas and everything after (recipe notes)
    if ',' in name:
        name = name.split(',')[0].strip()
    
    # Remove parenthetical notes
    name = re.sub(r'\([^)]*\)', '', name).strip()
    
    # Clean ingredient name for categorization (remove descriptors)
    name_for_category = re.sub(
        r'\b(fresh|dried|chopped|diced|minced|sliced|crushed|grated|ground|whole|frozen|canned|organic|raw|cooked|boneless|skinless)\b', 
        '', name.lower()
    ).strip()
    
    # Preserve original case for display
    # Try to find the name portion in the original line for proper casing
    name_start = original.lower().find(name.split()[0] if name.split() else name)
    if name_start >= 0:
        name = original[name_start:name_start + len(name)]
    
    return {
        'quantity': quantity,
        'unit': unit,
        'name': name.strip(),
        'name_for_category': name_for_category,
        'original': original
    }


def categorize_ingredient(ingredient_name: str) -> str:
    """Categorize an ingredient based on its name."""
    ingredient_name = ingredient_name.lower()
    
    for category, keywords in INGREDIENT_CATEGORIES.items():
        if category == 'Other':
            continue
        for keyword in keywords:
            if keyword in ingredient_name:
                return category
    
    return 'Other'


def normalize_unit(unit: str) -> Tuple[str, str]:
    """
    Normalize a unit and return (normalized_unit, unit_type).
    unit_type can be 'volume', 'weight', 'count', or 'other'
    """
    unit = unit.lower().strip()
    
    # Volume units
    volume_units = ['cup', 'cups', 'c', 'tablespoon', 'tablespoons', 'tbsp', 'tb',
                   'teaspoon', 'teaspoons', 'tsp', 't', 'fluid ounce', 'fluid ounces',
                   'fl oz', 'floz', 'pint', 'pints', 'pt', 'quart', 'quarts', 'qt',
                   'gallon', 'gallons', 'gal', 'liter', 'liters', 'l', 'milliliter',
                   'milliliters', 'ml']
    
    # Weight units
    weight_units = ['pound', 'pounds', 'lb', 'lbs', 'ounce', 'ounces', 'oz',
                   'gram', 'grams', 'g', 'kilogram', 'kilograms', 'kg']
    
    # Count units
    count_units = ['piece', 'pieces', 'pc', 'whole', 'item', 'items', 'clove', 'cloves',
                  'slice', 'slices', 'can', 'cans', 'package', 'packages', 'pkg',
                  'bunch', 'bunches']
    
    if unit in volume_units:
        return (unit, 'volume')
    elif unit in weight_units:
        return (unit, 'weight')
    elif unit in count_units:
        return (unit, 'count')
    else:
        return (unit, 'other')


def can_aggregate(item1: Dict, item2: Dict) -> bool:
    """Check if two ingredient items can be aggregated."""
    # Must have same base ingredient name (case insensitive)
    if item1['name'].lower() != item2['name'].lower():
        return False
    
    # Get unit types
    _, type1 = normalize_unit(item1['unit'])
    _, type2 = normalize_unit(item2['unit'])
    
    # Can aggregate if:
    # 1. Both have no units
    # 2. Both have same unit type (volume, weight, or count)
    if not item1['unit'] and not item2['unit']:
        return True
    
    if type1 == type2 and type1 != 'other':
        return True
    
    return False


def aggregate_ingredients(ingredients: List[Dict]) -> List[Dict]:
    """
    Aggregate identical ingredients by combining quantities.
    
    Args:
        ingredients: List of parsed ingredient dicts
        
    Returns:
        List of aggregated ingredient dicts
    """
    aggregated = {}
    
    for ing in ingredients:
        if not ing:
            continue
        
        # Create a key for aggregation (lowercase name + unit type)
        _, unit_type = normalize_unit(ing['unit'])
        key = f"{ing['name'].lower()}_{unit_type}"
        
        if key in aggregated:
            # Check if we can aggregate
            if can_aggregate(aggregated[key], ing):
                # Try to convert to common unit
                unit1 = ing['unit'].lower()
                unit2 = aggregated[key]['unit'].lower()
                
                if unit1 in UNIT_CONVERSIONS and unit2 in UNIT_CONVERSIONS:
                    # Convert both to base unit and add
                    base1 = ing['quantity'] * UNIT_CONVERSIONS[unit1]
                    base2 = aggregated[key]['quantity'] * UNIT_CONVERSIONS[unit2]
                    total_base = base1 + base2
                    
                    # Use the more common unit (the one already aggregated)
                    aggregated[key]['quantity'] = total_base / UNIT_CONVERSIONS[unit2]
                else:
                    # Can't convert, just add quantities with note
                    aggregated[key]['quantity'] += ing['quantity']
        else:
            # First occurrence of this ingredient
            aggregated[key] = ing.copy()
            aggregated[key]['category'] = categorize_ingredient(ing['name_for_category'])
    
    return list(aggregated.values())


def format_quantity(quantity: float) -> str:
    """Format a quantity as a nice string (convert to fraction if appropriate)."""
    # Handle whole numbers
    if quantity == int(quantity):
        return str(int(quantity))
    
    # Try to convert to fraction for common values
    frac = Fraction(quantity).limit_denominator(16)
    
    # If fraction is simpler than decimal, use it
    if abs(float(frac) - quantity) < 0.01:
        if frac.numerator > frac.denominator:
            # Mixed number
            whole = frac.numerator // frac.denominator
            remainder = frac.numerator % frac.denominator
            if remainder == 0:
                return str(whole)
            return f"{whole} {remainder}/{frac.denominator}"
        else:
            return f"{frac.numerator}/{frac.denominator}"
    
    # Otherwise use decimal
    return f"{quantity:.2f}".rstrip('0').rstrip('.')


# Unit to grams conversion (approximate) - for calorie calculations
UNIT_TO_GRAMS = {
    # Volume
    'cup': 240, 'cups': 240, 'c': 240,
    'tablespoon': 15, 'tablespoons': 15, 'tbsp': 15, 'tb': 15,
    'teaspoon': 5, 'teaspoons': 5, 'tsp': 5, 't': 5,
    'fluid ounce': 30, 'fluid ounces': 30, 'fl oz': 30, 'floz': 30,
    'pint': 480, 'pints': 480, 'pt': 480,
    'quart': 960, 'quarts': 960, 'qt': 960,
    'gallon': 3840, 'gallons': 3840, 'gal': 3840,
    'liter': 1000, 'liters': 1000, 'l': 1000,
    'milliliter': 1, 'milliliters': 1, 'ml': 1,
    
    # Weight
    'pound': 454, 'pounds': 454, 'lb': 454, 'lbs': 454,
    'ounce': 28, 'ounces': 28, 'oz': 28,
    'gram': 1, 'grams': 1, 'g': 1,
    'kilogram': 1000, 'kilograms': 1000, 'kg': 1000,
    
    # Count (approximate estimates)
    'piece': 50, 'pieces': 50, 'pc': 50,
    'whole': 100, 'item': 50, 'items': 50,
    'clove': 5, 'cloves': 5,
    'slice': 30, 'slices': 30,
    'can': 400, 'cans': 400,
    'package': 250, 'packages': 250, 'pkg': 250,
    'bunch': 100, 'bunches': 100,
    
    # Size descriptors
    'small': 50, 'medium': 100, 'large': 150, 'extra-large': 200, 'xl': 200
}


def estimate_grams(parsed_ingredient: Dict) -> int:
    """
    Estimate grams for a parsed ingredient (useful for calorie calculations).
    
    Args:
        parsed_ingredient: Dict from parse_ingredient()
        
    Returns:
        Estimated grams as integer
    """
    if not parsed_ingredient:
        return 100  # Default
    
    quantity = parsed_ingredient.get('quantity', 1.0)
    unit = parsed_ingredient.get('unit', '').lower()
    
    # Direct weight units - easy conversion
    if unit in ['g', 'gram', 'grams']:
        return int(quantity)
    if unit in ['kg', 'kilogram', 'kilograms']:
        return int(quantity * 1000)
    if unit in ['oz', 'ounce', 'ounces']:
        return int(quantity * 28)
    if unit in ['lb', 'lbs', 'pound', 'pounds']:
        return int(quantity * 454)
    
    # Get unit multiplier
    if unit and unit in UNIT_TO_GRAMS:
        grams = quantity * UNIT_TO_GRAMS[unit]
    elif quantity > 0 and quantity != 1:
        # No unit, assume 100g per item
        grams = quantity * 100
    else:
        grams = 100  # Default
    
    # Cap at reasonable amounts
    grams = min(grams, 2000)
    grams = max(grams, 5)
    
    return int(grams)


def extract_food_name(parsed_ingredient: Dict) -> str:
    """
    Extract clean food name for API lookups (e.g., USDA FoodData).
    
    Args:
        parsed_ingredient: Dict from parse_ingredient()
        
    Returns:
        Clean food name string
    """
    if not parsed_ingredient:
        return ''
    
    name = parsed_ingredient.get('name_for_category', parsed_ingredient.get('name', ''))
    
    # Additional cleaning for API lookups
    name = re.sub(r'\b(fresh|dried|frozen|canned|chopped|diced|minced|sliced|grated|shredded|organic|raw|cooked)\b', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name
