#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/14/19 2:01 PM

@author: matt
"""
import random
from string import ascii_uppercase
from typing import List

from quiz_cli.Question import Question


class Quiz(object):
    """
    This is a class that is a collection of Question objects and additional methods to create a quiz_cli.
    """

    def __init__(self,
                 questions: List[Question]
                 ) -> None:
        """
        Initializes Quiz class

        :param questions: list of selected Question objects
        """
        self.correct: int = 0
        self.incorrect: int = 0
        self.questions: List[Question] = questions
        random.shuffle(self.questions)

    def select_question_subset(self,
                               count: int
                               ) -> List[Question]:
        """
        Returns a subset of Question objects in a list. If count is larger than the number of questions available,
        returns all questions.

        :param count: Number of questions to return
        :return: List of Question objects
        """
        # Shuffle questions and answers
        random.shuffle(self.questions)

        start: int = 0
        stop: int = min(count, len(self.questions))
        return self.questions[start:stop]

    @staticmethod
    def print_question(question: Question
                       ) -> str:
        """
        STATIC METHOD
        Prints question and returns the letter of the correct answer.

        :param question: Question object
        :return: string of letter of correct answer
        """
        correct_answer: str

        r: str = 'Class: {:s}\nChapter: {:s}\n{:s}\n\n'.format(question.class_name,
                                                               question.chapter,
                                                               question.question)
        all_answers: List[str] = question.get_all_answers(shuffle=True)
        index: int
        answer: str
        for index, answer in enumerate(all_answers):
            r += '{:>4s}. {:s}\n'.format(ascii_uppercase[index], answer)
            if answer == question.true_answer:
                correct_answer = ascii_uppercase[index]

        print(r)

        return correct_answer

    @staticmethod
    def ask_user_for_answer(question: Question
                            ) -> str:
        """
        Asks user to input an answer and sanitizes input

        :param question: Question object to check valid answers
        :return: string of answer
        """
        start: int = 0
        stop: int = len(question.false_answers) + 1
        possible_answers: str = ascii_uppercase[start:stop]
        while True:
            response: str = input('Answer: ').upper()
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
        answered: int = self.correct + self.incorrect
        pct_correct: float = self.correct / (self.correct + self.incorrect) * 100
        pct_incorrect: float = self.incorrect / (self.correct + self.incorrect) * 100
        return '{:d} questions answered, {:.1f}% correct, {:.1f}% incorrect.'.format(answered, pct_correct,
                                                                                     pct_incorrect)

    @staticmethod
    def ask_user_to_continue() -> bool:
        """
        STATIC METHOD
        Asks user if they want to continue and returns boolean

        :return: True if user wants to continue, False if user wants to stop
        """
        response: str = input('Continue? [YES/no]: ').upper()
        if ('Y' in response) or (response == ''):
            return True
        else:
            return False

    def check_answer(self,
                     correct_answer: str,
                     user_response: str
                     ) -> bool:
        """
        Checks user response against correct answer and increments counters.

        :param correct_answer: Correct answer
        :param user_response: User response
        :return: True if user response is correct, False otherwise
        """
        if correct_answer == user_response:
            self.correct += 1
            print('Correct!\n')
        else:
            self.incorrect += 1
            print('Incorrect. The correct answer is {:s}.\n'.format(correct_answer))

        return correct_answer == user_response

    def take_quiz(self,
                  ask_for_more: bool = False,
                  number_of_questions: int = None
                  ) -> None:
        """
        Take a quiz_cli

        :param ask_for_more: True to ask to continue after each question, False (default)
        :param number_of_questions: Number of questions to ask to complete quiz_cli
        :return: None
        """
        self.correct = 0
        self.incorrect = 0

        more_questions: bool = True
        q: Question
        correct_answer: str
        user_response: str
        if ask_for_more:  # Ask if user wants to continue after each question
            while more_questions:
                for q in self.select_question_subset(1):
                    correct_answer = self.print_question(question=q)
                    user_response = self.ask_user_for_answer(q)
                    self.check_answer(correct_answer=correct_answer,
                                      user_response=user_response)
                    print(self.show_current_results())
                more_questions = self.ask_user_to_continue()
        elif number_of_questions is not None:  # Ask a fixed number of questions
            for q in self.select_question_subset(number_of_questions):
                correct_answer = self.print_question(question=q)
                user_response = self.ask_user_for_answer(q)
                self.check_answer(correct_answer=correct_answer,
                                  user_response=user_response)
            print(self.show_current_results())

        return None

    def __repr__(self) -> str:
        """
        Displays all questions in random order, with answers in random order (except T/F)

        :return: text of all questions
        """
        q_index: int
        question: Question
        r: str = ''
        for q_index, question in enumerate(self.questions):
            r += 'Class: {:s}\nChapter: {:s}\n{:s}. {:s}\n'.format(question.class_name,
                                                                   question.chapter,
                                                                   str(q_index + 1),
                                                                   question.question)
            all_answers: List[str] = question.get_all_answers()
            a_index: int
            answer: str
            for a_index, answer in enumerate(all_answers):
                r += '    {:s}. {:s}\n'.format(ascii_uppercase[a_index], answer)
            r += '\n'

        return r
