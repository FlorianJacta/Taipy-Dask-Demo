import utils

import taipy as tp
from taipy.gui import notify, Markdown
from taipy.config import Config

import numpy as np
import pandas as pd

BUSINESS_PATH = "data/yelp_business.csv"

# Load the business data using pandas
business_df = pd.read_csv(BUSINESS_PATH)
business_df["size"] = np.sqrt(business_df.loc[:,'review_count']/business_df.loc[:,'review_count'].max())*80 + 3
business_df['text'] = business_df['name'] + '</br>' + business_df['address'] + '</br>Stars:' + business_df['stars'].astype(str)+ '/5'

# Taipy Core
Config.load("config/config.toml")

Config.configure_data_node(id="review_data", read_fct_params=("data/yelp_review.csv",))

scenario_object = Config.scenarios["scenario"]
business_name = '"Mon Ami Gabi"'
reviews = pd.DataFrame({"review_id":[''],
                        "user_id":[''],
                        "business_id":[''],
                        "stars":[''],
                        "date":[''],
                        "text":[''],
                        "useful":[''],
                        "funny":[''],
                        "cool":['']})

print(reviews)

def on_selection(state):
    """
    Re-runs the scenario when the user selects a business.

    Args:
        - state: state of the app
    """
    print("Running query...")
    notify(state, "info", "Running query...")
    scenario = tp.create_scenario(scenario_object)
    scenario.business_name.write(state.business_name)
    tp.submit(scenario)

    tp.submit(scenario)
    state.reviews = scenario.parsed_reviews.read()
    notify(state, "success", "Query finished")
    print("Query finished")



categories = [category.split("|") for category in list(business_df.categories.astype(str))]
categories = ["All"] + utils.get_most_present_values(list(np.concatenate(categories).flat))
category = categories[0]

stars = ['0', '1', '2', '3', '4', '5']
selected_star = stars[0]

business_name_input = ""

business_names = list(business_df.name)

page = Markdown("""<|toggle|theme|>

# Querying **Big Data**{: .color-primary} with Taipy and Dask

## Select a **business**{: .color-primary}
<|layout|columns=1 1 1|
<|{business_name_input}|input|on_change=select_business|>

<|{category}|selector|lov={categories}|dropdown|on_change=select_business|>

<|{selected_star}|slider|lov={stars}|labels=True|on_change=select_business|>
|>

<|{business_name}|selector|lov={list(business_df.name)}|dropdown|on_change=on_selection|>

<|expandable|expanded=False|
<|{business_df}|chart|type=scattermapbox|lat=latitude|lon=longitude|marker={marker_map}|layout={layout_map}|mode=markers|height=1000px|text=text|>
|>

## Average **stars**{: .color-primary} for that business: <|{"⭐"*int(np.mean(reviews.stars))}|text|raw|>

<|{round(np.mean(reviews.stars),2)}|indicator|value={np.mean(reviews.stars)}|min=1|max=5|width=30%|>

## **Reviews**{: .color-primary} for that business:



<|expandable|expanded=False|
<|{reviews}|chart|type=histogram|x=stars|rebuild|>
|>

<|expandable|expanded=False|
<|{reviews}|table|width=100%|>
|>
""")

marker_map = {"color":"stars", "size": "size", "showscale":True, "colorscale":"RdYlGn"}
layout_map = {
            "dragmode": "zoom",
            "mapbox": { "style": "open-street-map", "center": { "lat": 41.5, "lon": -81.6 }, "zoom": 10}
            }


def select_business(state):
    selected_star = int(state.selected_star)
    if state.category == "All":
        category = ""
    else:
        category = state.category

    query = (business_df.name.str.contains(state.business_name_input)) & (business_df.stars >= selected_star) & (business_df.categories.astype(str).str.contains(category))
    print(len(business_df))
    state.business_df = business_df[query]
    print(len(state.business_df))
