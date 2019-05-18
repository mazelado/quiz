#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/14/19 2:01 PM

@author: matt
"""
import random
from string import ascii_uppercase
from typing import List, Any


class Question(object):
    """
    This is a class to define the questions, true answers, and false answers.
    """

    def __init__(self,
                 class_name,  # type: str
                 chapter,  # type: str
                 question,  # type: str
                 true_answer,  # type: str
                 false_answers,  # type: List[str]
                 ) -> None:
        """
        Initializes Question class

        :param class_name: name of class
        :param chapter: title of chapter
        :param question: text of question
        :param true_answer: text of true answer
        :param false_answers: list of text of incorrect answers
        """
        self.class_name = class_name  # type: str
        self.chapter = chapter  # type: str
        self.question = question  # type: str
        self.true_answer = true_answer  # type: str
        self.false_answers = false_answers  # type: List[str]

    def get_all_answers(self,
                        shuffle=False  # type: bool
                        ) -> List[str]:
        """
        Returns true and false answers, optionally shuffling them into random order

        :param shuffle: boolean True to shuffle, False (default) to leave unordered
        :return: list of text of all answers
        """
        r = [self.true_answer, *self.false_answers]  # type: List[str]
        if shuffle:
            self.shuffle_answers(r)

        return r

    @staticmethod
    def shuffle_answers(answers  # type: List[str]
                        ) -> List[str]:
        """
        STATIC METHOD
        Puts supplied answers into random order.
        
        :param answers: list of answers
        :return: list of supplied answers in random order
        """""
        if (len(answers) == 2) and ('True' in answers) and ('False' in answers):
            answers.sort(reverse=True)  # Leave T/F answers ordered
        else:
            random.shuffle(answers)  # Shuffle all other answers

        return answers

    def get_correct_letter_answer(self) -> str:
        """
        Returns correct letter answer.

        :return: String of correct letter answer
        """
        return ascii_uppercase[self.get_all_answers().index(self.true_answer)]

    def is_correct_answer(self,
                          answer  # type: str
                          ) -> bool:
        """
        Checks if specified answer matches true answer

        :param answer: string of specified answer
        :return: True if supplied answer matches true answer, False if not
        """
        return answer == self.true_answer

    def is_correct_letter_answer(self,
                                 letter  # type: str
                                 ) -> bool:
        """
        Checks specified letter answer against correct letter answer. Returns True if correct, False if incorrect.

        :param letter: String of letter answered
        :return: True if letter matches true answer, False if not
        """
        answer = self.get_all_answers()[ascii_uppercase.find(letter)]
        return self.is_correct_answer(answer)

    def __repr__(self) -> str:
        """
        Displays question, true answer in first position, and false answers in second+ positions

        :return: text of question and answers
        """
        # Construct return string r
        r = 'Class: {}\n'.format(self.class_name)  # type: str
        r += 'Chapter: {}\n'.format(self.chapter)
        r += '{}\n'.format(self.question + '\n')
        all_answers = self.get_all_answers(False)  # type: List[str]
        for index, answer in enumerate(all_answers):  # type: int, str
            # Mark correct answer
            if answer == self.true_answer:
                r += '   *'
            else:
                r += '    '

            # Add letter and answer
            r += '{}. {}\n'.format(ascii_uppercase[index], answer)

        return r


class Quiz(object):
    """
    This is a class that is a collection of Question objects and additional methods to create a quiz.
    """

    def __init__(self,
                 questions  # type: List[Any]
                 ) -> None:
        """
        Initializes Quiz class

        :param questions: list of selected Question objects
        """
        self.correct = 0  # type: int
        self.incorrect = 0  # type: int
        self.questions = questions  # type: List[Any]
        random.shuffle(self.questions)

    def select_question_subset(self,
                               count  # type: int
                               ) -> List[Any]:
        """
        Returns a subset of Question objects in a list. If count is larger than the number of questions available,
        returns all questions.

        :param count: Number of questions to return
        :return: List of Question objects
        """
        random.shuffle(self.questions)
        return self.questions[0:min(count, len(self.questions))]

    @staticmethod
    def ask_user_for_answer(question  # type: Question
                            ) -> str:
        """
        Asks user to input an answer and sanitizes input

        :param question: Question object to check valid answers
        :return: string of answer
        """
        possible_answers = ascii_uppercase[0:len(question.false_answers)]
        while True:
            response = input('Answer: ').upper()
            # Expecting a single letter, within group of possible answers
            if (len(response) == 1) and (response in possible_answers):
                return response
            else:
                print('Invalid answer. Try again.\n')

    def show_current_results(self) -> str:
        """
        Returns string of current questions answered, % correct, and % incorrect

        :return: String of results
        """
        answered = self.correct + self.incorrect  # type: int
        pct_correct = round(self.correct / (self.correct + self.incorrect), 3) * 100  # tyoe: float
        pct_incorrect = round(self.incorrect / (self.correct + self.incorrect), 3) * 100  # type: float
        return '{} questions answered, {}% correct, {}% incorrect.'.format(answered, pct_correct, pct_incorrect)

    @staticmethod
    def ask_user_to_continue() -> bool:
        """
        STATIC METHOD
        Asks user if they want to continue and returns boolean

        :return: True if user wants to continue, False if user wants to stop
        """
        response = input('Continue? [YES/no]: ').upper()  # type: str
        if ('Y' in response) or (response == ''):
            return True
        else:
            return False

    def take_quiz(self,
                  ask_for_more=False,  # type: bool
                  number_of_questions=None,  # type: int
                  min_score_percent=None  # type: int
                  ) -> None:
        """
        Take a quiz

        :param ask_for_more: True to ask to continue after each question, False (default)
        :param number_of_questions: Number of questions to ask to complete quiz
        :param min_score_percent: Minimum score required to complete quiz
        :return: None
        """
        self.correct = 0
        self.incorrect = 0

        # How many questions? (ask after each? fixed number? minimum score?)
        more_questions = True
        if ask_for_more:  # Ask if user wants to continue after each question
            while more_questions:
                for q in self.select_question_subset(1):  # type: Question
                    print(q)
                    # Get answer from user
                    user_response = self.ask_user_for_answer(q)
                    # Check answer, show result
                    if q.is_correct_letter_answer(user_response):
                        self.correct += 1
                        print('Correct!\n')
                    else:
                        self.incorrect += 1
                        print('Incorrect. The correct answer is {}.\n'.format(q.get_correct_letter_answer()))
                    print(self.show_current_results())
                more_questions = self.ask_user_to_continue()
        elif number_of_questions is not None:  # Ask a fixed number of questions
            # Select n questions (no repeats)
            # Loop through questions
            #   Display question
            #   Get answer from user
            #   Check answer
            # Show final results
            pass
        elif min_score_percent is not None:  # Ask questions until a given score is reached
            # Loop
            #   Select a question
            #   Display question
            #   Get answer from user
            #   Check answer
            #   Show result
            # Score >= min? -> If no, repeat loop
            # If yes, show final results
            pass

        # Show final results

        return None

    def __repr__(self) -> str:
        """
        Displays all questions in random order, with answers in random order (except T/F)

        :return: text of all questions
        """
        r = ''  # type: str
        for q_index, question in enumerate(self.questions):  # type: int, Question
            r += 'Class: {}\n'.format(question.class_name)
            r += 'Chapter: {}\n'.format(question.chapter)
            r += '{}. {}\n'.format(str(q_index + 1), question.question)
            all_answers = question.get_all_answers()  # type: List[str]
            for a_index, answer in enumerate(all_answers):  # type: int, str
                r += '    {}. {}\n'.format(ascii_uppercase[a_index], answer)
            r += '\n'

        return r
