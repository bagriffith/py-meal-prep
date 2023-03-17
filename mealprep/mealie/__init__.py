"""Implementation of the mealprep objects for mealie.
"""
from unidecode import unidecode
import mealprep
from mealprep.mealie.api import Mealie

PAGE_LIMIT = 50


class MealieRecipeManager(mealprep.RecipeManager):
    """Implementation of the RecipeManager for Mealie beta API.

    Args:
        mealie_api (Mealie): Mealie API object to query the server.

    Attributes:
        api (Mealie): Mealie API object to query the server.
    """
    def __init__(self, mealie_api):
        self.api = mealie_api
        super().__init__()

    def all_matching(self, query):
        """Retrieve keys for all recipes matching query.

        Args:
            query (dict): Dictionary of search parameters. This should include
            'include' and 'exclude' which reference dictionaries of recipe
            attributes that either the recipe must or must not have.

        Returns:
            index list[str]: A list of recipe slugs.
        """
        include = {'tags': [], 'categories': []}
        exclude = {'tags': [], 'categories': []}

        include.update(dict(query.get('include', dict())))
        exclude.update(dict(query.get('exclude', dict())))
        exclude['tags'].extend(['exempt', 'on-hand'])

        categories = include['categories'].copy()
        include['categories'] = list()
        tags = include['tags'].copy()
        include['tags'] = list()


        recipe_keys = []
        for page in range(PAGE_LIMIT):
            response = self.api.search_recipe(page, tags, categories)
            for item in response['items']:
                # Apply filter
                include_match = []
                exclude_match = []
                for tag_sent, tag_rec in [('tags', 'tags'), ('categories', 'recipeCategory')]:
                    labels = [x['slug'] for x in item[tag_rec]]
                    include_match.extend([i in labels for i in include[tag_sent]])
                    exclude_match.extend([i in labels for i in exclude[tag_sent]])

                if all(include_match) and not any(exclude_match):
                    recipe_keys.append(item['slug'])
            if response['total_pages'] <= page + 1:
                break
        else:
            raise RuntimeWarning('Hit page limit: ', page)

        return recipe_keys

    def get_recipe(self, index):
        """Retrieve a Recipe for the index provided.

        Args:
            index (str): Slug for recipe

        Returns:
            Recipe

        Raises:
            KeyError: If a recipe for index cannot be found.
        """
        response = self.api.get_recipe(index)

        if 'detail' in response:
            raise KeyError('Recipe not in database.')
        if response['slug'] != index:
            raise KeyError('Recipe not in database.')

        return json_to_recipe(response)


class MealieCalendar(mealprep.MealCalendar):
    """Interface with the Mealie Meal Plan service.

    Args:
        mealie_api (Mealie): Mealie API object to query the server.

    Attributes:
        api (Mealie): Mealie API object to query the server.
    """
    def __init__(self, mealie_api):
        self.api = mealie_api
        super().__init__()

    def add_recipe(self, date, recipe):
        """Adds a new recipe to the Mealie Meal Plan on date.

        Args:
            date (datetime.date): The date to grab recipes for.
            recipe (list(mealie.Recipe)): A list of recipe objects for the
                meals planned on the date given. All recipes added to the
                calendar must be from a Mealie RecipeManager.
        """
        if self.api.get_recipe(recipe.source)['name'] == recipe.name:
            self.api.add_recipe_to_plan(date, recipe.source)
        else:
            # In the future, this could add the new recipe to Mealie.
            raise RuntimeError('Meal not in mealie.')

    def get_recipe(self, date):
        """Retrieves all planned recipes for the given date.

        Args:
            date (datetime.date): The date to grab recipes for.

        Returns:
            list(Recipe): List of all recipes planned for the date.
        """
        recipes = []

        for page in range(PAGE_LIMIT):
            response = self.api.get_planned_meals(date, date, page=page)
            for item in response['items']:
                if item['recipe'] is None:
                    continue

                slug = item['recipe']['slug']
                recipes.append(json_to_recipe(self.api.get_recipe(slug)))
            if response['total_pages'] <= page + 1:
                break
        else:
            raise RuntimeWarning('Hit page limit')

        return recipes


class MealieShoppingLists(mealprep.ShoppingLists):
    """Manages Mealie shopping lists.

    Args:
        mealie_api (Mealie): Mealie API object to query the server.
        Arguments from ShoppingLists
    """
    def __init__(self, mealie_api, **kwargs):
        self.api = mealie_api
        super().__init__(**kwargs)

    def add_to_list(self, list_name, ingredient):
        """Add one ingredient to a shopping list.

        Args:
            list_name (str): Name of the list to add the ingredient to
            ingredient (str): THe ingredient
        """
        self.api.add_to_shopping_list(list_name, ingredient)

    def new_list(self, list_name):
        """Creates a new list assuming the list doesn't already exist.

        Args:
            list_name (str): Name of the list to create
        """
        self.api.add_shopping_list(list_name)

    def clear_list(self, list_name):
        """Clears a list.

        Args:
            list_name (str): Name of the list to clear
        """
        raise NotImplementedError('Mealie Shopping Lists not finished')
        # TODO

    def list_exists(self, list_name):
        """Checks is a list exist.

        Args:
            list_name (str): Name of the list to check

        Returns:
            bool: If the list exists
        """
        response = self.api.get_shopping_list(list_name)
        return response['name'] == list_name


def load_all(url, token):
    """Load all 3 Mealie classes.

    Args:
        url (str): The base url to the mealie server. e.g. https:yourmealie.com
        token (str): Mealie api token for this service.
    """
    api = Mealie(url, token)
    # return MealieRecipeManager(api), MealieCalendar(api), MealieShoppingLists(api)
    return MealieRecipeManager(api), MealieCalendar(api), None


def ing_to_str(ing):
    """Convert a Mealie JSON ingredient to a string.

    Args:
        ing (json): The ingredient to format.
    """
    quantity = f"{ing['quantity']}" if ing['quantity'] != 1 else ''

    if ing['disableAmount']:
        return unidecode(quantity + f"{ing['note']}")
    else:
        return unidecode(quantity + f"{ing['unit']} {ing['food']} ({ing['note']})")


def json_to_recipe(data):
    """Convert a mealie JSON reponse to a mealprep.Recipe object.
    """
    name = data['name']
    ingredients = [ing_to_str(i) for i in data['recipeIngredient']]
    prep = 'freezable' in [x['slug'] for x in data['tags']]
    slug = data['slug']
    return mealprep.Recipe(name, ingredients, prep, source=slug)
