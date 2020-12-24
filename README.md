# MultipleChoiceAnswerBot
A Python program that prompts user for a question and multiple choice answers. Retrieve data from Google using Rapid API, and compute the most correct answer out of the following choices.

![Screenshot](https://github.com/AlvinKW/MultipleChoiceAnswerBot/blob/main/example.gif)

## Getting Started

### Prerequisites
Things you need to install:

```
nltk
Pillow
pytesseract
regex
requests
tesseract
```

### Installing


1. Clone the repository
```
git clone https://github.com/AlvinKW/MultipleChoiceAnswerBot.git
```
2. cd to directory where requirements.txt is located
```
Run pip install -r requirements.txt
```
3. Install tesseract
```
Windows: Install tesseract from https://github.com/UB-Mannheim/tesseract/wiki
         Create a folder Tesseract-OCR where requirements.txt is located
         Install exe file inside Tesseract-OCR
         Uncomment tess.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe' in computing.py file
MacOS: brew install tesseract
```
4. Get API Key
```
https://rapidapi.com/apigeek/api/google-search3/endpoints
```

### Running the application
cd to where main.py located and in terminal use commands:
```
python3 main.py
```


## Author

Alvin Kwan
