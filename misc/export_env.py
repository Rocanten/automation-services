import os

def set_env():
    try:
        with open('.env', 'r') as reader:
            lines = reader.readlines()
            for line in lines:
                text = line.rstrip('\n')
                name = text.split('=')[0]
                value = text.split('=')[1]
                os.environ[name] = value
    except:
        return

