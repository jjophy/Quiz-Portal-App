#from sqlalchemy.orm.session import sessionmaker
from app.models import QuestionMaster, QuizInstance, QuizMaster, QuizQuestions, UserMaster, UserResponses, UserSession
from app import db
import uuid
from flask import session
from datetime import datetime
from typing import List

"""
[Services Module] Implement various helper functions here as a part of api
implementation using MVC Template
"""
class Error(Exception):
    #Base class for other exceptions
    pass

class UserNotFoundErr(Error):
    # User not found 
    pass

class UserNotAuthorisedErr(Error):
    # User not authorised for this activity -- need to be an admin
    pass

# No active sessions found for this user
class NoActiveSessionFoundErr(Error):
    pass

class UserAlreadyAttempted(Error):
    # user has already attempted this quiz before
    pass

class NoRecordFound(Error):
    pass

class UserAlreadyLoggedIn(Error):
    pass

# Sign-up - registers a new user
def create_user(**kwargs):
    try:
            user = UserMaster(
                uuid.uuid4(),
                kwargs['name'],
                kwargs['username'],
                kwargs['password'],
                kwargs['is_admin'])
            db.session.add(user)
            db.session.commit()
            return kwargs['username']
    except Exception as e:
        raise e

# Log in -- adds a session entry in user_session and is_active flag set to 1
def login_user(**kwargs):
    try:
        user = UserMaster.query.filter_by(
            username=kwargs['username'], password=kwargs['password']).first()
        if user:
            user_session = UserSession.query.filter_by(user_id=user.id, is_active=1).first()
            if user_session:
                raise UserAlreadyLoggedIn('User already logged in and has an active session')
            else:    
                try:
                    user_session = UserSession(
                        uuid.uuid4(),  # id
                        user.id,
                        uuid.uuid4())  # session_id
                    db.session.add(user_session)
                    db.session.commit()
                    return user_session.session_id
                except Exception as e:
                        raise e
        else:
            raise  UserNotFoundErr('Invalid credentials')
    except Exception as e:
            raise e

