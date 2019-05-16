# Quiz
Create and take quizzes. Questions and answers are shuffled each time. I created this to help my wife study for her grad school classes.

## Status:
Alpha - Still in development

## Usage:
```
usage: quiz.py [-h] [-a | -r | -p] [-q QUESTION] [-t TRUE_ANSWER]
               [-f FALSE_ANSWERS [FALSE_ANSWERS ...]]

Create a quiz.

optional arguments:
  -h, --help            show this help message and exit
  -a, --add             Add a new question
  -r, --remove          Remove an existing question
  -p, --print           Print all questions
  -q QUESTION, --question QUESTION
                        Question (enclosed in quotes)
  -t TRUE_ANSWER, --true_answer TRUE_ANSWER
                        True answer (enclosed in quotes)
  -f FALSE_ANSWERS [FALSE_ANSWERS ...], --false_answers FALSE_ANSWERS [FALSE_ANSWERS ...]
                        False answer(s) (each answer enclosed in quotes)
```
## Languages/Frameworks used:
* Python
  * [argparse](https://docs.python.org/3/library/argparse.html)
  * [typing](https://docs.python.org/3/library/typing.html)
* [SQLAlchemy](https://www.sqlalchemy.org/)
