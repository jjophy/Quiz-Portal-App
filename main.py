from app import application
from app.apis import *
from app.setup import *

"""
[Driver Module] : It is responsible for stating the server for application for apis serving
"""
if __name__ == "__main__":
    
    try:
        # add_questions()
        # add_users()
        print("skip creation of users and questions")
    except Exception as e:
        pass
    
    application.run(debug=True, use_reloader=False, port=8000)
    
    
    