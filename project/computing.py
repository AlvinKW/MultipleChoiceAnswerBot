"""
Alvin Kwan
Class: CS 521 - Fall 2
Date: December 17, 2020
CS521 Project
Modules File
API key retrieved from: https://rapidapi.com/apigeek/api/google-search3/
tutorials/using-python-to-call-google-search-api
The project is designed to answer multiple choice questions through gathering
data from Google and basing off of the frequencies of the choices.
"""
import re
import requests
import pytesseract as tess
import nltk
from PIL import Image
from nltk.corpus import stopwords
nltk.download('stopwords')
###########################################################################
# If NLTK SSL error occurs uncomment
# import nltk
# import ssl

# try:
#     _create_unverified_https_context = ssl._create_unverified_context
# except AttributeError:
#     pass
# else:
#     ssl._create_default_https_context = _create_unverified_https_context

# nltk.download()
############################################################################

# Uncomment if you are using WINDOWS
# tess.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
class UserImage:
    '''
    Class for retrieving user image and converting to text
    ...

    Attributes
    ----------
    None

    Methods
    ----------
    convert_images():
        Convert user image to text and write into a text document
    '''

    def __init__(self, image):
        '''
        Constructor for UserImage
        '''
        self.image = image

    def convert_images(self):
        '''Converts user input image to String and import to a text document
        Arguments:
        None

        Returns:
        None
        '''
        # Check if file exist
        try:
            img = Image.open(self.image)
        except IOError:
            print("Error: {} file does not exist".format(self.image))
        else:
            text = tess.image_to_string(img)
            file = open('output.txt', 'w')
            file.writelines('')
            file = open('output.txt', 'a')
            file.writelines(text)
            file.close()

class UserInput:
    '''
    Class for writing user questiona and multiple choice to text document
    ...

    Attributes
    ----------
    None

    Methods
    ----------
    input_to_file():
        Write question and multiple choice answers to text document
    '''
    def __init__(self, question, choice):
        '''
        Constructor for UserInput object
        '''
        self.question = question
        self.choice = choice

    def input_to_file(self):
        '''Writes question and multiple choice to text file
        Arguments:
        None

        Returns:
        None
        '''
        file = open('output.txt', 'w')
        file.writelines('')
        file = open('output.txt', 'a')
        file.writelines(self.question)
        file.writelines('\n')
        file.writelines(self.choice)
        file.close()

class Search:
    '''
    A class that represent a search object
    ...

    Attributes
    ----------
    None

    Methods
    ----------
    __repr__():
        Returns a printable representation of the question
    __parse_search():
        Returns a dictionary of multiple choices and their frequency
    calculate_score():
        Returns a dictionary of multiple choice computed scores
    print_choice():
        Returns multiple choice and percentages, and dictionary from
        parseSearch()
    print_result():
        Prints result of the best choice based on calculations of text from google
    '''
    def __init__(self, question, choice, choice_list):
        '''
        Constructor for Search object
        '''
        self.__question = question
        self.__choice = choice
        self.__choice_list = choice_list

    def __repr__(self):
        '''Returns printable representation of object question
        Argument:
        None

        Returns:
        (String) printable representation of question
        '''
        return repr(self.__question + '?')

    def __parse_search(self):
        '''Check for frequency of words from question searched using Google Search API.
        Argument:
        None

        Returns:
        (dict) dictionary of words choices and their frequency
        '''
        word_dict = {}
        word = self.__choice.split()
        # Use Rapid Google API to query the text data
        url = "https://google-search3.p.rapidapi.com/api/v1/search/q={}&num=100".format(
            self.__question
        )
        # API Key
        headers = {
            'x-rapidapi-key': "b1fc6ac51dmsh35a6d981032b6b4p1c6a98jsnf36bb6f64b27",
            'x-rapidapi-host': "google-search3.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers)
        text = response.text
        text = text.lower()
        # Use regex to remove all punctuation
        text = re.sub(r'[^\w\s]', '', text)
        list_text = text.split()
        # Remove all stopwords
        list_text = [w for w in list_text if w not in stopwords.words('english')]
        # Initialize word dictionary to keep track of each word count
        # shown up in the text
        for item in word:
            word_dict[item] = 0
        # Iterate through the online text data and see if it matches
        # a word from choice list, increment by 1 if in list
        for item in list_text:
            if item in word:
                if item not in word_dict:
                    word_dict[item] = 1
                else:
                    word_dict[item] += 1
        return word_dict

    def calculate_score(self, words):
        '''Calculate the score of each multiple choice answers.
        Arguments:
        (dict) dictionary of words with their frequency

        Returns:
        (dict) dictionary of choices and computed scores
        '''
        choice_dict = {}
        # Initialize choice dictionary to keep track of frequency of each choice
        for item in self.__choice_list:
            choice_dict[item] = 0

        for key, value in words.items():
            for word in self.__choice_list:
                if key in word:
                    choice_dict[word] += value
        return choice_dict

    def print_choice(self):
        '''Helper function to return choices and their frequencies and dictionary used.
        Argumens:
        None

        Returns:
        (String) Multiple choice answers and their percentage
        (dict) Dictionary of multiple choicees and their frequencies
        '''
        title = "Multiple Choices: \n"
        output = title
        total = 0
        # Dictionary for holding words and their frequencies
        word_dict = self.__parse_search()
        for key, val in self.calculate_score(word_dict).items():
            total += val
        # Catch error if total equals zero
        try:
            if total != 0:
                # Iterate through dictionary and the sum of multiple choices
                for key, val in self.calculate_score(word_dict).items():
                    temp = (val/total)*100
                    output += '\t{} = {:,.2f}%\n'.format(key, temp)
            return output, word_dict
        except ZeroDivisionError as e:
            print("Error: {}".format(e))

    def print_result(self):
        '''Print function for result output.
        Arguments:
        None

        Returns:
        (String) Result text
        '''
        # Print the question object
        question_string = 'Question: ' + repr(Search(
            self.__question, self.__choice, self.__choice_list)) + '\n'
        print('Please wait...Processing...Computing Answer...\n')
        output, word_dict = self.print_choice()
        max_val = 0
        temp = 0
        # Compute the weight sum for each mutiple choice answers
        calculate_dict = self.calculate_score(word_dict)
        num_list = []
        # Initizalize list
        duplicate_list = [0]
        # Get answer with the highest value
        for key, val in calculate_dict.items():
            temp = val
            if max_val < temp:
                max_val = temp
                max_key = key
            if val not in num_list:
                num_list.append(val)
            else:
                duplicate_list.append(val)
        # Print conditions
        # Print error if answers not determined
        if max_val == 0:
            dash = '\n' + '-'*55
            msg = '\nError: answer cannot be determined'
            result = output + msg + dash
            return result
        # Print duplicates for multiple answers
        elif max_val == max(duplicate_list):
            duplicate_choice = []
            for key, val in calculate_dict.items():
                if max_val == val:
                    duplicate_choice.append(key)
            dash = '\n' + '-'*55
            msg = '\nThe most correct answers would be: {}'.format(duplicate_choice)
            result = output + msg + dash
            return result
        # Print answer
        else:
            dash = '\n' + '-'*55 + '\n'
            msg = '\nThe most correct answer would be: {}'.format(max_key)
            result = question_string + output + msg + dash
            return result
