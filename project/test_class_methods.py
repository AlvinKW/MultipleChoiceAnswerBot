"""
Alvin Kwan
Class: CS 521 - Fall 2
Date: December 17, 2020
CS521 Project
Unit Test
The project is designed to answer multiple choice questions through gathering
data from Google and basing off of the frequencies of the choices.
"""
import unittest
from computing import Search

class TestSearch(unittest.TestCase):
    '''
    Class for unit testing modules from computing.py
    '''
    def test_calculate_score(self):
        '''
        Function to test calculate_score() single words
        '''
        test = Search('', 'apple orange grape', ['apple', 'orange', 'grape'])
        test_score = {'apple':5, 'orange':10, 'grape':20}
        self.assertEqual(test.calculate_score(test_score),
                         {'apple':5, 'orange':10, 'grape':20})

    def test_calculate_score_multiwords(self):
        '''
        Function to test calculate_score() multiwords
        '''
        test = Search('', 'Elon Musk Jeff Bezos  Tim Apple',
                      ['Elon Musk', 'Jeff Bezos', 'Tim Apple'])
        test_score = {'Elon': 10, 'Musk': 20, 'Jeff': 30, 'Bezos': 40, 'Tim': 50,
                      'Apple': 60}
        self.assertEqual(test.calculate_score(test_score),
                         {'Elon Musk': 30, 'Jeff Bezos': 70, 'Tim Apple': 110})

    def test_print_choice(self):
        '''
        Function to test print_choice
        '''
        test = Search('', 'apple orange grape', ['apple', 'orange', 'grape'])
        self.assertEqual(test.print_choice(),
                         ('Multiple Choices: \n', {'apple': 0, 'orange': 0, 'grape': 0}))

    def test_print_result(self):
        '''
        Function to test print_result()
        '''
        test = Search('', 'apple orange grape', ['apple', 'orange', 'grape'])
        dash = '\n' + '-'*55
        output = "Multiple Choices: \n"
        msg = '\nError: answer cannot be determined'
        result = output + msg + dash
        self.assertEqual(test.print_result(), result)

    def test_repr(self):
        '''
        Function to test __repr__()
        '''
        test = Search('This is a question', 'apple orange grape',
                      ['apple', 'orange', 'grape'])
        self.assertEqual(test.__repr__(), "\'This is a question?\'")

if __name__ == '__main__':
    unittest.main()
    