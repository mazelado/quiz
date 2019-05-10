#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/9/19 2:29 PM

@author: matt
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    true_answer = Column(String(250), nullable=False)


class FalseAnswer(Base):
    __tablename__ = 'false_answer'
    id = Column(Integer, primary_key=True)
    answer = Column(String(250))
    question_id = Column(Integer, ForeignKey('question.id'))
    question = relationship(Question)


engine = create_engine('sqlite:///quiz.db')

Base.metadata.create_all(engine)
