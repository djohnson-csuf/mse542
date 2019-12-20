#!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import time
from selenium.webdriver.support.color import Color
import webcolors

# waits for a condition
# see https://blog.codeship.com/get-selenium-to-wait-for-page-load/
def wait_for(condition_function):
  start_time = time.time() 
  while time.time() < start_time + 3: 
    if condition_function(): 
      return True 
    else: 
      time.sleep(0.1) 

# waits for a page to finish loading
# see https://blog.codeship.com/get-selenium-to-wait-for-page-load/
class wait_for_page_load(object):

  def __init__(self, browser):
    self.browser = browser
    
  def __enter__(self):
    self.old_page = self.browser.find_element_by_tag_name('html')
    
  def page_has_loaded(self):
    new_page = self.browser.find_element_by_tag_name('html')
    return new_page.id != self.old_page.id
    
  def __exit__(self, *_):
    wait_for(self.page_has_loaded)

# Get the current square color
def GetSquareColor(driver):
    wait.until(lambda driver: driver.find_element_by_id('theSquare'))
    colorSquare = driver.find_element_by_id('theSquare').value_of_css_property('background-color')
    colorSquare = Color.from_string(colorSquare).rgb
    return colorSquare

# Get the current color of the button
def GetButtonColor(driver):
    wait.until(lambda driver: driver.find_element_by_id('theButton'))
    colorButton = driver.find_element_by_id('theButton').value_of_css_property('background-color')
    colorButton = Color.from_string(colorButton).rgb
    return colorButton

# Get the current number of points
def GetScore(driver):
    wait.until(lambda driver: driver.find_element_by_id('status'))
    status = driver.find_element_by_id('status').text
    score = GetScoreFromStatus(status)
    return score

# Get the current number of lives
def GetLives(driver):
    wait.until(lambda driver: driver.find_element_by_id('status'))
    status = driver.find_element_by_id('status').text
    lives = GetLivesFromStatus(status)
    return lives

def GetScoreFromStatus(status):
    # 2nd and 4th index is the score and number of lives, respectively
    pieces = str.split(str(status),' ') 
    if (len(pieces) == 5):
        return int(pieces[2])
    else:
        return 0

def GetLivesFromStatus(status):
    # 2nd and 4th index is the score and number of lives, respectively
    pieces = str.split(str(status),' ') 
    if (len(pieces) == 5):
        return int(pieces[4])
    else:
        return 0

# Click the button
def ClickButton(driver):
    wait.until(lambda driver: driver.find_element_by_id('theButton'))
    theButton = driver.find_element_by_id('theButton')
    theButton.click()
    print('Clicked button')

# Function to handle test case TC-CSCG-001
def IfRightScoreShouldIncreasesAndLivesStaySame(driver):
    testedColors = []
    while (len(testedColors) < 7): # there are 7 possible colors
        lastScore = GetScore(driver)
        lastLives = GetLives(driver)
        buttonColor = GetButtonColor(driver)
        squareColor = GetSquareColor(driver)
        if (buttonColor == squareColor):
            WebDriverWait(driver, 100) # wait an additional 100ms to ensure it isn't the button transitioning to white temporarily between color change
            if (buttonColor == squareColor and buttonColor not in testedColors):
                ClickButton(driver)
                WebDriverWait(driver, 250) # wait 250ms then assert that the score changed and lives didn't
                assert (GetScore(driver) > lastScore)
                assert (GetLives(driver) == lastLives)
                testedColors.append(buttonColor)

# Function to handle test case TC-CSCG-002
def IfWrongLivesShouldDecrease(driver):
    while (GetLives(driver) > 0):
        lastScore = GetScore(driver)
        lastLives = GetLives(driver)
        if (GetButtonColor(driver) != GetSquareColor(driver)):
            ClickButton(driver)
            WebDriverWait(driver, 1000) # wait a second then assert that the lives changed and score
            assert (GetScore(driver) == lastScore)
            assert (GetLives(driver) < lastLives)

# Function to handle test case TC-CSCG-003
def IfRight20TimesScoreShouldBe20AndLives5(driver):
    while (GetScore(driver) < 20): 
        lastScore = GetScore(driver)
        lastLives = GetLives(driver)
        buttonColor = GetButtonColor(driver)
        squareColor = GetSquareColor(driver)
        if (buttonColor == squareColor):
            WebDriverWait(driver, 100) # wait an additional 100ms to ensure it isn't the button transitioning to white temporarily between color change
            if (buttonColor == squareColor):
                ClickButton(driver)
                WebDriverWait(driver, 250) # wait 250ms then assert that the score changed and lives didn't
                assert (GetScore(driver) > lastScore)
                assert (GetLives(driver) == lastLives)

# Initialize the selenium webdriver for the game
# I use the chrome webdriver, you can use whatever 
# browser you want and it will work the same
driver = webdriver.Chrome()
driver.get('https://www.compendiumdev.co.uk/games/buggygames/the_coloured_square_game/colouredsquarechanger.html')

# the standard wait with 10 second polling
wait = WebDriverWait(driver, 10)

with wait_for_page_load(driver):
    IfRightScoreShouldIncreasesAndLivesStaySame(driver)
    IfRight20TimesScoreShouldBe20AndLives5(driver)
    IfWrongLivesShouldDecrease(driver)