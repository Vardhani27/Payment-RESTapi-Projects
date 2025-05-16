from flask import Flask
from routes.payment_routes import router as payment_router
from routes.user_routes import user_router
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(payment_router)
app.register_blueprint(user_router)
Swagger(app)

@app.route('/')
def home():
    return "Welcome to the Payment API!"

if __name__ == '__main__':
    app.run(host="localhost", port=8080,debug=True)
