from app import APP

DEBUG = True  # if False, Flask-SSlify kicks in

if __name__ == '__main__':

    print("Starting the game ...")

    APP.run(debug=DEBUG)