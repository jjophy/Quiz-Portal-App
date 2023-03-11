import csv
from datetime import datetime
import uuid

from app.models import QuestionMaster, UserMaster
from app import db

"""
Helper function which will create questions based on the data in questions.csv file
"""
def add_questions():
    try:
        with open('questions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                question = row['Question']
                choice1 = row['Choice1']
                choice2 = row['Choice2']
                choice3 = row['Choice3']
                choice4 = row['Choice4']
                answer = row['Answer']
                marks = row['Marks']
                remarks = row['Remarks']
                
                print("question: "+question)
                question_row= QuestionMaster(
                    uuid.uuid4(),
                    question,
                    choice1,
                    choice2,
                    choice3,
                    choice4,
                    answer,
                    marks,
                    remarks,
                    1,          # is_active
                    datetime.utcnow()
                )
                db.session.add(question_row)
            db.session.commit()
    except Exception as e:
        print("could not add questions "+str(e))
        

def add_users():
    try:
        with open('users.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                name = row['Name']
                username = row['UserName']
                password = row['Password']
                
                
                user = UserMaster(
                    uuid.uuid4(),
                    name, 
                    username ,
                    password ,
                    0,          # is_admin
                    1,          # is_active
                    datetime.utcnow()
                )
                
                db.session.add(user)
                
            db.session.commit()
    except Exception as e:
            print("could not add users "+str(e))
