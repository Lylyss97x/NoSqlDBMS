import redis

#Connexion
r = redis.Redis(host='localhost', port=6379, db=0)

#Insert
r.set('user:1:name', 'John Doe')
r.set('user:1:email', 'john.doe@example.com')
r.setex('session_key', 3600, 'session_data')

#Get
user_name = r.get('user:1:name')
user_email = r.get('user:1:email')

user_name = user_name.decode('utf-8')
user_email = user_email.decode('utf-8')

print(f"User Name: {user_name}")
print(f"User Email: {user_email}")

#Get many
keys = ['user:1:name', 'user:1:email']
values = r.mget(keys)
values = [value.decode('utf-8') for value in values]

print(f"Values for keys {keys}: {values}")
