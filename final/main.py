from plotdaynight import Plot
from scraper import Scrape
import sys

def run():
    if len(sys.argv)==1:
        index='25544'
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
