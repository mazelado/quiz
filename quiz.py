#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 7:55 AM

@author: matt


"""
import click
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import Any, List

from db_declarative import Question, FalseAnswer, Base, Quiz


@click.command()
@click.option('--add/--remove', '-a/-r')
@click.option('--question', nargs=2, type=(str, str))
@click.option('--false', '-f', nargs=-1)
def edit_row(option, question, false_answers):
    click.echo('option=%s\nquestion=%s\ncorrect answer=%s\nfalse answer(s)=%s' % option, question[0], question[1],
               false_answers)


@click.command()
@click.option('--print', '-p')
def main(option, question):
    """
    Demonstrates use of Question and Quiz classes.

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
        false_answer_rows = session.query(FalseAnswer).filter(
            FalseAnswer.question == question_row).all()
        for false_answer_row in false_answer_rows:  # type: str
            false_answer_list.append(false_answer_row.answer)
        all_questions.append(Question(question_row.question, question_row.true_answer, false_answer_list))

    quiz = Quiz(all_questions)  # type: Quiz
    print(quiz)


if __name__ == '__main__':
    main()

    # TODO: Read command line arguments
    # TODO: Add CLI to add questions
    # TODO: Add CLI to print a quiz
    # TODO: Add CLI to delete a question
