import redis

db = redis.Redis(host='redis', port=6379)

if db:
    print("Connected")
else:
    print("Failed")