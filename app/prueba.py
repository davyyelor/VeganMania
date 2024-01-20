import hashlib

def hashear(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


if __name__ == '__main__':
    print("Hola mundo")
    print(hashear('1111'))
    print("0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c")
    print("Adios")

#0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c
#