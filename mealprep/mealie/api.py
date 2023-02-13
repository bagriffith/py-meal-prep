"""A wrapper for Mealie API calls.

If someone implements an python package for the mealie beta api, similar to
how mealieapi is for the alpha version, this should be removed and replaced
with calls to that package. This does no parsing other than converting the
json returned to a json object. See the Mealie api docs for what the response
should contain
"""
import os
import json
import requests

TIMEOUT = 60


class Mealie:
    """Make calls to the Mealie API.

    Args:
        mealie_url (str): The base url to the mealie server. e.g. https:yourmealie.com
        api_token (str): Mealie api token for this service.
    """
    def __init__(self, mealie_url, api_token):
        if url is None:
            raise ValueError()
        self.url = str(mealie_url) # TODO, make this some url object or check its format

        self._headers = {'user-agent': 'mealpreper/0.0.1',
                         'Authorization': 'Bearer ' + str(api_token),
                         'accept-language': 'en-US,en'}

    def search_recipe(self, page=1, tags=None, categories=None):
        """Search for recipes with provided tags and categories

        Args:
            page (int): Result page number
            tags (list(str)): List of tags to require
            categories (list(str)): List of categories to choose from.
        Returns:
            json: JSON response from Mealie
        """
        params = {'page': page}
        if tags is not None:
            params['tags'] = list(tags)
        if categories is not None:
            params['categories'] = list(categories)

        search_url = self.url + '/api/recipes'

        response = requests.get(search_url, headers=self._headers, params=params, timeout=TIMEOUT)
        return json.loads(response.text)

    def get_recipe(self, slug):
        """Get one recipe from its slug.

        Args:
            slug (str): slug from url for the recipe.
        Returns:
            json: JSON response from Mealie
        """
        search_url = self.url + '/api/recipes/' + slug

        response = requests.get(search_url, headers=self._headers, timeout=TIMEOUT)
        return json.loads(response.text)

    def add_recipe_to_plan(self, date, slug):
        """Add one recipe to the meal plan on a given day.

        Args:
            date (datetime.date): The day to plan the meal
            slug (str): slug from url for the recipe.
        Returns:
            json: JSON response from Mealie
        """
        data = {'date': str(date),
                'entryType': 'dinner',
                'recipeId': self.get_recipe(slug)['id']}
        add_meal_url = self.url + '/api/groups/mealplans'
        response = requests.post(add_meal_url, headers=self._headers, json=data, timeout=TIMEOUT)
        return json.loads(response.text)

    def get_planned_meals(self, start_date, end_date, page=1):
        """Add one recipe to the meal plan on a given day.

        Args:
            start_date (datetime.date): First day to grab
            end_date (datetime.date): Last day to grab
            page (int): Result page number
        Returns:
            json: JSON response from Mealie
        """
        params = {'start_date': str(start_date),
                  'end_date': str(end_date),
                  'page': page}
        get_meals_url = self.url + '/api/groups/mealplans'

        response = requests.get(get_meals_url, headers=self._headers,
                                params=params, timeout=TIMEOUT)
        return json.loads(response.text)

    def new_shopping_list(self, name):
        """Create a new shopping list with the name given.

        Args:
            name (str): New shopping list name
        Returns:
            json: JSON response from Mealie
        """
        raise NotImplementedError('Mealie Shopping Lists not finished')
        data = {'name': name}
        add_list_url = self.url + '/api/groups/shopping/lists'

        response = requests.post(add_list_url, headers=self._headers, json=data, timeout=TIMEOUT)
        return json.loads(response.text)

    def add_to_shopping_list(self, list_name, ingredient):
        """Add the ingredient to a shopping list.

        Args:
            list_name (str): Shopping list name
            ingredient (str): The ingredient to add
        Returns:
            json: JSON response from Mealie
        """
        raise NotImplementedError('Mealie Shopping Lists not finished')
        data = {'shoppingListID': list_name,
                'note': ingredient}
        add_list_url = self.url + '/api/groups/shopping/items'

        response = requests.post(add_list_url, headers=self._headers, json=data, timeout=TIMEOUT)
        return json.loads(response.text)

    def get_shopping_list(self, list_name):
        """Get the ingredients list from one list.

        Args:
            list_name (str): Shopping list name
        Returns:
            json: JSON response from Mealie
        """
        raise NotImplementedError('Mealie Shopping Lists not finished')
        get_meals_url = self.url + '/api/groups/shopping/lists/' + list_name

        response = requests.get(get_meals_url, headers=self._headers, timeout=TIMEOUT)
        return json.loads(response.text)


if __name__ == '__main__':
    # Testing.
    url = os.getenv('MEALIE_URL')
    token = os.getenv('MEALIE_TOKEN')
    m = Mealie(url, token)

    r = m.search_recipe(tags=['slow-cooker'])
    print(json.dumps(r, indent=2))
    print('\n\n\n')
    for meal in r['items']:
        print(meal['name'])
        print(json.dumps(meal, indent=2))
        print('\n\n\n')
