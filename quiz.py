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
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from class_declarative import Question, Quiz
from db_declarative import QuestionTable, FalseAnswersTable, Base


def start_session() -> sessionmaker:
    engine = create_engine('sqlite:///quiz.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    return session


def end_session(session  # type: sessionmaker
                ) -> bool:
    session.close()


def add_question(question,  # type: str
                 true_answer,  # type: str
                 false_answers  # type: List[str]
                 ) -> bool:
    """
    Adds a question to the database.

    :param question: text of question
    :param true_answer: text of true answer
    :param false_answers: list of text of false answers
    :return: True if database commit is successful
    """
    session = start_session()

    new_question = Question(question, true_answer, false_answers)
    new_row = QuestionTable(question=new_question.getQuestion(), true_answer=new_question.getTrueAnswer())
    session.add(new_row)
    session.commit()
    for f in new_question.getFalseAnswers():
        new_false_answer = FalseAnswersTable(answer=f, question=new_row)
        session.add(new_false_answer)
        session.commit()

    end_session(session)

    return True


def remove_question(question  # type: str
                    ) -> bool:
    session = start_session()

    try:
        question_rows = session.query(QuestionTable).filter(QuestionTable.question == question).one()
    except NoResultFound:
        print('ERROR: Question not found.')
        end_session(session)
        return False
    except MultipleResultsFound:
        print('ERROR: Multiple questions found.')
        end_session(session)
        return False
    else:
        session.delete(question_rows)
        session.commit()

        # Are all false answers also deleted?

        end_session(session)
        return True


def print_quiz() -> None:
    """
    Prints all questions in the form of a quiz.

    :return: None
    """
    session = start_session()

    question_rows = session.query(QuestionTable).all()
    all_questions = []  # type: List[Any]

    for question_row in question_rows:  # type: Any
        false_answer_list = []  # type: List[str]
        false_answer_rows = session.query(FalseAnswersTable).filter(FalseAnswersTable.question == question_row).all()
        for false_answer_row in false_answer_rows:  # type: str
            false_answer_list.append(false_answer_row.answer)
        all_questions.append(Question(question_row.question, question_row.true_answer, false_answer_list))

    end_session(session)

    quiz = Quiz(all_questions)  # type: Quiz
    print(quiz)

    return


def cli_arguments() -> None:
    """
    Parse command line interface arguments are call methods as necessary.

    :return:
    """
    parser = argparse.ArgumentParser(description='Create a quiz.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-a', '--add', action='store_true', help='Add a new question')
    group.add_argument('-r', '--remove', action='store_true', help='Remove an existing question')
    group.add_argument('-p', '--print', action='store_true', help='Print all questions')
    parser.add_argument('-q', '--question', type=str, help='Question (enclosed in quotes)')
    parser.add_argument('-t', '--true_answer', type=str, help='True answer (enclosed in quotes)')
    parser.add_argument('-f', '--false_answers', type=str, nargs='+',
                        help='False answer(s) (each answer enclosed in quotes)')
    args = parser.parse_args()

    # Print help message if no command line arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Process command line arguments add, remove, print
    if args.add:
        if add_question(args.question, args.true_answer, args.false_answers):
            print('Question added successfully.')
        else:
            print('Unable to add question.')
    elif args.remove:
        if remove_question(args.question):
            print('Question removed successfully.')
        else:
            print('Unable to remove question.')
    elif args.print:
        print_quiz()

    return


def main() -> None:
    cli_arguments()


if __name__ == '__main__':
    main()
