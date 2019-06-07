#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 7:55 AM

@author: matt
"""
import argparse
import logging
import sys
from argparse import ArgumentParser, Namespace
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from sqlalchemy.orm.session import sessionmaker

from quiz_cli.Question import Question
from quiz_cli.Quiz import Quiz
from quiz_cli.db_declarative import ClassTable, ChapterTable, QuestionTable, FalseAnswersTable, Base


def start_session() -> Session:
    """
    Opens a database session.

    :return: DB session
    """
    engine = create_engine('sqlite:///quiz.db')
    Base.metadata.bind = engine
    DBSession = sessionmaker()
    DBSession.configure(bind=engine)
    session = DBSession()

    return session


def end_session(session: Session
                ) -> None:
    """
    Closes database session.

    :param session: DB session
    :return: True
    """

    session.close()
    return None


def add_question(session: Session,
                 class_name: str,
                 chapter: str,
                 question: str,
                 true_answer: str,
                 false_answers: List[str]
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
    # Validate parameters
    if (not session) or (not class_name) or (not chapter) or (not question) or (not true_answer) or (not false_answers):
        raise SystemExit

    new_question: Question = Question(class_name=class_name,
                                      chapter=chapter,
                                      question=question,
                                      true_answer=true_answer,
                                      false_answers=false_answers)

    # Try to add new class, reuse if it exists
    new_class: ClassTable = ClassTable(class_name=new_question.class_name)
    try:
        session.add(new_class)
        session.commit()
    except (IntegrityError, InvalidRequestError):  # UNIQUE constraint failed, already exists in table
        logging.warning('IntegrityError or InvalidRequestError - class already exists in ClassTable')
        session.rollback()
        new_class = session.query(ClassTable).filter(ClassTable.class_name == new_question.class_name).one()

    # Try to add new chapter, reuse if it exists
    new_chapter: ChapterTable = ChapterTable(chapter=new_question.chapter, class_name=new_class)
    try:
        session.add(new_chapter)
        session.commit()
    except (IntegrityError, InvalidRequestError):  # UNIQUE constraint failed, already exists in table
        logging.warning('IntegrityError or InvalidRequestError - chapter already exists in ChapterTable')
        session.rollback()
        new_chapter = session.query(ChapterTable).filter(ChapterTable.chapter == new_question.chapter).one()

    new_row: QuestionTable = QuestionTable(question=new_question.question, true_answer=new_question.true_answer,
                                           chapter=new_chapter)
    session.add(new_row)
    session.commit()

    for f in new_question.false_answers:
        new_false_answer: FalseAnswersTable = FalseAnswersTable(answer=f, question=new_row)
        session.add(new_false_answer)
        session.commit()

    return True


def delete_question(session: Session,
                    question: str
                    ) -> bool:
    """
    Deletes a question from the database. Does not remove orphans classes or chapters.

    :param session: DB session
    :param question: question to delete
    :return: True if successful, False if not
    """

    try:
        query: Session = session.query(QuestionTable).filter(QuestionTable.question == question)
        question_rows: List[QuestionTable] = query.one()
    except NoResultFound:
        logging.error('Question not found.')
        end_session(session)
        return False
    except MultipleResultsFound:
        logging.error('Multiple questions found.')
        end_session(session)
        return False
    else:
        session.delete(question_rows)
        session.commit()

        return True


def question_table_to_list(session: Session,
                           question_rows: List[QuestionTable]
                           ) -> List[Question]:
    """
    Converts QuestionTable rows from query to a list of Question objects.

    :param session: DB session
    :param question_rows: QuestionTable rows from query
    :return: list of Question objects
    """
    all_questions: List[Question] = []
    for question_row in question_rows:
        query: Session = session.query(FalseAnswersTable).filter(FalseAnswersTable.question == question_row)
        false_answer_rows: List[FalseAnswersTable] = query.all()
        false_answer_list: List[str] = []
        for false_answer_row in false_answer_rows:
            false_answer_list.append(false_answer_row.answer)
        all_questions.append(Question(class_name=question_row.chapter.class_name.class_name,
                                      chapter=question_row.chapter.chapter,
                                      question=question_row.question,
                                      true_answer=question_row.true_answer,
                                      false_answers=false_answer_list))

    return all_questions


def get_questions_from_db(session: Session,
                          class_name: str = None,
                          chapter: str = None
                          ) -> List[Question]:
    """
    Retrieves rows from QuestionTable, filtering by class name and chapter.

    :param session: DB session
    :param class_name: string of class name
    :param chapter: string of chapter
    :return: list of Question objects
    """
    # Set up query
    query: Query = session.query(QuestionTable)
    if class_name is not None:
        query = query.filter(QuestionTable.chapter.class_name == class_name)
    if chapter is not None:
        query = query.filter(QuestionTable.chapter == chapter)
    question_rows: List[QuestionTable] = query.all()

    all_questions: List[Question] = question_table_to_list(session=session,
                                                           question_rows=question_rows)

    return all_questions


def print_quiz(session: Session,
               class_name: str,
               chapter: str
               ) -> None:
    """
    Prints all questions in the form of a quiz_cli.
    
    :param session: DB session 
    :param class_name: string of class_name
    :param chapter: string of chapter
    :return: None
    """
    all_questions: List[Question] = get_questions_from_db(session=session,
                                                          class_name=class_name,
                                                          chapter=chapter)

    quiz: Quiz = Quiz(all_questions)
    print(quiz)

    return


def take_quiz_number_of_questions(session: Session,
                                  class_name: str,
                                  chapter: str,
                                  number_of_questions: int
                                  ) -> None:
    """
    Take a quiz_cli with a fixed number of questions.

    :param session: DB session
    :param class_name: string of class name
    :param chapter: string of chapter
    :param number_of_questions: int of number of questions to ask
    :return: None
    """
    all_questions: List[Question] = get_questions_from_db(session=session,
                                                          class_name=class_name,
                                                          chapter=chapter)

    quiz: Quiz = Quiz(all_questions)
    quiz.take_quiz(number_of_questions=number_of_questions)

    return


def take_quiz_keep_asking(session: Session,
                          class_name: str,
                          chapter: str
                          ) -> None:
    """
    Take a quiz_cli, asking to continue after each question.

    :param session: DB session
    :param class_name: string of class name
    :param chapter: string of chapter
    :return: None
    """
    all_questions: List[Question] = get_questions_from_db(session=session,
                                                          class_name=class_name,
                                                          chapter=chapter)

    quiz: Quiz = Quiz(all_questions)
    quiz.take_quiz(ask_for_more=True)

    return


def cli_arguments() -> None:
    """
    Parse command line interface arguments are call methods as necessary.

    :return:
    """
    # Parser setup
    parser: ArgumentParser = argparse.ArgumentParser(description='Create a quiz.')
    group_1 = parser.add_mutually_exclusive_group()
    group_1.add_argument('-a', '--add', action='store_true', help='add a new question')
    group_1.add_argument('-r', '--remove', action='store_true', help='remove an existing question')
    group_1.add_argument('-p', '--print', action='store_true', help='print all questions')
    group_1.add_argument('-z', '--quiz', action='store_true', help='take a quiz')
    parser.add_argument('-c', '--class', type=str, dest='class_', help='class (enclosed in quotes)')
    parser.add_argument('-C', '--chapter', type=str, help='chapter (enclosed in quotes)')
    parser.add_argument('-q', '--question', type=str, help='question (enclosed in quotes)')
    parser.add_argument('-t', '--true_answer', type=str, help='true answer (enclosed in quotes)')
    parser.add_argument('-f', '--false_answers', type=str, nargs='+',
                        help='false answer(s) (each answer enclosed in quotes)')
    group_2 = parser.add_mutually_exclusive_group()
    group_2.add_argument('-n', '--number_of_questions', type=int, help='number of questions to ask on quiz')
    group_2.add_argument('-k', '--keep_asking', action='store_true',
                         help='keep asking quiz questions until told to stop')
    args: Namespace = parser.parse_args()

    # Print help message if no command line arguments are given
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Start DB session
    session: Session = start_session()

    # Process command line arguments
    if args.add:
        if add_question(session=session,
                        class_name=args.class_,
                        chapter=args.chapter,
                        question=args.question,
                        true_answer=args.true_answer,
                        false_answers=args.false_answers):
            print('Question added successfully.')
        else:
            print('Unable to add question.')
    elif args.remove:
        if delete_question(session=session,
                           question=args.question):
            print('Question removed successfully.')
        else:
            print('Unable to remove question.')
    elif args.print:
        print_quiz(session=session,
                   class_name=args.class_,
                   chapter=args.chapter)
    elif args.quiz:
        if args.number_of_questions:
            take_quiz_number_of_questions(session=session,
                                          class_name=args.class_,
                                          chapter=args.chapter,
                                          number_of_questions=args.number_of_questions)
        elif args.keep_asking:
            take_quiz_keep_asking(session=session,
                                  class_name=args.class_,
                                  chapter=args.chapter)

    # End DB session
    end_session(session)

    return


def main() -> None:
    cli_arguments()


if __name__ == '__main__':
    FORMAT = '%(levelname)s:%(asctime)s:%(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)

    main()
