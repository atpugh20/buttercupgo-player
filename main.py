#Testing some git stuff
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import *
from selenium.webdriver.common.by import By

service = Service("msedgedriver.exe")
driver = webdriver.Firefox()
driver.get("https://buttercup.rocks/")


def get_window(even_obs):
    top = ""
    bottom = ""
    path = '//*[@id="__next"]/div/div[5]/div[4]/div[3]' if even_obs else '//*[@id="__next"]/div/div[5]/div[5]/div[3]'
    window = driver.find_element(By.XPATH, f'{path}').get_attribute('style')
    top_finished = False
    for letter in window:
        if letter.isdigit():
            if top_finished:
                bottom += letter
            else:
                top += letter
        elif letter == ";":
            top_finished = True
    top = int(top)
    bottom = int(bottom)
    return [top, bottom]

def get_buttercup():
    y_axis = ""
    window = driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[5]/div[6]').get_attribute('style')
    x_finished = False
    for letter in window:
        if letter.isdigit() or letter == ".":
            if x_finished:
                y_axis += letter
        elif letter == ",":
            x_finished = True
        elif x_finished and letter == ")":
            break
    return float(y_axis)

def track_obstacles(even_obs):
    x_axis = ""
    path = '//*[@id="__next"]/div/div[5]/div[4]' if even_obs else '//*[@id="__next"]/div/div[5]/div[5]'
    position = driver.find_element(By.XPATH, f'{path}').get_attribute('style')
    w_finished = False
    for letter in position:
        if letter.isdigit() or letter == ".":
            if w_finished:
                x_axis += letter
        elif letter == ";":
            w_finished = True
        elif w_finished and letter == "p":
            break
    if x_axis == "":
        x_axis = "0"

    return float(x_axis)


while True:
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "div button").click()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, 'body').click()
    on_even_obstacle = False

    while driver.find_element(By.CSS_SELECTOR, ".styles_deadMessage__kW9am").get_attribute("style") == "display: none;":
        current_obstacle = track_obstacles(on_even_obstacle)
        print(current_obstacle)
        if current_obstacle > 600:
            on_even_obstacle = not on_even_obstacle
            current_obstacle = track_obstacles(on_even_obstacle)
        obstacle_height = get_window(on_even_obstacle)
        buttercup_y = get_buttercup()
        if obstacle_height[1] + 200 + 90.25 >= buttercup_y - 62.03:
            driver.find_element(By.CSS_SELECTOR, 'body').click()

    time.sleep(1)
    initials = driver.find_element(By.CSS_SELECTOR, ".styles_input__3823I")
    initials.send_keys("gee")
    driver.find_element(By.CSS_SELECTOR, ".styles_submitButton__2B0Uc button").click()
    time.sleep(1)
    driver.find_element(By.CSS_SELECTOR, ".styles_backButtonCt__1SJax button").click()
