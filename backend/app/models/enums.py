from enum import Enum

class Role(str, Enum) :
    USER = "user"    
    ADMIN = "admin"


class Action(str, Enum) :
    SUMMARY = "summary"
    TRANSLATION = "translation"
    QUIZ = "quiz"