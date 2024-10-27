from flask import Blueprint
from app.controllers.controllers import get_all_data_controller, get_data_sensor_controller, get_data_sensor_toTime_contoller, login_user_controller, register_user_controller, update_data_relay_controller, create_data_relay_controller, delete_data_relay_controller, delete_user_controller, update_password_user_controller, update_user_controller, upload_avatar_user_controller, get_avatar_user_controller, get_data_latest_controller, get_data_relay_controller, get_data_relay_detail_controller


data_routes = Blueprint('data_routes', __name__)


#Sensors
data_routes.route('/api/data', methods=['GET'])(get_all_data_controller)


#Sensors
data_routes.route('/api/data/sensors/latest', methods=['GET'])(get_data_latest_controller)


data_routes.route('/api/data/sensors', methods=['GET'])(get_data_sensor_controller)


data_routes.route('/api/data/sensorToTime', methods=['GET'])(get_data_sensor_toTime_contoller)


#Relay
data_routes.route('/api/data/relay/all', methods=['GET'])(get_data_relay_controller)


data_routes.route('/api/data/relay', methods=['GET'])(get_data_relay_detail_controller)


data_routes.route('/api/data/relay/update', methods=['PATCH'])(update_data_relay_controller)


data_routes.route('/api/data/relay/update', methods=['PATCH'])(update_data_relay_controller)


data_routes.route('/api/data/relay/create', methods=['POST'])(create_data_relay_controller)


data_routes.route('/api/data/relay/delete', methods=['POST'])(delete_data_relay_controller)


#User
data_routes.route('/api/users/login', methods=['POST'])(login_user_controller)


data_routes.route('/api/users/register', methods=['POST'])(register_user_controller)


data_routes.route('/api/users/update', methods=['POST'])(update_user_controller)


data_routes.route('/api/users/updatePassword', methods=['POST'])(update_password_user_controller)


data_routes.route('/api/users/delete', methods=['POST'])(delete_user_controller)


data_routes.route('/api/users/upload_avatar', methods=['POST'])(upload_avatar_user_controller)


@data_routes.route('/api/users/get_avatar/<email>', methods=['GET'])
def get_avatar_user(email):
    return get_avatar_user_controller(email)