#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/14/19 2:01 PM

@author: matt
"""
import random
from string import ascii_uppercase
from typing import List


class Question(object):
    """
    This is a class to define the questions, true answers, and false answers.
    """

    def __init__(self,
                 class_name: str,
                 chapter: str,
                 question: str,
                 true_answer: str,
                 false_answers: List[str]
                 ) -> None:
        """
        Initializes Question class

        :param class_name: name of class
        :param chapter: title of chapter
        :param question: text of question
        :param true_answer: text of true answer
        :param false_answers: list of text of incorrect answers
        """
        self.class_name: str = class_name
        self.chapter: str = chapter
        self.question: str = question
        self.true_answer: str = true_answer
        self.false_answers: List[str] = false_answers

    def get_all_answers(self,
                        shuffle: bool = False
                        ) -> List[str]:
        """
        Returns true and false answers, optionally shuffling them into random order

        :param shuffle: boolean True to shuffle, False (default) to leave unordered
        :return: list of text of all answers
        """
        r: List[str] = [self.true_answer, *self.false_answers]
        if shuffle:
            self.shuffle_answers(r)

        return r

    @staticmethod
    def shuffle_answers(answers: List[str]
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
                          answer: str
                          ) -> bool:
        """
        Checks if specified answer matches true answer

        :param answer: string of specified answer
        :return: True if supplied answer matches true answer, False if not
        """
        return answer == self.true_answer

    def is_correct_letter_answer(self,
                                 letter: str
                                 ) -> bool:
        """
        Checks specified letter answer against correct letter answer. Returns True if correct, False if incorrect.

        :param letter: String of letter answered
        :return: True if letter matches true answer, False if not
        """
        answer: str = self.get_all_answers()[ascii_uppercase.find(letter)]
        return self.is_correct_answer(answer)

    def __repr__(self) -> str:
        """
        Displays question, true answer in first position, and false answers in second+ positions

        :return: text of question and answers
        """
        # Construct return string r
        r: str = 'Class: {:s}\nChapter: {:s}\n{:s}\n\n'.format(self.class_name,
                                                               self.chapter,
                                                               self.question)
        all_answers: List[str] = self.get_all_answers(False)
        index: int
        answer: str
        for index, answer in enumerate(all_answers):
            # Mark correct answer
            if answer == self.true_answer:
                r += '   *'
            else:
                r += '    '

            # Add letter and answer
            r += '{:s}. {:s}\n'.format(ascii_uppercase[index], answer)

        return r
