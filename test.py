from datetime import datetime
from datetime import datetime
import pytz
    
vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
vietnam_time = datetime.now(vietnam_tz)

print(vietnam_time)
