import redis

db = redis.Redis(host='redis')

db.ping()

db.set('foo', 'bar')

print(db.get('foo'))
print(db.get('1'))

for i in range(1000):
    db.set(str(i), str(i))

db.flushdb()