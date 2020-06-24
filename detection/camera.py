import urllib.request
import yaml
from os import path

# Global configuration for file
cur_path = path.dirname(path.abspath(__file__))
cfg_path = cur_path + "/cfg/cfg.yml"
config = yaml.safe_load(open(cfg_path))


def take_picture(num):
    """
    A simple function to take a picture from a given URL and saving it locally
    """
    URL = config['camera_url']

    with urllib.request.urlopen(URL) as url:
        with open(cur_path + f'/captures/picture_{num}.jpg', 'wb') as f:
            f.write(url.read())
