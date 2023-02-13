# Python Meal Prep Tools

I've been looking for a tool works with my preferred meal prepping workflow. I
couldn't find one, so I wrote my own. I needed the tool to be able to

* Select a meal for each day according to rules (e.g. slow cooker on Monday)
* Create a shopping list for each week
* Separate out meals that can be prepped and frozen in their own list
* Separate out all shelf stable items, so I can buy them all at once
* Make a cheat sheet, so I can tell which meal each item on the list belongs to

This is the result of that. I tried to make it so that it would be easy to
change the service that manages recipes, stores the planned recipes, holds
the shopping lists, or displays the meal prep guide. I only implemented one
version of each so far. I use Mealie for recipe and calendar management and
text files for the shopping list and guide.

## Usage
Install this package with pip. Make a `.env` file with `MEALIE_URL` and
`MEALIE_TOKEN` defined. To create the meal plan between some START and END date
written in YYYY-MM-DD form, run

```bash
python -m mealprep plan --dates START END
```

Once completed, make and adjustments in the Mealie web interface. Then to make
the shopping lists and prep guide, run

```bash
python -m mealprep list --dates START END
```

## Future Work

### Additional Integrations

I only implemented what I intend to immediately use. Some ideas for future
additions could be implementing all the classes for the Paprika app. A meal
prep calendar could be kept in Google Calendars. Shopping Lists could be added
for Google Keep, Google Docs, or the app AnyList. It could also be replaced
with a grocery delivery service. The Recipe manager could also be replaced
with the recipes provided by a meal prep service on their website.
