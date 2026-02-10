from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidSessionIdException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
import threading
from interfaces import MCQuestion, FillInBlank, Constellation

debug = True


def getQuestion(fDriver):
    mcq_elements = fDriver.find_elements(By.ID, "choice-section")
    map_elements = fDriver.find_elements(By.XPATH, "//img[@alt='constellation question']")
    fill_elements = fDriver.find_elements(By.ID, "word-hint")
    correction_elements = fDriver.find_elements(By.ID, "context-help")
    stopSession = fDriver.find_elements(By.ID, "Click_me_to_stop")

    if correction_elements:
        nextButton = fDriver.find_element(By.ID, "next-btn")
        keyWordElement = fDriver.find_element(By.CLASS_NAME, 'wordform')
        keyWord = fDriver.execute_script("return arguments[0].innerText.trim();", keyWordElement)
        keyboard = ActionChains(fDriver)
        return ("CORRECTION", keyWord, nextButton, keyboard)

    elif map_elements:
        try:
            image_element = fDriver.find_element(By.XPATH, "//img[@alt='constellation question']")
            src_link = image_element.get_attribute('src')


            question_element = fDriver.find_element(By.CSS_SELECTOR, "h3.question")
            question_text = fDriver.execute_script("return arguments[0].innerText.trim();", question_element)
            question_text="Choose the word that best fits the following words: "    # overwriting for better prompt (hopefully)

            choice_one = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="0"]')
            choice_two = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="1"]')
            choice_three = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="2"]')
            choice_four = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="3"]')

            def get_choice_text(elements):
                texts = []
                for el in elements:
                    try:
                        text = fDriver.execute_script("return arguments[0].innerText ? arguments[0].innerText.trim() : '';", el)
                        texts.append(text)
                    except Exception as e:
                        print(f"Error reading choice text: {e}")
                return texts

            choice_texts = [
                get_choice_text(choice_one),
                get_choice_text(choice_two),
                get_choice_text(choice_three),
                get_choice_text(choice_four),
            ]

            # Flatten to single strings per choice assuming each list contains one string 
            optionA = "[A] " + (choice_texts[0][0] if choice_texts[0] else '')
            optionB = "[B] " + (choice_texts[1][0] if choice_texts[1] else '')
            optionC = "[C] " + (choice_texts[2][0] if choice_texts[2] else '')
            optionD = "[D] " + (choice_texts[3][0] if choice_texts[3] else '')

            constellation_obj = {
                "src": src_link,
                "question": question_text,
                "options": (optionA, optionB, optionC, optionD),
                "image_element": image_element,
            }


            details = (constellation_obj, map_elements, choice_one, choice_two, choice_three, choice_four)
            return ("CONSTELLATION",) + details

        except Exception as e:
            print(f"Constellation error: {e}")
            return ("UNKNOWN", None)

    elif fill_elements:
        try:
            fill_element = fill_elements[0]
            hint = fDriver.find_element(By.CSS_SELECTOR, '#word-hint p span').text
            first_letter = fDriver.find_element(By.CLASS_NAME, "first-letter").text
            maxlength_value = fDriver.find_element(By.ID, "choice").get_attribute("maxlength")
            max_length = 1+(int(maxlength_value))
            fill_obj = FillInBlank(maxLength=max_length, firstLetter=first_letter, hint=hint)
            keyboard = ActionChains(fDriver)
            print(f"Detected Fill-in-the-Blank: Hint={hint}, FirstLetter={first_letter}, MaxLength={max_length}")
            return ("FILL", fill_obj, fill_element, keyboard)
        except Exception as e:
            print(f"Fill error: {e}")
            return ("UNKNOWN", None)

    elif mcq_elements:
        choiceOne = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="0"]')
        choiceTwo = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="1"]')
        choiceThree = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="2"]')
        choiceFour = fDriver.find_elements(By.CSS_SELECTOR, '[data-value="3"]')
        def getChoiceText(givenChoiceElements):
            result = []
            for c in givenChoiceElements:
                try:
                    full_text = fDriver.execute_script("return arguments[0].innerText ? arguments[0].innerText.trim() : '';", c)
                    result.append(full_text)
                except Exception as e:
                    print(f"Error reading choice text: {e}")
            return result
        optionA = (" [A] " + str(getChoiceText(choiceOne)))
        optionB = (" [B] " + str(getChoiceText(choiceTwo)))
        optionC = (" [C] " + str(getChoiceText(choiceThree)))
        optionD = (" [D] " + str(getChoiceText(choiceFour)))
        questionElement = fDriver.find_element(By.CLASS_NAME, "question")
        questionText = fDriver.execute_script("return arguments[0].innerText.trim();", questionElement)
        MCQ_Question = MCQuestion(question=questionText, choices=[optionA, optionB, optionC, optionD])
        return ("MCQ", MCQ_Question, choiceOne, choiceTwo, choiceThree, choiceFour)
    
    elif stopSession:
        return "STOP"

    else:
        print("Unknown question type detected.")
        return ("UNKNOWN", None)
