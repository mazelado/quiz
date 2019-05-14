#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 7:55 AM

@author: matt


"""
import argparse
import sys
from typing import Any, List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_declarative import Question, FalseAnswer, Base, Quiz


def add_question(question, true_answer, false_answers) -> bool:
    pass


def remove_question(question) -> bool:
    pass


def print_quiz() -> None:
    """
    Prints all questions in the form of a quiz.

    :return: None
    """
    engine = create_engine('sqlite:///quiz.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    question_rows = session.query(Question).all()
    all_questions = []  # type: List[Any]

    for question_row in question_rows:  # type: Any
        false_answer_list = []  # type: List[str]
        false_answer_rows = session.query(FalseAnswer).filter(FalseAnswer.question == question_row).all()
        for false_answer_row in false_answer_rows:  # type: str
            false_answer_list.append(false_answer_row.answer)
        all_questions.append(Question(question_row.question, question_row.true_answer, false_answer_list))

    quiz = Quiz(all_questions)  # type: Quiz
    print(quiz)

    return


def main() -> None:
    parser = argparse.ArgumentParser(description='Create a quiz.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='Add a new question')
    group.add_argument('-r', '--remove', action='store_true', help='Remove an existing question')
    group.add_argument('-p', '--print', action='store_true', help='Print all questions')
    parser.add_argument('-q', '--question', type=str, help='Question (enclosed in quotes)')
    parser.add_argument('-t', '--true_answer', type=str, help='True answer (enclosed in quotes)')
    parser.add_argument('-f', '--false_answer', type=str, nargs='+',
                        help='False answer(s) (each answer enclosed in quotes)')
    args = parser.parse_args()

    # Print help message if no command line arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Process command line arguments add, remove, print
    if args.add:
        print('Question: ', args.question, '\nTrue: ', args.true_answer, '\nFalse: ', args.false_answer)
    elif args.remove:
        print('Question: ', args.question)
    elif args.print:
        print_quiz()

    return


if __name__ == '__main__':
    main()

    # TODO: Add CLI to delete a question
