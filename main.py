from website import create_app  # Importing the create_app function from the website package

app = create_app()  # Creating an instance of the Flask application using create_app function

if __name__ == '__main__':
    app.run(debug=True)  # Running the Flask application in debug mode if the script is executed directly
