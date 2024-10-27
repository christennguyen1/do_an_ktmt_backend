from flask import jsonify
from io import BytesIO
from PIL import Image
from flask import Flask, send_file
from app.services.service import get_all_data, get_data_sensor_service, get_data_sensor_toTime_service, login_user_service, register_user_service, update_data_relay_service, create_data_relay_service, delete_data_relay_service, delete_data_user_service, update_password_user_service, update_user_service, upload_avatar_user_service, get_avatar_user_service, get_data_latest_service, get_data_relay_detail_service, get_data_all_relay_service

def get_all_data_controller():
    try:
        # Truy vấn tất cả các document trong collection
        data, status = get_all_data()
        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,
            "errCode": 0
        }
        return jsonify(response), status
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    
def get_data_latest_controller():
    try:
        # Truy vấn tất cả các document trong collection
        data, status = get_data_latest_service()
        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,
            "errCode": 0
        }
        return jsonify(response), status
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def get_data_sensor_controller():
    try:
        # Truy vấn tất cả các document trong collection
        data, status = get_data_sensor_service()
        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,
            "errCode": 0
        }
        return jsonify(response), status
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500


def get_data_sensor_toTime_contoller():
    try:
        # Truy vấn tất cả các document trong collection
        data, status = get_data_sensor_toTime_service()
        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,
            "errCode": 0
        }
        return jsonify(response), status
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def login_user_controller():
    try:
        # Truy vấn tất cả các document trong collection
        data, status = login_user_service()
        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,
            "errCode": 0
        }
        return jsonify(response), status
    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def register_user_controller():
    try:
        data, status = register_user_service()  

        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,  
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def delete_user_controller():
    try:
        data, status = delete_data_user_service()  

        response = {
            "message": data.get('message'),
            "data": data.get('data'),
            "status": status,  
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def update_data_relay_controller():
    try:
        data, status = update_data_relay_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def create_data_relay_controller():
    try:
        data, status = create_data_relay_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def delete_data_relay_controller():
    try:
        data, status = delete_data_relay_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def get_data_relay_controller():
    try:
        data, status = get_data_all_relay_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def get_data_relay_detail_controller():
    try:
        data, status = get_data_relay_detail_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500

def update_password_user_controller():
    try:
        data, status = update_password_user_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500


def update_user_controller():
    try:
        data, status = update_user_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def upload_avatar_user_controller():
    try:
        data, status = upload_avatar_user_service() 

        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return {
            "status": 500,
            "message": str(e),
            "error": 1
        }, 500
    

def get_avatar_user_controller(email):
    try:
        # Gọi hàm dịch vụ để lấy avatar
        data, status = get_avatar_user_service(email) 

        if status == 200:
            # Nếu trạng thái 200, trả về ảnh
            return send_file(BytesIO(data), mimetype='image/jpeg')

        # Nếu không phải 200, trả về phản hồi lỗi
        response = {
            "message": data.get('message'),
            "data": data.get('data'),  
            "status": status, 
            "errCode": 0  
        }
        return jsonify(response), status  

    except Exception as e:
        return jsonify({
            "status": 500,
            "message": str(e),
            "error": 1
        }), 500