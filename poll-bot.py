# Copyright 2021 Sal Sicari
import time 
import random
from selenium.webdriver.common.keys import Keys
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup 

# Run in background 
options = Options()
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--headless")
options.add_argument("--window-size=1920, 1200")
options.add_experimental_option("excludeSwitches", ["enable-logging"])


def main():
  load_webpage()
  poll_loop()
  get_response_data()

  driver.quit()


def load_webpage():
  username = input("Enter username: ")
  password = input("Enter password: ")
  presentation = input("Enter presentation name: ") #note: this is what comes after PollEV.com/(presentation)
  screen_name = input("Enter screen name: ") # If previously signed in screen name will not update
  global run_time
  run_time = int(input("Enter run time in seconds: "))
  # run_time = 4800 # If running in google cloud set up preexisting program run time
  global open_webpage_timer
  open_webpage_timer = time.perf_counter()

  url = "https://pollev.com/home"

  DRIVER_PATH = "C:\\Users\\ssica\\Desktop\\poll-bot\\chromedriver"
  global driver
  driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
  driver.maximize_window()
  driver.get(url)

  driver.find_element_by_xpath('/html/body/div/aside/div[2]/div[2]/pe-button[2]/button/span').click() #click agree if cookies messge pops up
  driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/tab-bar/nav/button[5]').click() #click log in

  driver.implicitly_wait(15)
  #enter username
  username_input = driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/div/div[3]/div/div/form/div[1]/div/div/pe-text-field/div/label/input')
  username_input.send_keys(username)
  driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/div/div[3]/div/div/form/button').click() #click next button on page



  #enter password
  password_input = driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/div/div[3]/div/div/div[1]/div/div[2]/pe-password-field/pe-text-field/div/label')
  password_input.send_keys(password)
  driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/div/div[3]/div/div/button[1]').click() # click log in

  #enter presentation
  presentation_input = driver.find_element_by_xpath('//*[@id="join-a-presentation"]/div/label/input')
  presentation_input.send_keys(presentation)

  #join presentation
  driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/div[1]/form/button').click()

def reset_webpage():
  # If the webpage doesn't reload after deactivating a question and it gets stuck this will automatically reload the webpage to reset it
  reset_condition = True
  while reset_condition:

    try:
     reset_condition = False
     element = WebDriverWait(driver,30).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/layout-tab-bar/section/div/main/div[3]/div/div[1]/img')))
     # After question wait up to input time to find xpath
    except:
      print('Timed out waiting for page to reset. Try again') # If xpath not found by end of given time 
      reset_condition = True
      action = webdriver.ActionChains(driver) # driver.refresh would break out of while loop so I opted to refresh the page this way
      action.key_down(Keys.CONTROL).send_keys(Keys.F5).perform()

def poll_loop():
  load_webpage_time = time.perf_counter()
  reached_webpage_time = load_webpage_time - open_webpage_timer # Gets the time of the above executions to more accurately keep track of time in the loop below
  i = reached_webpage_time
  poll_question = False
  while not poll_question:
      
      start_time = time.perf_counter()
      rand_num = random.randint(1,2) # get random number either 1 or 2 
      try:
        #If this works then no question is being asked
        time.sleep(3)
        active_poll = driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/div[3]/div/div[1]/img')
        # soup = BeautifulSoup(driver.page_source, 'html.parser') # Used Beautifulsoup for help debugging an error I was encountering
        # active_poll= soup.find('div', class_='hold-screen__logo')
        #print(f'{active_poll}')

        print('no question right now')

        #Refresh page after delay
        time.sleep(15)
        driver.refresh()
        time.sleep(5) # safety to make sure webpage fully loaded before checking for xpath
        end_time = time.perf_counter()
        total_time = end_time - start_time
        i = i + total_time
        # Subtracts the 7 secnds of time.sleep() from the get response data function
        if (i >= run_time - 7):
          break
          
          
          

      except:
        if (rand_num == 1):
          poll_response = driver.find_element_by_xpath("/html/body/div/div/layout-tab-bar/section/div/main/div[3]/div/div/div/div[2]/div[2]/div/button[1]") # a
          letter = 'A' # set a variable to A based on randNum value
        elif(rand_num == 2):
          poll_response = driver.find_element_by_xpath("/html/body/div/div/layout-tab-bar/section/div/main/div[3]/div/div/div/div[2]/div[2]/div/button[2]") # b
          letter = 'B' # set a variable to B based on randNum value

          # click a or b
        print('Clicked answer:', letter) # if 1 print A else B
        poll_response.click() # click answer
        
        reset_webpage()

        end_time = time.perf_counter()
        total_time = end_time - start_time
        i = i + total_time
        # Subtracts the 7 secnds of time.sleep() from the get response data function
        if (i >= run_time - 7):
          break

# Emails response data to the inputed email # Note: Data includes all responses from previous pollEV presenations due to a lack of clear data feauture
def get_response_data():
  driver.get('https://pollev.com/response_history')
  time.sleep(3)
  driver.find_element_by_xpath('/html/body/div/div/layout-tab-bar/section/div/main/pec-participant-response-history/div[2]/pe-button/button/span').click()
  print('Emailed Data')
  time.sleep(4)# Make sure export request finishes before program closes


if __name__ == "__main__":
    main()

