# Quiz
Create and take quizzes. Questions and answers are shuffled each time. I created this to help my wife study for her grad school classes.

## Status:
Alpha - Still in development

## Usage:
```
usage: quiz.py [-h] [-a | -r | -p | -z] [-c CLASS_] [-C CHAPTER] [-q QUESTION]
               [-t TRUE_ANSWER] [-f FALSE_ANSWERS [FALSE_ANSWERS ...]]
               [-n NUMBER_OF_QUESTIONS | -s MINIMUM_SCORE | -k]

Create a quiz.

optional arguments:
  -h, --help            show this help message and exit
  -a, --add             add a new question
  -r, --remove          remove an existing question
  -p, --print           print all questions
  -z, --quiz            take a quiz
  -c CLASS_, --class CLASS_
                        class (enclosed in quotes)
  -C CHAPTER, --chapter CHAPTER
                        chapter (enclosed in quotes)
  -q QUESTION, --question QUESTION
                        question (enclosed in quotes)
  -t TRUE_ANSWER, --true_answer TRUE_ANSWER
                        true answer (enclosed in quotes)
  -f FALSE_ANSWERS [FALSE_ANSWERS ...], --false_answers FALSE_ANSWERS [FALSE_ANSWERS ...]
                        false answer(s) (each answer enclosed in quotes)
  -n NUMBER_OF_QUESTIONS, --number_of_questions NUMBER_OF_QUESTIONS
                        number of questions to ask on quiz
  -k, --keep_asking     keep asking quiz questions until told to stop
```
## Languages/Frameworks used:
* Python
  * [argparse](https://docs.python.org/3/library/argparse.html)
  * [typing](https://docs.python.org/3/library/typing.html)
* [SQLAlchemy](https://www.sqlalchemy.org/)
