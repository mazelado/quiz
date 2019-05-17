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
        self.set_class_name(class_name)
        self.set_chapter(chapter)
        self.set_question(question)
        self.set_true_answer(true_answer)
        self.set_false_answers(false_answers)

    def get_class_name(self) -> str:
        """
        Returns class name

        :return: text of class name
        """
        return self.class_name

    def set_class_name(self,
                       new_class_name  # type: str
                       ) -> None:
        """
        Sets name of class, overwriting existing

        :param new_class_name: text of new class name
        :return: None
        """
        self.class_name = new_class_name
        return None

    def get_chapter(self) -> str:
        """
        Returns chapter

        :return: text of chapter
        """
        return self.chapter

    def set_chapter(self,
                    new_chapter_name  # type: str
                    ) -> None:
        """
        Sets chapter, overwriting existing

        :param new_chapter_name: text of new chapter
        :return: None
        """
        self.chapter = new_chapter_name
        return None

    def get_question(self) -> str:
        """
        Returns question

        :return: text of question
        """
        return self.question

    def set_question(self,
                     new_question  # type: str
                     ) -> None:
        """
        Sets question, overwriting existing

        :param new_question: text of new question
        :return: None
        """
        self.question = new_question
        return None

    def get_true_answer(self) -> str:
        """
        Returns true answer

        :return: text of true answer
        """
        return self.true_answer

    def set_true_answer(self,
                        new_true_answer  # type: str
                        ) -> None:
        """
        Sets true answer, overwriting existing

        :param new_true_answer: text of new true answer
        :return: None
        """
        self.true_answer = new_true_answer
        return None

    def get_false_answers(self,
                          shuffle=False  # type: bool
                          ) -> List[str]:
        """
        Returns false answers, optionally shuffling them into random order

        :param shuffle: boolean True to shuffle false answers, False (default) to leave false answers unordered
        :return: list of text of false answers
        """
        if shuffle:
            return self.shuffle_answers(self.false_answers)
        else:
            return self.false_answers

    def set_false_answers(self,
                          new_false_answers  # type: List[str]
                          ) -> None:
        """
        Sets false answers, overwriting existing

        :param new_false_answers: list of text of new false answers
        :return: None
        """
        self.false_answers = new_false_answers
        return None

    def add_false_answer(self,
                         new_false_answer  # type: str
                         ) -> None:
        """
        Adds a false answer

        :param new_false_answer: text of false answer to add
        :return: None
        """
        self.false_answers.append(new_false_answer)
        return None

    def remove_false_answer(self,
                            false_answer_to_remove  # type: str
                            ) -> bool:
        """
        Removes a false answer

        :param false_answer_to_remove: text of false answer to remove
        :return: True if successful, False if unsuccessful
        """
        if false_answer_to_remove in self.false_answers:
            self.false_answers.remove(false_answer_to_remove)
            return True
        else:
            return False

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

    def __repr__(self) -> str:
        """
        Displays question, true answer in first position, and false answers in second+ positions

        :return: text of question and answers
        """
        # Construct return string r
        r = 'Class: ' + self.get_class_name() + '\n'
        r += 'Chapter: ' + self.get_chapter() + '\n'
        r += self.get_question() + '\n'  # type: str
        all_answers = self.get_all_answers(False)  # type: List[str]
        for index, answer in enumerate(all_answers):  # type: int, str
            # Mark correct answer
            if answer == self.true_answer:
                r += '   *'
            else:
                r += '    '

            # Add letter and answer
            r += ascii_uppercase[index] + '. ' + answer + '\n'

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

    def __repr__(self) -> str:
        """
        Displays all questions in random order, with answers in random order (except T/F)

        :return: text of all questions
        """
        r = ''  # type: str
        for q_index, question in enumerate(self.questions):  # type: int, Question
            r += 'Class: ' + question.get_class_name() + '\n'  # type: str
            r += 'Chapter: ' + question.get_chapter() + '\n'
            r += str(q_index + 1) + '. ' + question.get_question() + '\n'
            all_answers = question.get_all_answers()  # type: List[str]
            for a_index, answer in enumerate(all_answers):  # type: int, str
                r += ' ' * 4 + ascii_uppercase[a_index] + '. ' + answer + '\n'
            r += '\n'

        return r
