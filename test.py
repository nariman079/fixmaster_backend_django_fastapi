from datetime import datetime, timedelta

current_time = datetime.now().time()
result = (
   datetime.combine(datetime.now(), current_time) + timedelta(minutes=30)
).time()
print(result)