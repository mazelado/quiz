#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 2:35 PM

@author: matt
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError, InvalidRequestError

from class_declarative import Question
from db_declarative import Base, ClassTable, ChapterTable, QuestionTable, FalseAnswersTable

engine = create_engine('sqlite:///quiz.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert new questions in the table
questions = [Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Human somatic cells have ____ chromosomes.',
                      true_answer='46',
                      false_answers=['23', '4', '2']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Human gametes have ____ chromosomes.',
                      true_answer='23',
                      false_answers=['46', '4', '2']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Gametes are _________.',
                      true_answer='haploid (n)',
                      false_answers=['diploid (2n)']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Zygotes are _________.',
                      true_answer='diploid (2n)',
                      false_answers=['haploid (n)']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Sister chromatids of a chromosome separate and are pulled apart during prophase.',
                      true_answer='False',
                      false_answers=['True']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='A zygote undergoes mitosis during the development of the embryo.',
                      true_answer='True',
                      false_answers=['False']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Oogenesis produces four functional egg cells from one cell.',
                      true_answer='False',
                      false_answers=['True']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Meiosis generates zygotes',
                      true_answer='False',
                      false_answers=['True']),
             Question(class_name='BIOL 1127',
                      chapter='19',
                      question='Chromosomes line up along the cell\'s equator during metaphase.',
                      true_answer='True',
                      false_answers=['False'])]

for q in questions:
    # Try to add new class, reuse if it exists
    new_class = ClassTable(class_name=q.class_name)
    try:
        session.add(new_class)
        session.commit()
    except (IntegrityError, InvalidRequestError):  # UNIQUE constraint failed, already exists in table
        session.rollback()
        new_class = session.query(ClassTable).filter(ClassTable.class_name == q.class_name).one()

    # Try to add new chapter, reuse if it exists
    new_chapter = ChapterTable(chapter=q.chapter, class_name=new_class)
    try:
        session.add(new_chapter)
        session.commit()
    except (IntegrityError, InvalidRequestError):  # UNIQUE constraint failed, already exists in table
        session.rollback()
        new_chapter = session.query(ChapterTable).filter(ChapterTable.chapter == q.chapter).one()

    new_question = QuestionTable(question=q.question, true_answer=q.true_answer, chapter=new_chapter)
    session.add(new_question)
    session.commit()
    for f in q.false_answers:
        new_false_answer = FalseAnswersTable(answer=f, question=new_question)
        session.add(new_false_answer)
        session.commit()
