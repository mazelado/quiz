#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 2:29 PM

@author: matt
"""
import random
from string import ascii_uppercase
from typing import List, Any

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Question(Base):
    """
    This is a class to define the Question database table.

    Contains the question and correct answer. See the FalseAnswer table for the incorrect answers.
    """
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    true_answer = Column(String(250), nullable=False)

    def __init__(self,
                 question,  # type: str
                 true_answer,  # type: str
                 false_answers,  # type: List[str]
                 ) -> None:
        """
        Args:
            question: text of question
            true_answer: text of the correct answer to the question
            false_answers: list of text of incorrect answers to the question
        """
        self.question = question  # type: str
        self.true_answer = true_answer  # type: str
        self.false_answers = false_answers  # type: List[str]

    def getQuestion(self) -> str:
        return self.question

    def getTrueAnswer(self) -> str:
        return self.true_answer

    def getFalseAnswers(self) -> List[str]:
        return self.false_answers

    def getAllAnswers(self) -> List[str]:
        r = [self.true_answer, *self.false_answers]  # type: List[str]
        self.shuffleAnswers(r)

        return r

    def shuffleAnswers(self,
                       answers  # type: List[str]
                       ) -> List[str]:
        """
        Args:
            answers: joined list of both true and false answers to the question
        """
        if (len(answers) == 2) and ('True' in answers) and ('False' in answers):
            answers.sort(reverse=True)  # Leave T/F answers unshuffled
        else:
            random.shuffle(answers)  # Shuffle all other answers

        return answers

    def __repr__(self) -> str:
        all_answers = [self.true_answer, *self.false_answers]  # type: List[str]
        self.shuffleAnswers(all_answers)

        # Construct return string r
        r = '%s\n' % self.question  # type: str
        for index, answer in enumerate(all_answers):  # type: int, str
            # Mark correct answer
            if answer == self.true_answer:
                r += '   *'
            else:
                r += '    '

            # Add letter and answer
            r += ascii_uppercase[index] + '. ' + answer + '\n'

        return r


class FalseAnswer(Base):
    """
    This is a class to define the FalseAnswer database table.

    Uses a one-to-many relationship from the Question table to multiple rows in the FalseAnswer table.
    """
    __tablename__ = 'false_answer'
    id = Column(Integer, primary_key=True)
    answer = Column(String(250))
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship(Question)


class Quiz(object):
    """This is a class that is a collection of Question objects and additional
    methods to create a quiz.
    """

    def __init__(self,
                 questions  # type: List[Any]
                 ) -> None:
        """
        Args:
            questions: list of Question objects
        """
        self.correct = 0  # type: int
        self.incorrect = 0  # type: int
        self.questions = questions  # type: List[Any]
        random.shuffle(self.questions)

    def __repr__(self) -> str:
        """Displays all questions in random order, with answers in random order
        (except T/F)

        Returns:
            text of all questions
        """
        r = ''  # type: str
        for q_index, question in enumerate(self.questions):  # type: int, Question
            r += str(q_index + 1) + '. ' + question.getQuestion() + '\n'
            for a_index, answer in enumerate(question.getAllAnswers()):  # type: int, str
                r += '    ' + ascii_uppercase[a_index] + '. ' + answer + '\n'
            r += '\n'

        return r


engine = create_engine('sqlite:///quiz.db')

Base.metadata.create_all(engine)
