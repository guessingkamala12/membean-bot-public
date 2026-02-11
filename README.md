# Membean Bot Public

An automated Membean training session bot that uses Selenium for web automation and OpenAI's GPT models to intelligently answer vocabulary questions.

## ⚠️ Disclaimer

This project is intended for **educational purposes only**. Using automation tools on educational platforms like Membean may violate their Terms of Service. Use this software at your own risk. The author is not responsible for any consequences resulting from the use of this code.

## Features

- 🤖 **Automated Login**: Automatically logs into your Membean account
- - 🧠 **AI-Powered Answers**: Uses OpenAI's GPT-4o models to solve vocabulary questions
  - - 📝 **Multiple Question Types**: Handles various question formats:
    -   - Multiple Choice Questions (MCQ)
        -   - Fill-in-the-Blank
            -   - Constellation (word mapping with OCR)
                -   - Correction exercises
                    - - 🔍 **OCR Integration**: Uses EasyOCR to read text from constellation images
                      - - ⚙️ **Configurable**: Environment-based configuration for credentials and API keys
                       
                        - ## Prerequisites
                       
                        - - Python 3.8 or higher
                          - - Google Chrome browser (latest version)
                            - - ChromeDriver (compatible with your Chrome version)
                              - - OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
                                - - Membean account credentials
                                 
                                  - ## Installation
                                 
                                  - 1. **Clone the repository**
                                    2.    ```bash
                                             git clone https://github.com/guessingkamala12/membean-bot-public.git
                                             cd membean-bot-public
                                             ```

                                          2. **Install dependencies**
                                          3.    ```bash
                                                   pip install -r requirements.txt
                                                   ```

                                                3. **Set up environment variables**
                                            
                                                4.       Create a `.env` file in the root directory by copying the example file:
                                                5.      ```bash
                                                6.     cp .env.example .env
                                                7.    ```

                                                         Edit the `.env` file and add your credentials:
                                                         ```env
                                                         # Membean credentials
                                                         MEMBEAN_USER=your_membean_username
                                                         MEMBEAN_PASSWORD=your_membean_password

                                                         # OpenAI API key (get one at https://platform.openai.com/api-keys)
                                                         OPENAI_API_KEY=sk-your-openai-api-key-here
                                                         ```

                                                      4. **Install ChromeDriver** (if not already installed)
                                                  
                                                      5.       The bot uses Selenium with Chrome. Make sure you have ChromeDriver installed and added to your PATH, or install it via:
                                                      6.      ```bash
                                                      7.     # On macOS
                                                      8.    brew install chromedriver
                                                  
                                                      9.      # On Ubuntu/Debian
                                                      10.     sudo apt-get install chromium-chromedriver
                                                  
                                                      11.       # Or use webdriver-manager (optional, uncomment in requirements.txt)
                                                      12.      pip install webdriver-manager
                                                      13.     ```
                                                  
                                                      14. ## Usage
                                                  
                                                      15. Run the main script:
                                                      16. ```bash
                                                          python main.py
                                                          ```

                                                          The bot will:
                                                          1. Open Chrome and navigate to Membean's login page
                                                          2. 2. Log in with your credentials
                                                             3. 3. Start a training session (attempts to select 15-minute sessions if available)
                                                                4. 4. Automatically answer questions as they appear
                                                                   5. 5. Continue until the session ends
                                                                     
                                                                      6. ### Headless Mode
                                                                     
                                                                      7. To run the bot without opening a visible browser window, uncomment this line in `main.py`:
                                                                      8. ```python
                                                                         chrome_options.add_argument("--headless=new")
                                                                         ```

                                                                         ### Debug Mode

                                                                         To see detailed console output for troubleshooting, set `debug = True` in `main.py`:
                                                                         ```python
                                                                         debug = True
                                                                         ```

                                                                         ## Project Structure

                                                                         ```
                                                                         membean-bot-public/
                                                                         ├── main.py                  # Entry point - handles login and main loop
                                                                         ├── getQuestion.py           # Detects and extracts different question types
                                                                         ├── answerQuestion.py        # Uses OpenAI to generate answers
                                                                         ├── interfaces.py            # Data classes for question types
                                                                         ├── ocrConstellations.py     # OCR functionality for constellation images
                                                                         ├── requirements.txt         # Python dependencies
                                                                         ├── .env.example             # Example environment variables file
                                                                         ├── .gitignore              # Git ignore rules
                                                                         ├── .gitattributes          # Git attributes for line endings
                                                                         └── README.md               # This file
                                                                         ```

                                                                         ## How It Works

                                                                         1. **Question Detection** (`getQuestion.py`): Analyzes the page DOM to identify the question type
                                                                         2. 2. **Answer Generation** (`answerQuestion.py`): Sends question data to OpenAI's API for intelligent responses
                                                                            3. 3. **OCR Processing** (`ocrConstellations.py`): Extracts text from constellation images using EasyOCR
                                                                               4. 4. **Answer Submission** (`main.py`): Selects the appropriate answer or fills in text based on the question type
                                                                                 
                                                                                  5. ## Known Issues
                                                                                 
                                                                                  6. - **Correction Elements**: Sometimes the bot doesn't pick up correction elements properly (noted in code)
                                                                                     - - **Fill-in-the-Blank**: The bot slices off the first character of answers (`fill_answer[1:]`) - this may need adjustment based on Membean's current interface
                                                                                       - - **OCR Accuracy**: Constellation word recognition depends on image quality and may occasionally misread words
                                                                                        
                                                                                         - ## Configuration Options
                                                                                        
                                                                                         - ### `.env` File Variables
                                                                                        
                                                                                         - | Variable | Description | Required |
                                                                                         - |----------|-------------|----------|
                                                                                         - | `MEMBEAN_USER` | Your Membean username | Yes |
                                                                                         - | `MEMBEAN_PASSWORD` | Your Membean password | Yes |
                                                                                         - | `OPENAI_API_KEY` | Your OpenAI API key | Yes |
                                                                                        
                                                                                         - ### Customization
                                                                                        
                                                                                         - - **Session Duration**: The bot attempts to select 15-minute sessions. Modify the ID selector in `main.py` for different durations
                                                                                           - - **AI Model**: Change the model in `answerQuestion.py` (currently uses `gpt-4o-mini` for MCQ and `gpt-4o` for other types)
                                                                                             - - **Wait Times**: Adjust `time.sleep()` values in `main.py` to control pacing between answers
                                                                                              
                                                                                               - ## Dependencies
                                                                                              
                                                                                               - Key dependencies include:
                                                                                               - - `selenium` - Web automation
                                                                                                 - - `easyocr` - Optical character recognition
                                                                                                   - - `openai` - OpenAI API client
                                                                                                     - - `python-dotenv` - Environment variable management
                                                                                                       - - `torch` & `torchvision` - Required for EasyOCR
                                                                                                         - - `Pillow` & `opencv-python` - Image processing
                                                                                                          
                                                                                                           - See `requirements.txt` for complete list and versions.
                                                                                                          
                                                                                                           - ## Contributing
                                                                                                          
                                                                                                           - This is a public educational project. Contributions, bug reports, and feature requests are welcome! Please feel free to:
                                                                                                           - 1. Fork the repository
                                                                                                             2. 2. Create a feature branch
                                                                                                                3. 3. Make your changes
                                                                                                                   4. 4. Submit a pull request
                                                                                                                     
                                                                                                                      5. ## License
                                                                                                                     
                                                                                                                      6. This project is provided as-is for educational purposes. Please ensure you comply with Membean's Terms of Service and use responsibly.
                                                                                                                     
                                                                                                                      7. ## Support
                                                                                                                     
                                                                                                                      8. For issues or questions, please open an issue on GitHub.
                                                                                                                     
                                                                                                                      9. ---
                                                                                                                     
                                                                                                                      10. **Note**: This bot requires active OpenAI API credits. Monitor your usage at https://platform.openai.com/usage to avoid unexpected charges.
