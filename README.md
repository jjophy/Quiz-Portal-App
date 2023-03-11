# Quiz Portal App

Mini Project - Quiz Portal	 IIITH-SEDS-Part A_July 21
Jan 03, 2022	Student: Jophy Joseph

Quiz Portal app has the below functionalities:

1. Sign Up : Users will be signed up for using the application. Users will be Admin or Normal
Users.
2. Login: User can be able to login using the credentials.In this session_id will be created
which will be further used for all subsequent activities.
3. Add Questions : Admin can add new questions in the questions table.
4. List All Questions : Admin can list all questions persisted in the database.
5. Creating Quiz : Admin can create a new quiz and tag the required questions to the created
quiz
6. Assigning Quiz to Users : Admin can assign the required quiz to the user.
7. View quiz : Users are able to view the list of all questions for the particular quiz id.
8. List all Assigned Quizzes: Users can able to view the list of all assigned quizzes with the
respective status and with respective scores (submitted/not submitted)
9. Attempt Quiz : Users can attempt the assigned quiz only once by submitting the
responses in the given json format. Response will be the score achieved from the quiz
10.List All Quizzes : Admin can list all created quizzes.
11.Quiz Results : For a given quiz id, Admin can fetch quiz results in which the results are
sorted in decreasing order of the achieved scores and the quiz instances where users are
yet to attempt the quiz, will be displayed at last.
12.Logout : User will be perform a logout action in case of taking break from the application


The app folder has below 6 .py files

__init__
apis
models
schemas
services
setup

The app is triggered with main.py. This also calls 2 methods for creating initial users and questions. I have commented it for now. Can be  uncommented and run for the first time

  

 
