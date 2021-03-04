import redis

db = redis.Redis(host='redis', socket_connect_timeout=1)

db.ping()

db.set('foo', 'bar')

print(db.get('foo'))