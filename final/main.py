from plotdaynight import Plot
from scraper import Scrape


def run():
    scrapper = Scrape()
    scrapper.run()
    plotter = Plot()
    plotter.run()
    raw_input()
    scrapper.stop()
    plotter.stop()

run()