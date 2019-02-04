import configparser
import logging

from PIL import Image

from foxlib.toolkits.logger_toolkit import LoggerToolkit
# from uwo_ps_app.image_compare_estimator import ImageCompareEstimator as ICE

from uwo_ps_app.extractor import MarketRateExtractor
# from uwo_ps_utils.market_rates_cropper import PillowToolkit

ESTIMATOR_INPUTS = [
    ("./resources/goods.png", "./resources/goods.labels"),
    ("./resources/towns.png", "./resources/towns.labels"),
    ("./resources/rates.png", "./resources/rates.labels"),
    ("./resources/arrows.png", "./resources/arrows.labels")
]

GAME_NAME = "Uncharted Waters Online"
CONFIG_FILE = "config.ini"
config = configparser.ConfigParser()

DEFAULT = 'Default'
KEY_INTERVAL = 'interval'

def __load_config():
    config.read(CONFIG_FILE)
    try:
        config[DEFAULT]
    except KeyError:
        config[DEFAULT] = {}

def __save_config():
    try:
        f = open(CONFIG_FILE, "w")
        config.write(f)
    except:
        print("Something wrong while writing config")

def run_gui():
    from uwo_ps_app import game_screen_monitor as gsm
    from uwo_ps_app.formatter import FoxyFormatter

    __load_config()

    estimator = ICE(ESTIMATOR_INPUTS)
    monitor = gsm.GameScreenMonitor(GAME_NAME)
    try:
        monitor.set_interval(float(config[DEFAULT][KEY_INTERVAL]))
    except KeyError:
        print("No interval config")

    from uwo_ps_app.gui import MainApp
    app = MainApp(estimator, FoxyFormatter(), monitor)
    app.mainloop()

    config[DEFAULT][KEY_INTERVAL] = str(monitor.get_interval())
    __save_config()

def filepath2estimate():
    logging.basicConfig(level=logging.DEBUG)

    filepath = "/home/yerihyo/Downloads/1424950540855101629.png"
    marketplace_data = MarketRateExtractor.filepath2marketplace_data(filepath)
    ptgs_data_list = MarketRateExtractor.marketplace_data2ptgs_data_list(marketplace_data)


    # estimator = ICE(ESTIMATOR_INPUTS)
    # v = estimator.estimate(filepath)
    # print(v)

if __name__ == "__main__":
    filepath2estimate()
