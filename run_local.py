from app import app

DEBUG = True  # if False, Flask-SSlify kicks in

if __name__ == '__main__':

    print("Starting the game ...")

    app.run(debug=DEBUG)