"""CLI for meal prep planning.
"""
import argparse
import datetime
import os
from dotenv import load_dotenv
import mealprep

load_dotenv()
MEALIE_URL = os.getenv('MEALIE_URL')
MEALIE_TOKEN = os.getenv('MEALIE_TOKEN')
OUTPUT_DIR = './'


def main():
    """CLI for making meal plans.
    """
    parser = argparse.ArgumentParser(prog = 'Meal Prep Tool')
    parser.add_argument('step', choices=['plan', 'list'])
    parser.add_argument('--dates', type=datetime.date.fromisoformat, nargs=2)
    args = parser.parse_args()

    # Load
    recipes, calendar, _ = mealprep.mealie.load_all(MEALIE_URL, MEALIE_TOKEN)

    if 'dates' in args:
        start = args.dates[0]
        end = args.dates[1]
    else:
        today = datetime.date.today()
        start = today + datetime.timedelta(days=(7 - today.weekday()))
        end = start + datetime.timedelta(weeks=4, days=-1)

    if args.step == 'plan':
        print('Making Meal Plan')
        calendar.fill(recipes, start, end)
    elif args.step == 'list':
        print('Making Shopping List')
        shopping = mealprep.txt.TxtShoppingLists()
        guide = mealprep.txt.TxtPrepGuide()

        shopping.fill_list(calendar, start, end)
        shopping.write(OUTPUT_DIR + '/shopping-lists/')

        guide.add_calendar(calendar, start, end)
        guide.write(OUTPUT_DIR + '/guide.txt')


if __name__ == '__main__':
    main()
