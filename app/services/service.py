from app.databases.databases import collection_sensor, collection_user, collection_relay, fs, collection_relay_history
from app.models.models import serialize_item
from flask import Flask, request, jsonify, send_file
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from app.constant.constant import nutnhan
import pytz


def get_all_data():
    data = list(collection_sensor.find())
        
    # Chuyển đổi kết quả sang dạng có thể JSON hóa
    result = [serialize_item(item) for item in data]
    return {
            'message': 'Get data successful',
            'data': result
        }, 200


def get_data_latest_service():
    result = collection_sensor.find_one(sort=[("timestamp", -1)])

    result = serialize_item(result)  
    return {
            'message': 'Get data successful',
            'data': result
        }, 200


def get_data_sensor_service():
    variable = request.args.get('variable')
    data = collection_sensor.find({}, {"_id": 0, variable: 1, "timestamp": 1})
        
    # Chuyển dữ liệu thành list
    result = [{variable: doc[variable], "timestamp": doc["timestamp"]} for doc in data]
        
    return {
            'message': 'Get data sensor successful',
            'data': result
        }, 200


def get_data_sensor_toTime_service():
    start_date_str = request.args.get('start_date')
    end_date_str = request.args.get('end_date')
    variable = request.args.get('variable')

    if not start_date_str or not end_date_str:
        return {
                "error": "Both 'start_date' and 'end_date' are required", 
                "status": 400, 
                "errCode": 1
            }, 400

    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)


    # Tạo truy vấn MongoDB để lấy dữ liệu trong khoảng thời gian và theo variable
    data = collection_sensor.find({
            "timestamp": {
                "$gte": start_date,
                "$lte": end_date
            }
        }, {"_id": 0, variable: 1, "timestamp": 1})  

    result = [{variable: doc[variable], "timestamp": doc["timestamp"]} for doc in data]

    return {
            'message': 'Get data successful',
            'data': result
        }, 200


def update_data_relay_service():
    data = request.json

    relay_name = data.get('relayName')
    status_relay = data.get('status')

    if relay_name not in nutnhan:
        return {
                'message': 'Relay not in server', 
                'errCode': 1
            }, 400
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)

    # Định dạng lại chuỗi datetime (bỏ phần microsecond và timezone)
    formatted_datetime = vietnam_time.strftime("%Y-%m-%d %H:%M:%S")
    
    data = {
        'relayName': relay_name,
        'status': status_relay,
        'timestamp': formatted_datetime
    }

    relay = collection_relay.find_one({'relayName': relay_name})

    relay_status_delete = relay.get('isDeleted', 'Unknown')

    if ((not relay) or (relay_status_delete == True)):
        return {
                'message': 'Relay not in system', 
                'errCode': 1
            }, 400
    

    query = {"relayName": relay_name}
    new_values = {
        "$set": {
            "status": status_relay, "timestamp": formatted_datetime
            }
        }
    
    collection_relay.update_one(query, new_values)

    collection_relay_history.insert_one(data)

        
    return {
        'message': 'Relay update successful',
        'data': {
            'relayName': relay_name,
            'status': status_relay,
            'timestamp': formatted_datetime
        }
    }, 200


def get_data_all_relay_service():
    data = list(collection_relay.find({'isDeleted': {'$ne': True}},{'isDeleted': 0} ))
        
    # Chuyển đổi kết quả sang dạng có thể JSON hóa
    result = [serialize_item(item) for item in data]
    return {
            'message': 'Get data relay successful',
            'data': result
        }, 200


def get_data_relay_detail_service():
    variable = request.args.get('variable')

    if variable not in nutnhan:
        return {
                'message': 'Relay not in server', 'errCode': 1
            }, 400

    relay = collection_relay.find_one(
        {'relayName': variable}, 
        {'relayName': 1, 'status': 1, 'timestamp': 1, 'isDeleted': 1}  
    )

    if relay:
        relay_status_delete = relay.get('isDeleted', 'Unknown')
        if relay_status_delete == True:
            return {
                    'message': 'Relay was setted up', 
                    'errCode': 1
                }, 400
        
    relay.pop('isDeleted', None)    
    result = serialize_item(relay) 
    
    return {
        'message': 'Get data relay detail successful',
        'data': result
    }, 200


