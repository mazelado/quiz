#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 2:35 PM

@author: matt
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from class_declarative import Question
from db_declarative import Base, QuestionTable, FalseAnswersTable

engine = create_engine('sqlite:///quiz.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert new questions in the table
questions = [Question('Human somatic cells have ____ chromosomes.', '46', ['23', '4', '2']),
             Question('Human gametes have ____ chromosomes.', '23', ['46', '4', '2']),
             Question('Gametes are _________.', 'haploid (n)', ['diploid (2n)']),
             Question('Zygotes are _________.', 'diploid (2n)', ['haploid (n)']),
             Question('Sister chromatids of a chromosome separate and are pulled apart during prophase.', 'False',
                      ['True']),
             Question('A zygote undergoes mitosis during the development of the embryo.', 'True', ['False']),
             Question('Oogenesis produces four functional egg cells from one cell.', 'False', ['True']),
             Question('Meiosis generates zygotes', 'False', ['True']),
             Question('Chromosomes line up along the cell\'s equator during metaphase.', 'True', ['False'])]

for q in questions:
    new_question = QuestionTable(question=q.get_question(), true_answer=q.get_true_answer())
    session.add(new_question)
    session.commit()
    for f in q.get_false_answers():
        new_false_answer = FalseAnswersTable(answer=f, question=new_question)
        session.add(new_false_answer)
        session.commit()
