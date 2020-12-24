"""
Alvin Kwan
Class: CS 521 - Fall 2
Date: December 17, 2020
CS521 Project
Main File
The project is designed to answer multiple choice questions through gathering
data from Google and basing off of the frequencies of the choices.
"""
import os.path
from computing import UserImage, UserInput, Search

def main():
    '''Main method. Prompts user for input based on the following choices:
    Upload file, input manual question, exit program.
    Arguments:
    None

    Returns:
    None
    '''
    while True:
        # Print dialogue to user
        print('\n' + "#"*55 + '\n')
        print('Enter a choice: \n')
        print('1. Upload multiple choice question through image file')
        print('2. Enter multiple choice question manually')
        print('3. Exit program\n')
        user_input = input()
        # Import image from file and compute result of multiple choice question
        if user_input == '1':
            user_img = input('Enter image file located on same directory as main.py: ')
            if 'png' in user_img and os.path.exists(user_img):
                option_one(user_img)
            else:
                print('Error: File not found')
        # Get user's manual question and compute result
        elif user_input == '2':
            option_two()
        # End program
        elif user_input == '3':
            print("Program has ended.")
            break
        else:
            print("Invalid input.")

def option_one(user_img):
    '''Get image from user and convert to String and import to output.txt
    From output.txt, parse question and muliple choices and return best answer
    Arguments:
    (str) image name

    Returns:
    None
    '''
    # Convert image to String and input to output.txt
    user_image = UserImage(user_img)
    user_image.convert_images()
    # Parse question from output.txt
    valid, msg = get_question()
    # Check if question is valid
    if valid:
        choices_string = ''
        choices_list = get_choices()
        question = msg
        # Create choice string from choice list
        for item in choices_list:
            choices_string += item + '\n'
        # Search object to search question
        new_search = Search(question, choices_string, choices_list)
        print('-'*55)
        # Result
        search_result = new_search.print_result()
        print(search_result)
        # Prompt user if he/she want to save result to history.txt
        while True:
            user_save = input("Do you want to save result to history.txt: (Y/N)? ")
            if user_save.lower() == 'y':
                save_to_history(search_result)
                break
            elif user_save.lower() == 'n':
                break
            else:
                print("Error: invalid input")
    else:
        print(msg)

def option_two():
    '''Prompt user to enter multiple choice questions and chain of possible
    answers. Import string to output.txt. From output.txt, parse question
    and muliple choices and return best answer.
    Arguments:
    None

    Returns:
    None
    '''
    # Prompt user for multiple choice question
    user_question = input("Enter multiple choice question: ")
    print('\n')
    choices_string = ''
    # Check if question is valid
    user_input_ob = UserInput(user_question, choices_string)
    user_input_ob.input_to_file()
    valid, msg = get_question()
    if valid:
        # Prompt user for multiple choice answers, delimited by new line
        user_choices = []
        print("Enter multiple choices (DO NOT ENTER NUMBERS): ")
        print("After each individual choice, hit ENTER.")
        print("Enter '0' to state you are finished adding choices.")
        # Keep entering answers while condition is TRUE
        while True:
            user_input = input()
            # Make sure user does not enter a number other than 0
            if user_input != '0' and user_input.isdigit():
                print('{} will not be considered. Please do not enter numbers.'.format(user_input))
            # '0' means no more answers to input
            elif user_input == '0':
                choices_string = ''
                # Create choice string from choice list
                for item in user_choices:
                    choices_string += item + '\n'
                user_input_second = UserInput(user_question, choices_string)
                user_input_second.input_to_file()
                choices_string = ''
                choices_list = get_choices()
                question = msg
                for item in choices_list:
                    choices_string += item
                # Search object to search question
                new_search = Search(question, choices_string, choices_list)
                print('-'*55)
                # Result
                search_result = new_search.print_result()
                print(search_result)
                # Prompt user if he/she want to save result to history.txt
                while True:
                    user_save = input("Do you want to save result to history.txt: (Y/N)? ")
                    if user_save.lower() == 'y':
                        save_to_history(search_result)
                        break
                    elif user_save.lower() == 'n':
                        break
                    else:
                        print("Error: invalid input")
                break
            else:
                user_choices.append(user_input)
    else:
        print(msg)

def save_to_history(answer):
    '''Save string to history.txt file by appending.
    Arguments:
    (String) result string

    Returns:
    None
    '''
    file = open('history.txt', 'a')
    file.writelines(answer)
    file.close()

def get_question():
    '''Function to retrieve question from output.txt
    Arguments:
    None

    Returns:
    (bool) question is valid or not
    (str) message for error otherwise return question
    '''
    # Return none and false if not a question
    # otherwise return question
    valid = True
    error_msg = None
    file = open('output.txt', 'r')
    question = ''
    for line in file:
        sentence = line.split()
        for word in sentence:
            question += word + ' '
    temp = question
    # Separate question from other text
    sep = '?'
    question = question.split(sep, 1)[0]
    if sep not in temp or len(question) < 5:
        valid = False
        error_msg = 'Error: invalid question (make sure to end question with \'?\')'
        return valid, error_msg
    else:
        return valid, question

def get_choices():
    '''Function to retrieve choices from output.txt
    Arguments:
    None

    Returns:
    None
    '''
    choice_list = []
    final_list = []
    file = open('output.txt', 'r')
    # Iterate through file for choices
    for line in file:
        choice_list.append(line.replace('\n', ''))
    for i in choice_list:
        # Remove question and only input choices
        if '?' in i:
            choice_list = choice_list[choice_list.index(i) + 1:len(choice_list)]
    # Iterate through choices and only save real word choices
    for i in choice_list:
        temp = ''
        choice = i.split()
        for word in choice:
            temp += word + ' '
        temp = temp.lower()
        final_list.append(temp)
    # Remove empty string
    final_list = list(filter(None, final_list))
    return final_list
# Main
if __name__ == '__main__':
    main()
