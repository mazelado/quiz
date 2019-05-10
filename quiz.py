#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 7:55 AM

@author: matt
"""
import random
from string import ascii_uppercase
from typing import Any, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import db_declarative


class Question(object):
    def __init__(self,
                 question,  # type: str
                 true_answer,  # type: str
                 false_answers,  # type: List[str]
                 ) -> None:
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


class Quiz(object):
    def __init__(self,
                 questions  # type: List[Any]
                 ) -> None:
        self.correct = 0  # type: int
        self.incorrect = 0  # type: int
        self.questions = questions  # type: List[Any]
        random.shuffle(self.questions)

    def __repr__(self) -> str:
        r = ''  # type: str
        for q_index, question in enumerate(self.questions):  # type: int, Question
            r += str(q_index + 1) + '. ' + question.getQuestion() + '\n'
            for a_index, answer in enumerate(question.getAllAnswers()):  # type: int, str
                r += '    ' + ascii_uppercase[a_index] + '. ' + answer + '\n'
            r += '\n'

        return r


def main() -> None:
    engine = create_engine('sqlite:///quiz.db')
    db_declarative.Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    question_rows = session.query(db_declarative.Question).all()
    all_questions = []  # type: List[Any]

    for question_row in question_rows:  # type: Any
        false_answer_list = []  # type: List[str]
        false_answer_rows = session.query(db_declarative.FalseAnswer).filter(
            db_declarative.FalseAnswer.question == question_row).all()
        for false_answer_row in false_answer_rows:  # type: str
            false_answer_list.append(false_answer_row.answer)
        all_questions.append(Question(question_row.question, question_row.true_answer, false_answer_list))

    quiz = Quiz(all_questions)  # type: Quiz
    print(quiz)


if __name__ == '__main__':
    main()
