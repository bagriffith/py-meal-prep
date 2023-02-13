"""Manage shopping lists.
"""
import datetime


class ShoppingLists:
    """Manages a collection of shopping lists.

    Args:
        bulk (str, optional): Name of the bulk list, if being used.
        prep (str, optional): Name of the frozen prep list, if being used.
        format (str, optional): Valid format string for a week integer
    """
    def __init__(self, **kwargs):
        self.bulk = kwargs.get('bulk', 'Bulk Items List')
        self.start_list(self.bulk)

        self.prep = kwargs.get('prep', 'Prep List')
        self.start_list(self.prep)

        self.name_format = kwargs.get('format', 'Week {} List')

    def add_to_list(self, list_name, ingredient):
        """Add one ingredient to a shopping list.

        Should be overwritten by subclass.

        Args:
            list_name (str): Name of the list to add the ingredient to
            ingredient (str): THe ingredient
        """
        _ = list_name, ingredient

    def new_list(self, list_name):
        """Creates a new list assuming the list doesn't already exist.

        Should be overwritten by subclass.

        Args:
            list_name (str): Name of the list to create
        """
        _ = list_name

    def clear_list(self, list_name):
        """Clears a list.

        Should be overwritten by subclass.

        Args:
            list_name (str): Name of the list to clear
        """
        _ = list_name

    def list_exists(self, list_name):
        """Checks is a list exist.

        Should be overwritten by subclass.

        Args:
            list_name (str): Name of the list to check

        Returns:
            bool: If the list exists
        """
        _ = list_name
        return False

    def start_list(self, list_name):
        """Initialize the list.

        Make sure the a list of the name given exists and is clear.

        Args:
            list_name (str): Name of the list to initialize
        """
        if self.list_exists(list_name):
            self.clear_list(list_name)
        else:
            self.new_list(list_name)

    def add_recipe(self, week_list, recipe):
        """Add all of the ingredients from a recipe to the correct list.

        Args:
            week (int): Week number
            recipe (Recipe): Recipe
        """
        bulk = self.bulk if self.bulk is not None else week_list

        if recipe.prepped and self.prep is not None:
            week_list = self.prep
            bulk = week_list

        for ing in recipe.not_bulk:
            self.add_to_list(week_list, ing)

        for ing in recipe.bulk:
            self.add_to_list(bulk, ing)

    def fill_list(self, calendar, start, end):
        """Add recipes from the calendar over a specified time range.

        Args:
            calendar (MealCalendar): Calendar to grab recipes from
            start (datetime.date): The first day to grad a recipe for
            end (datetime.date): The last day to grad a recipe for
        """
        start_dow = (start.weekday() + 1) % 7
        epoch = start - datetime.timedelta(days=start_dow)

        for week in range((end - epoch).days//7 + 1):
            list_name = self.name_format.format(week+1)
            self.start_list(list_name)

            first = epoch + datetime.timedelta(weeks=week)
            last = first + datetime.timedelta(weeks=1)
            meals = calendar.get_range(first, last)
            for date, meal in meals:
                if (start <= date) and (date <= end):
                    for recipe in meal:
                        self.add_recipe(list_name, recipe)
