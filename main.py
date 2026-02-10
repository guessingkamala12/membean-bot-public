from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import interfaces as inter
import getQuestion as gq
from dotenv import load_dotenv
import os

load_dotenv() 


user = os.getenv("MEMBEAN_USER")
password = os.getenv("MEMBEAN_PASSWORD")
if not user or not password:
    raise RuntimeError("Missing MEMBEAN_USER or MEMBEAN_PASSWORD environment varihoables. Create a .env file or set them in your environment.")
import answerQuestion as answer
import ocrConstellations as ocr

# KNOWN BUG: SOMETIMES IT DOESN'T PICK UP CORRECTION ELEMENTS

debug = False

chrome_options = Options()
# Run headless (modern headless mode)
# chrome_options.add_argument("--headless=new")

# Recommended extras for stability
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
# note: detach isn't useful for headless mode, so we don't set detach

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://membean.com/login")

wait = WebDriverWait(driver, 10)

# login info
driver.find_element(By.ID, "username").send_keys(user)
driver.find_element(By.ID, "password").send_keys(password)

# REMEMBER SIGNIN
rememberMe = driver.find_element(By.ID, "rememberMe")
driver.execute_script("arguments[0].parentNode.click();", rememberMe)
time.sleep(0.5)

# Sign in
signIn = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
signIn.click()

# Wait for startSession button
startSession = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "startTrainingBtn"))
)
driver.execute_script("arguments[0].click();", startSession)

# Try to select 15 min session if available, otherwise move on
try:
    intoSession = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.ID, "15_min_"))
    )
    driver.execute_script("arguments[0].click();", intoSession)
    print("15 min session selected.")
except Exception as e:
    print("15 min session not visible or not required. Continuing…\n")

while True:
    try:
        qType, *details = gq.getQuestion(driver)
        print(f"Received question type: {qType}")

        if qType == "MCQ":
            mcqObj, choiceOne, choiceTwo, choiceThree, choiceFour = details
            print(mcqObj)
            answered = answer.solveMCQ(mcqObj)
            print("Selecting:", answered, "\n")
            time.sleep(8)
            if answered == 'A' and choiceOne:
                choiceOne[0].click()
            elif answered == 'B' and choiceTwo:
                choiceTwo[0].click()
            elif answered == 'C' and choiceThree:
                choiceThree[0].click()
            elif answered == 'D' and choiceFour:
                choiceFour[0].click()
            time.sleep(4)


        elif qType == "FILL":
            fillObj, fillElement, keyboard = details
            fill_answer = answer.solveFillInBlank(fillObj)

            if not fill_answer:
                print("🚨 ERROR: NO FILL ANSWER RETRIEVED")
                time.sleep(2)
                continue

            # keep your slice here
            fill_answer = fill_answer[1:]

            input_box = wait.until(EC.element_to_be_clickable((By.ID, "choice")))
            input_box.click()
            for char in fill_answer:
                input_box.send_keys(char)
                time.sleep(0.5)
            time.sleep(4)


        elif qType == "CONSTELLATION":
            constellationObj, mapElement, choiceOne, choiceTwo, choiceThree, choiceFour = details
            if debug: print(f"Constellation: {constellationObj}")
            themeWords = ocr.getText(constellationObj['src'])
            constellationQuestion = inter.Constellation(
                question = f"{constellationObj['question']} {themeWords}",
                options = constellationObj['options']
            )
            if debug: print(constellationQuestion)

            theAnswer = answer.solveConstellations(constellationQuestion)
            time.sleep(8)
            if theAnswer == 'A' and choiceOne:
                choiceOne[0].click()
            elif theAnswer == 'B' and choiceTwo:
                choiceTwo[0].click()
            elif theAnswer == 'C' and choiceThree:
                choiceThree[0].click()
            elif theAnswer == 'D' and choiceFour:
                choiceFour[0].click()
            time.sleep(4)  # <--- Wait after answering


        elif qType == "CORRECTION":
            keyWord, nextButton, keyboard = details
            keyboard.send_keys("a")
            keyboard.send_keys("b")
            keyboard.send_keys("c")
            keyboard.perform()
            time.sleep(60)
            nextButton.click()
            try:
                time.sleep(2)
                driver.find_element(By.ID, "wordspell")
                # If found, proceed with typing the correction
                try:
                    inputBox = wait.until(
                        EC.element_to_be_clickable((By.ID, "choice"))
                    )
                    inputBox.click()
                    for char in keyWord:
                        inputBox.send_keys(char)
                        time.sleep(0.5)
                    time.sleep(1)
                except Exception as e:
                    print("Correction input box not found or error typing:", e)
            except NoSuchElementException:
                print("No correction wordtype element found, skipping...\n")
                pass

            time.sleep(4)  # <--- Wait after answering
        
        elif qType == "S":
            stopButton = driver.find_element(By.CLASS_NAME, "danger")
            stopButton.click() # hi
            print("\n"*4)
            print("Session succesfully ended.")
            exit()

        elif qType == "UNKNOWN":
            print("Unrecognized question type: skipping...")
            time.sleep(4)  # <--- Wait just in case

    except Exception as e:
        print(f"Error in main loop: {e}")
        time.sleep(3)

input("Press Enter to exit...")
