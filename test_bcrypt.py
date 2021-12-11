from bcrypt import hashpw, checkpw, gensalt

password = 'testpass1'.encode('utf-8')
hashed = hashpw(password, gensalt())

if checkpw(password, hashed):
    print('Match')
else:
    print('No match')
