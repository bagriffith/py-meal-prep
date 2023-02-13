"""Recipe management generic classes.

Todo:
    * Implement function to identify ingredients that can be bought in bulk.
"""
import random
import math


class Recipe:
    """A container for one recipe.

    This method stores the ingredients and source if provided. It also stores
    if the recipe can be prepped and will pull out all bulk ingredients for
    a separate shopping list.

    Args:
        name (str): Name of the recipe.
        ingredients (list[str]): Ingredients, each as strings.
        prepped (bool): Can this recipe be prepped and frozen.
        source (str, optional): Url or id to get back to the source of the
            recipe in the manager.

    Attributes:
        ingredients (list[str]): Ingredients, each as strings.
        prepped (bool): Can this recipe be prepped and frozen.
        source (str, optional): Url or id to get back to the source of the
            recipe in the manager.
    """
    def __init__(self, name, ingredients, prepped, source=None):
        self.name = name
        self.ingredients = list(ingredients)
        self.prepped = bool(prepped)
        self.source = source

    @property
    def buyable(self):
        """List of items not excluded from shopping lists.

        This is a very simple way to see if an ingredient is something I have
        stocked in my pantry. There are better NLP approaches, but this one only
        took a couple minutes to create.

        Returns:
            list(str): List of ingredients that aren't pantry items.
        """
        # TODO There should be caching of this search
        excluded = {'pepper', 'butter', 'flour', 'parmesan', 'garlic powder',
                    'salt', 'water', 'oil', 'soy sauce',
                    'white rice', 'grain rice', 'mayo', 'garlic',
                    'peanut butter', 'lemon juice', 'lime juice',
                    'chicken breast', 'chicken thigh', 'ramen', 'pasta',
                    'mustard', 'vinegar', 'milk', 'cornstarch',
                    'red pepper flakes', 'honey', 'hoisin sauce',
                    'curry powder', 'cooking spray'}
        mask = [not any(x in i.lower() for x in excluded) for i in self.ingredients]
        return [i for m, i in zip(mask, self.ingredients) if m]

    @property
    def bulk(self):
        """list[str]: Returns a list of only bulk buyable ingredients.
        """
        included = {' can ', ' cans ', 'canned', 'frozen', 'broth', 'bread crumbs',
                    'soup mix', ' jar ', 'picante', ' corn ', 'coconut milk'
                    'soup', 'croutons', 'tomato sauce', 'cooked chicken',
                    'marinara sauce'}
        mask = [any(x in i.lower() for x in included) for i in self.buyable]
        return [i for m, i in zip(mask, self.buyable) if m]

    @property
    def not_bulk(self):
        """list[str]: Returns a list of everything but bulk buyable ingredients.
        """
        excluded = {' can ', 'canned', 'frozen', 'broth', 'bread crumbs',
                    'soup mix', ' jar ', 'picante', ' corn ', 'coconut milk'}
        mask = [not any(x in i.lower() for x in excluded) for i in self.buyable]
        return [i for m, i in zip(mask, self.buyable) if m]


class RecipeManager:
    """A base class for retrieving Recipes from a database.

    This is intended to be inherited to handle specific recipe management
    services. Those classes should implement the __init__ and search_recipe
    functions.
    """
    def get_n_recipes(self, query, number):
        """Retrieves a specific number of recipes matching query.

        This searches the database to grab indexes for all recipes matching
        query. If there are more recipes found than are needed, it returns
        a subset. If there are fewer, the set is repeated in random order
        until n are chosen.

        Args:
            query (dict): Dictionary of parameters to pass to the search. What
                to include will depend on the specific implementation.
            number (int > 0): Number of recipes in the list returned.

        Returns:
            list[Recipe]: Length number list of Recipes matching query

        Raises:
            ValueError: If number is less than 1.
            KeyError: If query does not return at least one recipe.
        """
        if number < 1:
            raise ValueError('At least one recipe must be requested.')

        all_recipes = self.all_matching(query)
        n_found = len(all_recipes)
        if n_found < 1:
            raise KeyError('Recipe Query was empty')

        chosen_recipes = []
        repeats = math.ceil(number / n_found)
        for i in range(repeats):
            # Choose all needed recipes, up to the length of the set
            n_in_set = min(n_found, number - i*n_found)
            chosen_set = random.sample(all_recipes, n_in_set)
            chosen_recipes.extend(chosen_set)

        assert len(chosen_recipes) == number

        return [self.get_recipe(r) for r in chosen_recipes]

    def get_recipe(self, index):
        """Retrieve a Recipe for the index provided.

        Args:
            index: Any type needed. This will uniquely identify one element in
                the database. This is to be implemented by the subclass.

        Returns:
            Recipe

        Raises:
            KeyError: If a recipe for index cannot be found.
        """
        _ = index
        return Recipe('', [], False)

    def all_matching(self, query):
        """Retrieve keys for all recipes matching query.

        Args:
            query (dict): Dictionary of parameters to pass to the search. What
                to include will depend on the specific implementation.

        Returns:
            index: Any type needed. This will uniquely identify one element in
                the database. This is to be implemented by the subclass. The
                implementation of get_recipe must be able to handle this.
        """
        _ = query
        return list()