def create_data_relay_service():
    data = request.json

    relay_name = data.get('relayName')
    status_relay = data.get('status')

    if relay_name not in nutnhan:
        return {
                'message': 'Relay not in server', 'errCode': 1
            }, 400
    
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
    
    data = {
        'relayName': relay_name,
        'status': status_relay,
        'timestamp': vietnam_time,
        'isDeleted': False
    }

    relay = collection_relay.find_one({'relayName': relay_name})

    if relay:
        relay_status_delete = relay.get('isDeleted', 'Unknown')
        if relay_status_delete == False:
            return {
                    'message': 'Relay was setted up', 
                    'errCode': 1
                }, 400
        else:
            vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
            vietnam_time = datetime.now(vietnam_tz)
            query = {"relayName": relay_name}
            new_values = {
                "$set": {
                    'status': status_relay, "isDeleted": False, "timestamp": vietnam_time
                    }
                }
            
            collection_relay.update_one(query, new_values)
    else:
        if relay_name not in nutnhan:
            return {
                    'message': 'Relay was not setted up', 
                    'errCode': 1
                }, 400
        collection_relay.insert_one(data)

    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
        
    return {
        'message': 'Create Relay successful',
        'data': {
            'relayName': relay_name,
            'status': status_relay,
            'timestamp': vietnam_time
        }
    }, 200

def get_data_relay_history_service():
    data = collection_relay_history.find().sort("timestamp", -1).limit(10)
        
    # Chuyển đổi kết quả sang dạng có thể JSON hóa
    result = [serialize_item(item) for item in data]
    return {
            'message': 'Get data successful',
            'data': result
        }, 200

def delete_data_relay_service():
    data = request.json
    relay_name = data.get('relayName')

    relay = collection_relay.find_one({'relayName': relay_name})

    relay_status_delete = relay.get('isDeleted', 'Unknown')

    if ((not relay) or (relay_status_delete == True)):
        return {
                'message': 'Relay not in system', 
                'errCode': 1
            }, 400
    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)
    
    query = {"relayName": relay_name}
    new_values = {
        "$set": {
            "isDeleted": True, "timestamp": vietnam_time
            }
        }
    
    collection_relay.update_one(query, new_values)

    vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
    vietnam_time = datetime.now(vietnam_tz)

    return {
        'message': 'Relay delete successful',
        'data': {
            'relayName': relay_name,
            'timestamp': vietnam_time
        }
    }, 200
    

def login_user_service():
    data = request.json

    # Kiểm tra nếu email và password được gửi đến
    if not data or not data.get('email') or not data.get('password'):
        return {
                'message': 'Email and password required', 
                'errCode': 1
            }, 400

    email = data.get('email')
    password = data.get('password')

    # Tìm người dùng theo email trong MongoDB
    user = collection_user.find_one({'email': email})

    user_status_delete = user.get('isDeleted', 'Unknown')

    if((not user) or (user_status_delete == True)):
        return {
                'message': 'User not found', 'errCode': 1
            }, 404

    # Kiểm tra mật khẩu có đúng không
    if not check_password_hash(user['password'], password):
        return {
                'message': 'Wrong password', 'errCode': 1
            }, 401
    
    # Trả về thông tin người dùng khi đăng nhập thành công
    return {
        'message': 'Login successful',
        'data': {
            'name': user['name'],
            'email': user['email'],
            'phoneNumber': user['phoneNumber']
        }
    }, 200


def register_user_service():
    data = request.json

    if not data or not data.get('email') or not data.get('password'):
        # Trả về phản hồi lỗi nếu thiếu thông tin
        return {
                'message': 'Email and password required', 
                'data': [],
                'errCode': 1
            }, 400

    name = data.get('name')
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    phoneNumber = data.get('phoneNumber')
    address = data.get('address')
    role = data.get('role')

    user = collection_user.find_one({'email': email})

    # Mã hóa mật khẩu trước khi lưu
    hashed_password = generate_password_hash(password)

    # Tạo người dùng vào cơ sở dữ liệu
    user_data = {
        'name': name,
        'username': username,
        'password': hashed_password,
        'email': email,
        'phoneNumber': phoneNumber,
        'address': address,
        'role': role,
        'isDeleted': False
    }

    print(user_data)

    # Kiểm tra nếu người dùng đã tồn tại
    if user:
        user_status_delete = user.get('isDeleted', 'Unknown')
        if user_status_delete == False:
            return {
                    'message': 'User already exists', 
                    'errCode': 1,
                    'data': []
                }, 409
        else: 
            query = {"email": email}
            new_values = {
                "$set": {
                    'password': hashed_password, 
                    'name': name, 
                    'phoneNumber': phoneNumber, 
                    'address': address, 
                    'role': role,
                    'isDeleted': False
                    }
                }
            
            collection_user.update_one(query, new_values)
    else:     
        collection_user.insert_one(user_data)

    # Trả về thông tin người dùng vừa đăng ký
    return {
        'message': 'User registered successfully',
        'data': {
            'name': user_data['name'],
            'username': user_data['username'],
            'email': user_data['email'],
            'phoneNumber': user_data['phoneNumber'],
            'address': user_data['address']
        }
    }, 201  


