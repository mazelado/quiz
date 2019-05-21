#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 5/20/19 3:51 PM

@author: matt
"""

import pytest

import quiz


class TestQuiz(object):
    @pytest.fixture
    def supply_session(self):
        session = quiz.start_session()

        return session

    def test_start_session(self):
        # Setup
        session = quiz.start_session()

        # Tests
        assert session.bind.url.database == 'quiz.db'
        assert session.bind.url.drivername == 'sqlite'
        # assert session.is_active is True

        # Teardown
        quiz.end_session(session=session)

    def test_end_session(self):
        # Setup
        # session = quiz.start_session()
        # quiz.end_session(session=session)

        # Tests
        # assert session.is_active is False

        # Teardown
        pass

    @pytest.mark.parametrize('session, class_name, chapter, question, true_answer, false_answers', [
        (quiz.start_session(), None, 'Test Chapter', 'Test Question', 'Test True Answer',
         ['Test False Answer 1', 'Test False Answer 2', 'Test False Answer 3']),
        (quiz.start_session(), 'Test Class Name', None, 'Test Question', 'Test True Answer',
         ['Test False Answer 1', 'Test False Answer 2', 'Test False Answer 3']),
        (quiz.start_session(), 'Test Class Name', 'Test Chapter', None, 'Test True Answer',
         ['Test False Answer 1', 'Test False Answer 2', 'Test False Answer 3']),
        (quiz.start_session(), 'Test Class Name', 'Test Chapter', 'Test Question', None,
         ['Test False Answer 1', 'Test False Answer 2', 'Test False Answer 3']),
        (quiz.start_session(), 'Test Class Name', 'Test Chapter', 'Test Question', 'Test True Answer',
         None)])
    def test_add_question(self, session, class_name, chapter, question, true_answer, false_answers):
        # Setup
        # session = quiz.start_session()

        # Tests
        with pytest.raises(SystemExit):
            quiz.add_question(session=session,
                              class_name=class_name,
                              chapter=chapter,
                              question=question,
                              true_answer=true_answer,
                              false_answers=false_answers)

        # Teardown
        quiz.end_session(session)

    def test_delete_question(self):
        pass

    def test_delete_question_noresultfound(self):
        pass

    def test_delete_question_multipleresultsfound(self):
        pass

    def test_question_table_to_list(self):
        pass

    def test_get_questions_from_db(self):
        pass

    def test_print_quiz(self):
        pass

    def test_take_quiz_number_of_questions(self):
        pass

    def test_take_quiz_keep_asking(self):
        pass

    def test_cli_arguments(self):
        pass
