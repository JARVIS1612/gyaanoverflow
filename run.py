from GOF import create_app
import os
from dotenv import load_dotenv
app = create_app()
load_dotenv()
if __name__ == "__main__":
    app.secret_key = 'mysecret'
    app.run(debug=False, host="0.0.0.0", port=os.getenv("PORT"))