# Log out -- is_active flag set to 0 for the given session
def logout_user(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session_id'], is_active=1).first()
        if user_session:
            try:
                user_session.is_active = 0
                db.session.commit()
            except Exception as e:
                    raise e       
        else:
            raise  UserNotFoundErr('Active user session not found')
    except Exception as e:
            raise e

        
# Add question -- only admin user can add questions
def add_question(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            user = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            if user:
                try:
                   question = QuestionMaster(
                   uuid.uuid4(),
                   kwargs['question'],
                   kwargs['choice1'],
                   kwargs['choice2'],
                   kwargs['choice3'],
                   kwargs['choice4'],
                   kwargs['answer'],
                   kwargs['marks'],
                   kwargs['remarks'])
                   db.session.add(question)
                   db.session.commit()
                except Exception as e:
                   raise e  
            else:
                raise  UserNotAuthorisedErr("User not authorised for this activity ") 
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
       raise e


def list_questions(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            user = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            if user:
                try:
                    questions = QuestionMaster.query.filter_by(is_active=1)
                    questions_list = list()
                    for question in questions:
                        question_dict = {}
                        question_dict['question_id'] = question.id
                        question_dict['question'] = question.question
                        question_dict['choice1'] = question.choice1
                        question_dict['choice2'] = question.choice2
                        question_dict['choice3'] = question.choice3
                        question_dict['choice4'] = question.choice4
                        question_dict['answer'] = question.answer
                        question_dict['marks'] = question.marks
                        question_dict['remarks'] = question.remarks
                        questions_list.append(question_dict)
                    return questions_list
                except Exception as e:
                    raise e  
            else:
                raise  UserNotAuthorisedErr("User not authorised for this activity ") 
        else:
            raise  NoActiveSessionFoundErr("No active session for this user")      
    except Exception as e:
        raise e

def create_quiz(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            user = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            if user:
                try:
                    quiz_id = uuid.uuid4()   # id of QuizMaster, used as quiz_id in QuizQuestions
                    quiz = QuizMaster(
                        quiz_id,
                        kwargs['quiz_name'])
                    db.session.add(quiz)
                    # db.session.commit()

                    question_ids = kwargs['question_ids']
                    for question in question_ids:
                        quiz_question = QuizQuestions(
                            uuid.uuid4(),
                            quiz_id,
                            question)
                        db.session.add(quiz_question) 
                    db.session.commit()
                    return kwargs['quiz_name']
                except Exception as e:
                    raise e  
            else:
                raise  UserNotFoundErr("No quiz assigned to this user") 
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e


# only admin and assigned users can view the questions in a quiz
def assign_quiz(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            admin = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            if admin :
                try:
                    assigned_quiz = QuizInstance(
                    uuid.uuid4(),
                    kwargs['quiz_id'],
                    kwargs['user_id']
                    )

                    db.session.add(assigned_quiz)
                    db.session.commit()
                except Exception as e:
                    raise e  
            else:
                raise  UserNotAuthorisedErr("User not authorised for this activity ") 
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e


# only admin and assigned users can view the questions in a quiz
def view_quiz(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            admin = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            assigned_user = QuizInstance.query.filter_by(user_id=user_session.user_id, quiz_id=kwargs['quiz_id']).first()
            if admin or assigned_user :
                try:
                    inp_quiz_id = kwargs['quiz_id']
                    quiz_questions = QuizQuestions.query.filter_by(quiz_id=inp_quiz_id)
                    questions = []
                    for quiz_question in quiz_questions :     
                        questions.append(QuestionMaster.query.filter_by(id=quiz_question.question_id).first()) 
                    questions_list=list()
                    for question in questions:
                        question_dict = {}
                        question_dict['question_id'] = question.id
                        question_dict['question'] = question.question
                        question_dict['choice1'] = question.choice1
                        question_dict['choice2'] = question.choice2
                        question_dict['choice3'] = question.choice3
                        question_dict['choice4'] = question.choice4
                        question_dict['answer'] = question.answer
                        question_dict['marks'] = question.marks
                        question_dict['remarks'] = question.remarks
                        questions_list.append(question_dict)
                    return questions_list
                               
                except Exception as e:
                    raise e  
            else:
                raise  UserNotAuthorisedErr("User not authorised for this activity ") 
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e



# users can view the quizzes assigned to them along with their submission status and scores
def view_assigned_quiz(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            try:
                assigned_quizzes = QuizInstance.query.filter_by(user_id=user_session.user_id)
                print(assigned_quizzes)
                quiz_list = list()
                for quiz in assigned_quizzes:
                    quiz_dict = {}
                    quiz_dict['quiz_id'] = quiz.quiz_id
                    quiz_dict['score_achieved'] = quiz.score_achieved
                    quiz_dict['is_submitted'] = quiz.is_submitted
                    quiz_details = QuizMaster.query.filter_by(id=quiz.quiz_id,is_active=1).first()
                    quiz_dict['quiz_name'] = quiz_details.quiz_name
                    
                    quiz_list.append(quiz_dict)
                    print(quiz_list)
                    return quiz_list

            except Exception as e:
                raise e  
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e

# users can attempt the quiz assigned to them and their scores will be displayed upon submssion
def attempt_quiz(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            print(user_session.user_id)
            quiz_entry = QuizInstance.query.filter_by(quiz_id = kwargs['quiz_id'], user_id=user_session.user_id, is_active=1).first()
            if quiz_entry :
                if quiz_entry.is_submitted == 1:
                    raise UserAlreadyAttempted("user has already attempted this quiz") 
                else:    
                    try:
                        # add each response into the UserResponses table
                        score = 0
                        response_dict = kwargs['responses']
                        for key  in response_dict:
                            user_response = UserResponses(
                                uuid.uuid4(),
                                kwargs['quiz_id'],
                                user_session.user_id,
                                key,
                                response_dict[key])
                            db.session.add(user_response)
                            #db.session.commit()

                            # calculating and adding score received for each correct answer
                            question_rec = QuestionMaster.query.filter_by(id=key,is_active=1).first()
                            if question_rec:
                                if question_rec.answer == response_dict[key]:
                                    score = score + question_rec.marks
                            else:
                                raise  NoRecordFound("no record found in QuestionMaster for given question")     

                        # updating QuizInstance table with score acheived and setting submitted flag to 1
                        quiz_entry.score_achieved = score
                        quiz_entry.is_submitted = 1
                        db.session.commit()

                        return score
                    
                    except Exception as e:
                            raise e  
            else:
              raise NoRecordFound("user has not been assigned this quiz")
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e

def mySortFunc(e):
  return e['score_achieved']  

# admin can view the results of a particular quiz assigned to different users
def quiz_results(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            admin = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            if admin:
                try:
                    quiz_results = QuizInstance.query.filter_by(quiz_id=kwargs['quiz_id'])
                    result_list = list()
                    for result in quiz_results:
                        result_dict = {}
                        result_dict['is_submitted'] = result.is_submitted
                        result_dict['score_achieved'] = result.score_achieved
                        result_dict['user_id'] = result.user_id
                        result_list.append(result_dict)
                    result_list.sort(reverse=True,key=mySortFunc)
                    return(result_list)

                except Exception as e:
                        raise e  
            else:
               raise  UserNotAuthorisedErr("User not authorised for this activity")              
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e


# admin can view all the quizzes created
def view_all_quiz(**kwargs):
    try:
        user_session = UserSession.query.filter_by(session_id=kwargs['session'],is_active=1).first()
        if user_session:
            admin = UserMaster.query.filter_by(id = user_session.user_id, is_admin=1).first()
            if admin:
                try:
                    quiz_info = QuizMaster.query.filter_by(is_active=1)
                    quiz_list = list()
                    for quiz in quiz_info:
                        quiz_dict = {}
                        quiz_dict['quiz_id'] = quiz.id
                        quiz_dict['quiz_name'] = quiz.quiz_name
                        quiz_list.append(quiz_dict)
                    return quiz_list

                except Exception as e:
                        raise e  
            else:
               raise  UserNotAuthorisedErr("User not authorised for this activity")  
        else:
            raise  NoActiveSessionFoundErr("no active session for this user")      
    except Exception as e:
        raise e








  