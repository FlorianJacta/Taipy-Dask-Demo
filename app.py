import taipy as tp
from taipy.gui import Gui

from pages.maps import scenario_object, page

def on_init(state):
    scenario = tp.create_scenario(scenario_object)
    tp.submit(scenario)
    state.reviews = scenario.parsed_reviews.read()

if __name__ == "__main__":
    tp.Core().run()
    Gui(page).run(port=5001)
