"""Module to interface with meal scheduling.

TODO:
 * Create an iterator to give meal, week from MealCalendar
"""
import datetime
import pkg_resources
import yaml


DEFAULT_RULES_YAML = pkg_resources.resource_string('mealprep', 'rules.yaml')


class MealCalendar:
    """General class to track planned meals.

    The class is designed to be inherited for specific implantation. Any service
    that can store a list of recipe identifiers for upcoming days can be used.
    """
    def add_recipe(self, date, recipe):
        """Add a new recipe to be planned for the given date.

        This adds an additional recipe, and does not remove anything already
        scheduled. This needs to be reimplemented by the subclass.

        Args:
            date (datetime.date): The date to grab recipes for.
            recipe (list(mealie.Recipe)): A list of recipe objects for the meals
                planned on the date given.
        """
        _ = date, recipe

    def get_recipe(self, date):
        """Retrieves all planned recipes for the given date.

        This needs to be reimplemented by the subclass.

        Args:
            date (datetime.date): The date to grab recipes for.

        Returns:
            list(Recipe): List of all recipes planned for the date.
        """
        _ = date
        return []

    def get_range(self, start, end):
        """Retrieves recipes for all days in the range.

        Args:
            start (datetime.date): The first day to retrieve.
            end (datetime.date): The final day to retrieve.

        Returns:
            list(date, list(Recipe)): A tuple of the date and list of recipes
            planned for all days with recipes in the range.
        """
        all_recipes = []

        for day in range((end-start).days + 1):
            date = start + datetime.timedelta(days=day)
            recipes = self.get_recipe(date)
            if len(recipes) > 0:
                all_recipes.append((date, self.get_recipe(date)))

        return all_recipes

    def fill(self, recipes, start, end, rules_yaml=None):
        """Create a filled calendar according to rules for each day.

        Args:
            recipes (RecipeManager): List to grab recipes from.
            start (datetime.date)
            end (datetime.date)
        """
        # Load the default parameters and yaml file here
        searches = [None]*7  # Mealie search for day. With days of week as rows
        rules_yaml = rules_yaml if rules_yaml is not None else DEFAULT_RULES_YAML
        for dow, rules in yaml.safe_load(rules_yaml).items():
            searches[dow] = rules
        # searches[0] = {'include':{'tags': ['Slow Cooker'], 'categories': ['Dinner']}}

        weeks = (end - start).days//7 + 1

        # epoch is the  Sunday before or on start
        start_dow = (start.weekday() + 1) % 7
        epoch = start - datetime.timedelta(days=start_dow)

        # Make Calendar
        for dow in range(7):
            search_params = searches[dow]
            if search_params is None:
                continue

            for i, recipe in enumerate(recipes.get_n_recipes(search_params, weeks)):
                date = epoch + datetime.timedelta(days=(7*i + dow))
                if (date >= start) and (date <= end):
                    self.add_recipe(date, recipe)
