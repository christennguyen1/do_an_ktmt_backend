from flask import Flask
from app.routes.routes import data_routes

app = Flask(__name__)

app.register_blueprint(data_routes)

@app.route('/ping', methods=['GET'])
def ping():
    return {"message": "Server is running"}, 200

if __name__ == '__main__':
    app.run()
    # app.run(host='0.0.0.0', port=5000, debug=True)
