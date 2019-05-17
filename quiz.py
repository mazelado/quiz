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
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from class_declarative import Question, Quiz
from db_declarative import ClassTable, ChapterTable, QuestionTable, FalseAnswersTable, Base


def start_session() -> sessionmaker:
    """
    Opens a database session.

    :return: DB session
    """
    engine = create_engine('sqlite:///quiz.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.bind = engine
    session = DBSession()

    return session


def end_session(session  # type: sessionmaker
                ) -> bool:
    """
    Closes database session.

    :param session: DB session
    :return: True
    """

    session.close()
    return True


def add_question(session,  # type: sessionmaker
                 class_name,  # type: str
                 chapter,  # type: str
                 question,  # type: str
                 true_answer,  # type: str
                 false_answers  # type: List[str]
                 ) -> bool:
    """
    Adds a question to the database.

    :param session: DB session
    :param class_name: text of class
    :param chapter: text of chapter
    :param question: text of question
    :param true_answer: text of true answer
    :param false_answers: list of text of false answers
    :return: True if database commit is successful
    """

    new_question = Question(class_name=class_name,
                            chapter=chapter,
                            question=question,
                            true_answer=true_answer,
                            false_answers=false_answers)

    # Try to add new class, reuse if it exists
    new_class = ClassTable(class_name=new_question.get_class_name())
    try:
        session.add(new_class)
        session.commit()
    except (IntegrityError, InvalidRequestError):  # UNIQUE constraint failed, already exists in table
        session.rollback()
        new_class = session.query(ClassTable).filter(ClassTable.class_name == q.get_class_name()).one()

    # Try to add new chapter, reuse if it exists
    new_chapter = ChapterTable(chapter=new_question.get_chapter(), class_name=new_class)
    try:
        session.add(new_chapter)
        session.commit()
    except (IntegrityError, InvalidRequestError):  # UNIQUE constraint failed, already exists in table
        session.rollback()
        new_chapter = session.query(ChapterTable).filter(ChapterTable.chapter == q.get_chapter()).one()

    new_row = QuestionTable(question=new_question.get_question(), true_answer=q.get_true_answer(), chapter=new_chapter)
    session.add(new_row)
    session.commit()
    for f in new_question.get_false_answers():
        new_false_answer = FalseAnswersTable(answer=f, question=new_row)
        session.add(new_false_answer)
        session.commit()

    return True


def remove_question(session,  # type: sessionmaker
                    question  # type: str
                    ) -> bool:
    """
    Removes a question from the database.

    :param session: DB session
    :param question: question to remove
    :return: True if successful, False if not
    """

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

        return True


def print_quiz(session) -> None:
    """
    Prints all questions in the form of a quiz.

    :param session: DB session
    :return: True
    """

    question_rows = session.query(QuestionTable).all()
    all_questions = []  # type: List[Any]

    for question_row in question_rows:  # type: Any
        false_answer_list = []  # type: List[str]
        false_answer_rows = session.query(FalseAnswersTable).filter(FalseAnswersTable.question == question_row).all()
        for false_answer_row in false_answer_rows:  # type: FalseAnswersTable
            false_answer_list.append(false_answer_row.answer)
        all_questions.append(Question(class_name=question_row.chapter.class_name.class_name,
                                      chapter=question_row.chapter.chapter,
                                      question=question_row.question,
                                      true_answer=question_row.true_answer,
                                      false_answers=false_answer_list))

    quiz = Quiz(all_questions)  # type: Quiz
    print(quiz)

    return True


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
    parser.add_argument('-c', '--class', type=str, help='Class (enclosed in quotes)')
    parser.add_argument('-C', '--chapter', type=str, help='Chapter (enclosed in quotes)')
    parser.add_argument('-q', '--question', type=str, help='Question (enclosed in quotes)')
    parser.add_argument('-t', '--true_answer', type=str, help='True answer (enclosed in quotes)')
    parser.add_argument('-f', '--false_answers', type=str, nargs='+',
                        help='False answer(s) (each answer enclosed in quotes)')
    args = parser.parse_args()

    # Print help message if no command line arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    session = start_session()

    # Process command line arguments add, remove, print
    if args.add:
        if add_question(session, args.class_, args.chapter, args.question, args.true_answer, args.false_answers):
            print('Question added successfully.')
        else:
            print('Unable to add question.')
    elif args.remove:
        if remove_question(session, args.question):
            print('Question removed successfully.')
        else:
            print('Unable to remove question.')
    elif args.print:
        print_quiz(session)

    end_session(session)

    return


def main() -> None:
    cli_arguments()


if __name__ == '__main__':
    main()
