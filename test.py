from datetime import datetime
from datetime import datetime
import pytz
    
vietnam_tz = pytz.timezone('Asia/Ho_Chi_Minh')
vietnam_time = datetime.now(vietnam_tz)

print(vietnam_time)




switch(status):
    case ligt_off:
        Hal_written_gpio(led, .. , reset)
        if is_button_on:
            Hal_written_gpio(led_low_gpio, led_low_pin , reset)
            status = light_on-dimmed
        break
    case light_on-dimmed:
        if is_button_on:
            status = light_on-dimmed
        if is_button_off:
            den tat
            status = ligt_off
        break
    case light_on-medium:
        break
    case light_on-bright:
        break
    default:
        break