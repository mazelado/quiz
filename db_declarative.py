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


class ClassTable(Base):
    """
    This is a class to define the Class database table.
    Contains the name of the class.
    """
    __tablename__ = 'class'
    id = Column(Integer, primary_key=True)
    class_name = Column(String(250), nullable=False, unique=True)
    chapter = relationship("ChapterTable", back_populates='class_name', cascade='all, delete-orphan')


class ChapterTable(Base):
    """
    This is a class to define the Chapter database table.
    Contains the chapter name.

    Has a one-to-many relationship with the Class table.
    """
    __tablename__ = 'chapter'
    id = Column(Integer, primary_key=True)
    class_id = Column(Integer, ForeignKey('class.id'))
    chapter = Column(String(250), nullable=False, unique=True)
    question = relationship("QuestionTable", back_populates='chapter', cascade='all, delete-orphan')
    class_name = relationship('ClassTable', back_populates='chapter')


class QuestionTable(Base):
    """
    This is a class to define the Question database table.
    Contains the question and correct answer. Incorrect answers are stored in the FalseAnswers table.

    Has a one-to-many relationship with the Chapter table.
    """
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True)
    chapter_id = Column(Integer, ForeignKey('chapter.id'))
    question = Column(String(250), nullable=False, unique=True)
    true_answer = Column(String(250), nullable=False)
    false_answers = relationship("FalseAnswersTable", back_populates='question', cascade='all, delete-orphan')
    chapter = relationship('ChapterTable', back_populates='question')


class FalseAnswersTable(Base):
    """
    This is a class to define the FalseAnswer database table.
    Contains the incorrect answers to the referenced question.

    Has a one-to-many relationship with the FalseAnswer table.
    """
    __tablename__ = 'false_answer'
    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey('question.id'))
    answer = Column(String(250))
    question = relationship("QuestionTable", back_populates='false_answers')


engine = create_engine('sqlite:///quiz.db')

Base.metadata.create_all(engine)
