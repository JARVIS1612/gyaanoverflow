from GOF import create_app

app = create_app()

if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(debug=False, host="0.0.0.0")