from marshmallow import Schema, fields


"""
This module aims at providing the request and response format for the various api calls.
This also helpful for creating swagger docs for apis testing.
"""


# Response from the server
class APIResponse(Schema):
    message = fields.Str(default="Success")

# Sign Up
class SignUpRequest(Schema):
    name = fields.Str(default = "name")
    username = fields.Str(default="username")
    password = fields.Str(default = "password")
    is_admin = fields.Int(default = 0)

# Log In
class LoginRequest(Schema):
    username = fields.Str(default="username")
    password = fields.Str(default="password")

# Log Out
class LogoutRequest(Schema):
    session_id = fields.Str(default="session_id")


# Add a question request
class AddQuestionRequest(Schema):
    session = fields.Str(default="session_id")
    question = fields.Str(default="question")
    choice1 = fields.Str(default="choice1")
    choice2 = fields.Str(default="choice2")
    choice3 = fields.Str(default="choice3")
    choice4 = fields.Str(default="choice4")
    answer = fields.Int(default=0)
    marks = fields.Int(default=0)
    remarks = fields.Str(default="remarks")

# SessionIdRequest
class SessionIdRequest(Schema):
    session = fields.Str(default="session_id")   

# List questions response   
class QuestionListResponse(Schema):
    questions = fields.List(fields.Dict()) 

# Create Quiz request
class CreateQuizRequest(Schema):
    question_ids = fields.List(fields.Str) 
    quiz_name = fields.Str(default="quiz_name")
    session = fields.Str(default="session_id")

# View Quiz request
class ViewQuizRequest(Schema):
    quiz_id = fields.Str(default="quiz_id")
    session = fields.Str(default="session_id")  


# Quiz response  -- when output is a list of dictionary values 
class QuizResponse(Schema):
    results = fields.List(fields.Dict()) 


# Assign Quiz Request
class AssignQuizRequest(Schema):
    user_id = fields.Str(default="user_id") 
    quiz_id = fields.Str(default="quiz_id")
    session = fields.Str(default="session_id")

# Attempt Quiz Request
class AttemptQuizRequest(Schema):
    quiz_id = fields.Str(default="quiz_id")
    responses = fields.Dict()
    session = fields.Str(default="session_id")   # user session_id who will attempt the quiz

# Quiz Results Request
class QuizResultsRequest(Schema):
    quiz_id = fields.Str(default="quiz_id")
    session = fields.Str(default="session_id")  # active admin session_id

