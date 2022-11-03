from GOF import create_app
import os

app = create_app()
if __name__ == "__main__":
    app.secret_key = 'mysecret'
    # app.run(debug=False, host="hospitable-store-production.up.railway.app", port=os.getenv("PORT"))