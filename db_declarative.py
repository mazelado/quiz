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


class QuestionTable(Base):
    """
    This is a class to define the Question database table.

    Contains the question and correct answer. See the FalseAnswer table for the incorrect answers.
    """
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    question = Column(String(250), nullable=False)
    true_answer = Column(String(250), nullable=False)
    false_answer = relationship("FalseAnswers", cascade='all, delete-orphan')


class FalseAnswerTable(Base):
    """
    This is a class to define the FalseAnswer database table.

    Uses a one-to-many relationship from the Question table to multiple rows in the FalseAnswer table.
    """
    __tablename__ = 'false_answer'
    id = Column(Integer, primary_key=True)
    answer = Column(String(250))
    question_id = Column(Integer, ForeignKey('question.id'))


engine = create_engine('sqlite:///quiz.db')

Base.metadata.create_all(engine)
