from app.models import *
from app import *
from flask_restful import Resource
from flask_apispec.views import MethodResource

from flask_apispec import marshal_with, doc, use_kwargs
from app.schemas import *
from app.services import *


"""
[Sign Up API] : Its responsibility is to perform the signup activity for the user.
"""
class SignUpAPI(MethodResource, Resource):
    @doc(description='Sign Up API', tags=['Sign Up API'])
    @use_kwargs(SignUpRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            username = create_user(**kwargs)
            return APIResponse().dump(dict(message='User '+username + ' is successfully registered')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to register user : {str(e)}')), 400
api.add_resource(SignUpAPI, '/signup')
docs.register(SignUpAPI)


"""
[Login API] : Its responsibility is to perform the login activity for the user and
create session id which will be used for all subsequent operations.
"""
class LoginAPI(MethodResource, Resource):
    @doc(description='Login API', tags=['Login API'])
    @use_kwargs(LoginRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            session_id = login_user(**kwargs)
            username=kwargs['username']
            return APIResponse().dump(dict(message='User  '+username + ' with session_id '+session_id+' is successfully logged in')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to login user : {str(e)}')), 401
api.add_resource(LoginAPI, '/login')
docs.register(LoginAPI)


"""
[Logout API] : Its responsibility is to perform the logout activity for the user.
"""
class LogoutAPI(MethodResource, Resource):
    @doc(description='Logout API', tags=['Logout API'])
    @use_kwargs(LogoutRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            logout_user(**kwargs)
            return APIResponse().dump(dict(message='User is successfully logged out')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to logout user : {str(e)}')), 400
api.add_resource(LogoutAPI, '/logout')
docs.register(LogoutAPI)


"""
[Add Question API] : Its responsibility is to add question to the question bank.
Only Admin has the rights to perform this activity.
"""
class AddQuestionAPI(MethodResource, Resource):
    @doc(description='Add Question API - only admin', tags=['Questions'])
    @use_kwargs(AddQuestionRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            add_question(**kwargs)
            return APIResponse().dump(dict(message='Question has been successfully added')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to add question : {str(e)}')), 401   
api.add_resource(AddQuestionAPI, '/add.question')
docs.register(AddQuestionAPI)


"""
[List Questions API] : Its responsibility is to list all questions present actively in the question bank.
Here only Admin can access all the questions.
"""
class ListQuestionAPI(MethodResource, Resource):
    @doc(description='Question List API - only admin', tags=['Questions'])
    @use_kwargs(SessionIdRequest, location=('json'))
    @marshal_with(QuestionListResponse)  # marshalling
    def post(self, **kwargs):
        try:
            result = list_questions(**kwargs)
            return QuestionListResponse().dump(dict(questions=result)), 200
        except Exception as e:
            return QuestionListResponse().dump(dict(questions=[{"Not able to list questions":str(e)}])), 401
api.add_resource(ListQuestionAPI, '/list.questions')
docs.register(ListQuestionAPI)


"""
[Create Quiz API] : Its responsibility is to create quiz and only admin can create quiz using this API.
"""
class CreateQuizAPI(MethodResource, Resource):
    @doc(description='Create Quiz API - only admin', tags=['Quiz'])
    @use_kwargs(CreateQuizRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            quiz_name = create_quiz(**kwargs)
            return APIResponse().dump(dict(message=f'Quiz {str(quiz_name)} has been successfully created')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to create quiz : {str(e)}')), 401   
api.add_resource(CreateQuizAPI, '/create.quiz')
docs.register(CreateQuizAPI)


"""
[Assign Quiz API] : Its responsibility is to assign quiz to the user. Only Admin can perform this API call.
"""
class AssignQuizAPI(MethodResource, Resource):
    @doc(description='Assign Quiz API - only admin', tags=['Quiz'])
    @use_kwargs(AssignQuizRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            assign_quiz(**kwargs)
            return APIResponse().dump(dict(message='Quiz has been successfully assigned to user ')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to assign quiz : {str(e)}')), 401   
api.add_resource(AssignQuizAPI, '/assign.quiz')
docs.register(AssignQuizAPI)


"""
[View Quiz API] : Its responsibility is to view the quiz details.
Only Admin and the assigned users to this quiz can access the quiz details.
"""
class ViewQuizAPI(MethodResource, Resource):
    @doc(description='View Quiz API - admin and assigned users', tags=['Quiz'])
    @use_kwargs(ViewQuizRequest, location=('json'))
    @marshal_with(QuizResponse)  # marshalling
    def post(self, **kwargs):
        try:
            result = view_quiz(**kwargs)
            return QuizResponse().dump(dict(results=result)), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to view quiz : {str(e)}')), 401   
api.add_resource(ViewQuizAPI, '/view.quiz')
docs.register(ViewQuizAPI)


"""
[View Assigned Quiz API] : Its responsibility is to list all the assigned quizzes 
to the particular user (session_id) with their submission status and achieved scores.
"""
class ViewAssignedQuizAPI(MethodResource, Resource):
    @doc(description='View Assigned Quiz API - assigned user', tags=['Quiz'])
    @use_kwargs(SessionIdRequest, location=('json'))
    @marshal_with(QuizResponse)  # marshalling
    def post(self, **kwargs):
        try:
            result = view_assigned_quiz(**kwargs)
            return QuizResponse().dump(dict(results=result)), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to view assigned quizzes : {str(e)}')), 401   
api.add_resource(ViewAssignedQuizAPI, '/assigned.quizzes')
docs.register(ViewAssignedQuizAPI)


"""
[View All Quiz API] : Its responsibility is to list all the created quizzes.
 Admin can only list all quizzes.
"""
class ViewAllQuizAPI(MethodResource, Resource):
    @doc(description='View All Quiz API - only admin', tags=['Quiz'])
    @use_kwargs(SessionIdRequest, location=('json'))
    @marshal_with(QuizResponse)  # marshalling
    def post(self, **kwargs):
        try:
            result = view_all_quiz(**kwargs)
            return QuizResponse().dump(dict(results=result)), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to view all quizzes : {str(e)}')), 401   
api.add_resource(ViewAllQuizAPI, '/all.quizzes')
docs.register(ViewAllQuizAPI)


"""
[Attempt Quiz API] : Its responsibility is to perform quiz attempt activity by 
the user and the score will be shown as a result of the submitted attempt.
"""
class AttemptQuizAPI(MethodResource, Resource):
    @doc(description='Attempt Quiz API - assigned user', tags=['Quiz'])
    @use_kwargs(AttemptQuizRequest, location=('json'))
    @marshal_with(APIResponse)  # marshalling
    def post(self, **kwargs):
        try:
            score = attempt_quiz(**kwargs)
            return APIResponse().dump(dict(message=f'Quiz has been successfully attempted and user score is: {str(score)}')), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to attempt quizzes : {str(e)}')), 401   
api.add_resource(AttemptQuizAPI, '/attempt.quiz')
docs.register(AttemptQuizAPI)


"""
[Quiz Results API] : Its responsibility is to provide the quiz results in which the users 
having the scores sorted in descending order are displayed, 
also the ones who have not attempted are also shown.
Admin only has access to this functionality.
"""
class QuizResultAPI(MethodResource, Resource):
    @doc(description='Quiz Results API - only admin', tags=['Quiz'])
    @use_kwargs(QuizResultsRequest, location=('json'))
    @marshal_with(QuizResponse)  # marshalling
    def post(self, **kwargs):
        try:
            result = quiz_results(**kwargs)
            return QuizResponse().dump(dict(results=result)), 200
        except Exception as e:
            return APIResponse().dump(dict(message=f'Not able to fetch quiz results : {str(e)}')), 401   
api.add_resource(QuizResultAPI, '/quiz.results')
docs.register(QuizResultAPI)


