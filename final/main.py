import sys

from plotdaynight import Plot
from scraper import Scrape


def run():
    if len(sys.argv) == 1:
        index = '35931'
    else:
        index = str(sys.argv[1])
    scrapper = Scrape(index)
    scrapper.run()
    plotter = Plot(index)
    plotter.run()
    raw_input()
    scrapper.stop()
    plotter.stop()


run()
