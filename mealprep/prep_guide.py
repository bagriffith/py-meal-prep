"""Make lists so prepping is easier.
"""
import datetime


class PrepGuide:
    """A tool to make meal prepping easier.

    Args:
        prep (bool): Make a list of ingredients for frozen meal prep
        first_week (bool): Make a list for first week ingredients
        bulk (bool): Make a list of bulk bought ingredients
    """
    def __init__(self, prep=True, first_week=True, bulk=True):
        self.first_week = dict() if first_week else None
        self.prep = dict() if prep else None
        self.bulk = dict() if bulk else None

    def add_items(self, prep_list, week, recipe_name, ingredients):
        """Add one item to the specified list.

        Args:
            prep_list (dict): The dict for week lists to add the ingredients
            week (int): Week number
            ingredients (list(str)): List of ingredients to add.
        """
        if len(ingredients) > 0:
            if week not in prep_list:
                prep_list[week] = list()

            prep_list[week].append((recipe_name, ingredients))

    def add_recipe(self, recipe, week):
        """Add a new recipe to the guide.

        Args:
            recipe (mealprep.Recipe): Recipe to add.
            week (int): Week to add it to.
        """
        if (self.prep is not None) and recipe.prepped:
            self.add_items(self.prep, week, recipe.name, recipe.ingredients)
        elif (self.first_week is not None) and (week == 0):
            self.add_items(self.first_week, week, recipe.name, recipe.bulk + recipe.not_bulk)
        elif self.bulk is not None:
            self.add_items(self.bulk, week, recipe.name, recipe.bulk)

    def add_calendar(self, calendar, start, end):
        """Add recipes from the calendar over a specified time range.

        Args:
            calendar (MealCalendar): Calendar to grab recipes from
            start (datetime.date): The first day to grad a recipe for
            end (datetime.date): The last day to grad a recipe for
        """
        start_dow = (start.weekday() + 1) % 7
        epoch = start - datetime.timedelta(days=start_dow)

        for week in range((end - epoch).days//7 + 1):
            first = epoch + datetime.timedelta(weeks=week)
            last = first + datetime.timedelta(weeks=1)
            meals = calendar.get_range(first, last)
            for date, meal in meals:
                if (start <= date) and (date <= end):
                    for recipe in meal:
                        self.add_recipe(recipe, week)
