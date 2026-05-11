import time

from get_data import update_data

while True:
    update_data()
    time.sleep(300)