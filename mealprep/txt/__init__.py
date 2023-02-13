"""Implementation of the mealprep objects for ascii text files.

This handles a text shopping list collection and the meal prepping guide. This
could also include a recipe manager in the future.
"""
import pathlib
import textwrap
from unidecode import unidecode
import mealprep


class TxtShoppingLists(mealprep.ShoppingLists):
    """Manages Mealie shopping lists.

    Args:
        Arguments from ShoppingLists
    """
    def __init__(self, **kwargs):
        self.lists = dict()
        super().__init__(**kwargs)

    def add_to_list(self, list_name, ingredient):
        """Add one ingredient to a shopping list.

        Args:
            list_name (str): Name of the list to add the ingredient to
            ingredient (str): THe ingredient
        """
        self.lists[list_name].append(ingredient)

    def new_list(self, list_name):
        """Creates a new list assuming the list doesn't already exist.

        Args:
            list_name (str): Name of the list to create
        """
        self.lists[list_name] = list()

    def clear_list(self, list_name):
        """Clears a list.

        Args:
            list_name (str): Name of the list to clear
        """
        self.lists[list_name] = list()

    def list_exists(self, list_name):
        """Checks is a list exist.

        Args:
            list_name (str): Name of the list to check

        Returns:
            bool: If the list exists
        """
        return list_name in self.lists

    def write(self, output_dir):
        """Writes the lists to text files.

        Args:
            output_dir (path): Directory to write the files into.
        """
        output_dir = pathlib.Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for name, ingredients in self.lists.items():
            posix_name = ''.join([c for c in name.replace(' ', '_')
                                    if c.isalnum() or c in ['.', '_', '-']])
            list_path = output_dir / (posix_name + '.txt')
            self.write_list(list_path, ingredients)

    def write_list(self, filename, ingredients):
        """Writes a list of ingredients to the filename given.

        Args:
            filename (path): Output text file path.
            ingredients (list(str)): List of ingredients
        """
        with open(filename, 'w', encoding='ascii') as file:
            file.writelines([unidecode(line) + '\n' for line in ingredients])


class TxtPrepGuide(mealprep.PrepGuide):
    """Implementation of Prep Guide as a text file.
    """
    def write(self, output):
        """Write a text file of the Prep Guide.

        Args:
            output (path): The output text file path.
        """
        text = []

        prep_lists = [(self.bulk, 'Bulk'),
                      (self.first_week, 'First Week'),
                      (self.prep, 'Frozen Prep')]

        for prep_list, name in prep_lists:
            if prep_list is None:
                continue

            if len(prep_list) == 0:
                continue

            text.append(f'===== {name} =====\n')
            for week, recipes in prep_list.items():
                text.append(f'Week {week+1}:\n')
                for recipe_name, ingredients in recipes:
                    wrapped = textwrap.wrap(recipe_name+':', width=60,
                                            initial_indent=' '*1,
                                            subsequent_indent=' '*5)
                    text.extend([x+'\n' for x in wrapped])
                    for i in ingredients:
                        i = unidecode(i)
                        wrapped = textwrap.wrap(f'- {i}', width=60,
                                                initial_indent=' '*2,
                                                subsequent_indent=' '*5)
                        text.extend([x+'\n' for x in wrapped])
                    text.append('\n')
                text.append('\n')
            # text.append('\n')
        with open(output, 'w', encoding='ascii') as file:
            file.writelines(text)