def delete_data_user_service():
    data = request.json
    email = data.get('email')

    user = collection_user.find_one({'email': email})

    user_status_delete = user.get('isDeleted', 'Unknown')

    if ((not user) or (user_status_delete == True)):
        return {
                'message': 'User not in system', 
                'errCode': 1
            }, 400
    
    query = {"email": email}
    new_values = {
        "$set": {
            "isDeleted": True, "timestamp": datetime.now()
            }
        }
    
    collection_user.update_one(query, new_values)

    return {
        'message': 'User delete successful',
        'data': {
            'email': email,
            'timestamp': datetime.now()
        }
    }, 200


def update_password_user_service():
    data = request.json

    if not data or not data.get('email') or not data.get('password'):
        # Trả về phản hồi lỗi nếu thiếu thông tin
        return {
                'message': 'Email and password required', 
                'errCode': 1
            }, 400

    password = data.get('password')
    email = data.get('email')

    user = collection_user.find_one({'email': email})

    user_status_delete = user.get('isDeleted', 'Unknown')

    if ((not user) or (user_status_delete == True)):
         return {
                'message': 'User not found', 
                'errCode': 1
            }, 404


    # Mã hóa mật khẩu trước khi lưu
    hashed_password = generate_password_hash(password)

    query = {"email": email}
    new_values = {
        "$set": {
            'password': hashed_password
            }
        }
            
    collection_user.update_one(query, new_values)


    # Trả về thông tin người dùng vừa đăng ký
    return {
        'message': 'Update password user successfully',
        'data': {
            'email': email
        }
    }, 201  


def update_user_service():
    data = request.json

    if not data or not data.get('email'):
        return {
                'message': 'Email and password required', 
                'errCode': 1
            }, 400

    email = data.get('email')
    name = data.get('name')
    phoneNumber = data.get('phoneNumber')
    address = data.get('address')

    user = collection_user.find_one({'email': email})

    user_status_delete = user.get('isDeleted', 'Unknown')

    if ((not user) or (user_status_delete == True)):
         return {
                'message': 'User not found', 
                'errCode': 1
            }, 404
    
    query = {"email": email}

    new_values = {"$set": {}}

    if name:
        new_values["$set"]['name'] = name
    else:
        new_values["$set"]['name'] = user.get('name')


    if phoneNumber:
        new_values["$set"]['phoneNumber'] = phoneNumber
    else:
        new_values["$set"]['phoneNumber'] = user.get('phoneNumber')


    if address:
        new_values["$set"]['address'] = address
    else:
        new_values["$set"]['address'] = user.get('address')
            
    collection_user.update_one(query, new_values)

    return {
        'message': 'User update successfully',
        'data': {
            'name': name,
            'email': email,
            'phoneNumber': phoneNumber,
            'address': address
        }
    }, 201 


def upload_avatar_user_service():
    data = request.json

    if not data or not data.get('email'):
        return {
                'message': 'Email is required', 
                'errCode': 1
            }, 400

    email = data.get('email')

    user = collection_user.find_one({'email': email})

    user_status_delete = user.get('isDeleted', 'Unknown')

    if ((not user) or (user_status_delete == True)):
         return {
                'message': 'User not found', 
                'errCode': 1
            }, 404
    
    if 'avatar' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['avatar']

    if file.filename == '':
        return {"error": "No selected file"}, 400

    # Lưu ảnh vào GridFS
    try:
        avatar_id = fs.put(file, filename=f"avatar_{email}")
        
        # Cập nhật user document với avatar_id
        collection_user.update_one(
            {"email": email},
            {"$set": {"avatar_id": avatar_id}},
            upsert=True
        )

        return {
            "message": "Avatar uploaded successfully",
            'data': {
                'email': email,
                "avatar_id": str(avatar_id)
            } 
        }, 200
    except Exception as e:
        return {
            "message": "Avatar uploaded fail",
            "error": str(e)
        }, 500
    

def get_avatar_user_service(email):
    if not email:
        return {
            'message': 'Email is required', 
            'errCode': 1
        }, 400

    user = collection_user.find_one({'email': email})

    if not user or user.get('isDeleted', False):
        return {
            'message': 'User not found', 
            'errCode': 1
        }, 404

    if "avatar_id" in user:
        avatar_id = user["avatar_id"]
        
        # Lấy file từ GridFS
        try:
            grid_out = fs.get(avatar_id)
            avatar_data = grid_out.read()
            return avatar_data, 200  # Trả về dữ liệu ảnh và mã trạng thái 200
        except Exception as e:
            return {"error": str(e)}, 500

    return {"error": "No avatar found for this user"}, 404