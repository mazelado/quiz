#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/22/19 3:40 PM

@author: matt
"""
import logging
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem

from quiz_gui.quiz_uic import Ui_MainWindow
from quiz_cli.Question import Question
from quiz_cli.Quiz import Quiz
from quiz_cli.db_declarative import ClassTable, ChapterTable, QuestionTable, FalseAnswersTable
from quiz_cli.quiz import start_session, end_session, get_questions_from_db


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, session):
        logging.debug('entering MainWindow.__init__')
        super(MainWindow, self).__init__()
        self.session = session

        # Set up the user interface from Qt Designer
        self.setupUi(self)

        # Connect the controls
        # Buttons
        self.pushButton_add_question.clicked.connect(self.pushButton_add_question_clicked)
        self.pushButton_edit_question.clicked.connect(self.pushButton_edit_question_clicked)
        self.pushButton_delete_question.clicked.connect(self.pushButton_delete_question_clicked)
        self.pushButton_add_false_answer.clicked.connect(self.pushButton_add_false_answer_clicked)
        self.pushButton_edit_false_answer.clicked.connect(self.pushButton_edit_false_answer_clicked)
        self.pushButton_delete_false_answer.clicked.connect(self.pushButton_delete_false_answer_clicked)
        # Menu
        self.action_quit.triggered.connect(self.action_quit_triggered)
        self.action_undo.triggered.connect(self.action_undo_triggered)
        self.action_redo.triggered.connect(self.action_redo_triggered)
        self.action_cut.triggered.connect(self.action_cut_triggered)
        self.action_copy.triggered.connect(self.action_copy_triggered)
        self.action_paste.triggered.connect(self.action_paste_triggered)
        self.action_delete.triggered.connect(self.action_delete_triggered)
        self.action_select_all.triggered.connect(self.action_select_all_triggered)
        self.action_about.triggered.connect(self.action_about_triggered)
        # Actions
        self.listWidget_questions.itemSelectionChanged.connect(self.listWidget_questions_itemSelectionChanged)

        # Populate the data
        self.all_questions = get_questions_from_db(session=session)
        # quiz = Quiz(self.all_questions)
        for q in self.all_questions:
            item = QListWidgetItem(q.question)
            self.listWidget_questions.addItem(item)

        logging.debug('exiting MainWindow.__init__')

    def pushButton_add_question_clicked(self):
        logging.debug('entering MainWindow.pushButton_add_question_clicked')
        logging.debug('exiting MainWindow.pushButton_add_question_clicked')

    def pushButton_edit_question_clicked(self):
        logging.debug('entering MainWindow.pushButton_edit_question_clicked')
        logging.debug('exiting MainWindow.pushButton_edit_question_clicked')

    def pushButton_delete_question_clicked(self):
        logging.debug('entering MainWindow.pushButton_delete_question_clicked')
        logging.debug('exiting MainWindow.pushButton_delete_question_clicked')
        
    def pushButton_add_false_answer_clicked(self):
        logging.debug('entering MainWindow.pushButton_add_false_answer_clicked')
        logging.debug('exiting MainWindow.pushButton_add_false_answer_clicked')

    def pushButton_edit_false_answer_clicked(self):
        logging.debug('entering MainWindow.pushButton_edit_false_answer_clicked')
        logging.debug('exiting MainWindow.pushButton_edit_false_answer_clicked')

    def pushButton_delete_false_answer_clicked(self):
        logging.debug('entering MainWindow.pushButton_delete_false_answer_clicked')
        logging.debug('exiting MainWindow.pushButton_delete_false_answer_clicked')

    def action_quit_triggered(self):
        logging.debug('entering MainWindow.action_quit_triggered')
        logging.debug('exiting MainWindow.action_quit_triggered')
        end_session(session=self.session)
        sys.exit()

    def action_undo_triggered(self):
        logging.debug('entering MainWindow.action_undo_triggered')
        logging.debug('exiting MainWindow.action_undo_triggered')

    def action_redo_triggered(self):
        logging.debug('entering MainWindow.action_redo_triggered')
        logging.debug('exiting MainWindow.action_redo_triggered')

    def action_cut_triggered(self):
        logging.debug('entering MainWindow.action_cut_triggered')
        logging.debug('exiting MainWindow.action_cut_triggered')

    def action_copy_triggered(self):
        logging.debug('entering MainWindow.action_copy_triggered')
        logging.debug('exiting MainWindow.action_copy_triggered')

    def action_paste_triggered(self):
        logging.debug('entering MainWindow.action_paste_triggered')
        logging.debug('exiting MainWindow.action_paste_triggered')

    def action_delete_triggered(self):
        logging.debug('entering MainWindow.action_delete_triggered')
        logging.debug('exiting MainWindow.action_delete_triggered')

    def action_select_all_triggered(self):
        logging.debug('entering MainWindow.action_select_all_triggered')
        logging.debug('exiting MainWindow.action_select_all_triggered')

    def action_about_triggered(self):
        logging.debug('entering MainWindow.action_about_triggered')
        logging.debug('exiting MainWindow.action_about_triggered')

    def listWidget_questions_itemSelectionChanged(self):
        logging.debug('entering MainWindow.listWidget_questions_itemSelectionChanged')
        # TODO: Get class, chapter, true answer, false answers for question clicked
        logging.debug('exiting MainWindow.listWidget_questions_itemSelectionChanged')


def main():
    logging.debug('entering main')
    app = QApplication(sys.argv)
    session = start_session()
    window = MainWindow(session=session)
    window.show()

    end_session(session=session)
    logging.debug('exiting main')
    sys.exit(app.exec_())


if __name__ == '__main__':
    FORMAT = '%(levelname)s:%(asctime)s:%(message)s'
    logging.basicConfig(level=logging.DEBUG, format=FORMAT)
    main()
