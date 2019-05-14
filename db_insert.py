#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 2:35 PM

@author: matt
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_declarative import Base, Question, FalseAnswer
import quiz

engine = create_engine('sqlite:///quiz.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Insert new questions in the table
questions = []
questions.append(quiz.Question('Human somatic cells have ____ chromosomes.', '46', ['23', '4', '2']))
questions.append(quiz.Question('Human gametes have ____ chromosomes.', '23', ['46', '4', '2']))
questions.append(quiz.Question('Gamese are _________.', 'haploid (n)', ['diploid (2n)']))
questions.append(quiz.Question('Zygotes are _________.', 'diploid (2n)', ['haploid (n)']))
questions.append(
    quiz.Question('Sister chromatids of a chromosome separate and are pulled apart during prophase.', 'False',
                  ['True']))
questions.append(quiz.Question('A zygote undergoes mitosis during the development of the embryo.', 'True', ['False']))
questions.append(quiz.Question('Oogenesis produces four functional egg cells from one cell.', 'False', ['True']))
questions.append(quiz.Question('Meiosis generates zygotes', 'False', ['True']))
questions.append(quiz.Question('Chromosomes line up along the cell\'s equator during metaphase.', 'True', ['False']))

for q in questions:
    new_question = Question(question=q.getQuestion(), true_answer=q.getTrueAnswer())
    session.add(new_question)
    session.commit()
    for f in q.getFalseAnswers():
        new_false_answer = FalseAnswer(answer=f, question=new_question)
        session.add(new_false_answer)
        session.commit()
