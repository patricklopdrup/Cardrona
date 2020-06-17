import urllib.request
import yaml

config = yaml.safe_load(open("cfg/cfg.yml"))


def take_picture(num):
    URL = config['camera_url']

    with urllib.request.urlopen(URL) as url:
        with open(f'captures/picture_{num}.jpg', 'wb') as f:
            f.write(url.read())
