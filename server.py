from flask import Flask, render_template, url_for, request, redirect
from flask_pymongo import MongoClient #I think this is correct?
from flask_login import LoginManager

app = Flask(__name__)
client = MongoClient('mongo') #Connect to the hostname 'mongo' as defined in the docker compose file
db = client['r_p_s']    #Select the database


#Collections
users = db['users']

@app.route('/', methods=["GET"])
def login_page():
    return render_template('register.html')

@app.route('/home', methods=["GET"])
def home_page():
    return render_template('home.html')

#test

# commentHistory.delete_many({})
# currentId.delete_many({})

currentId.insert_one({'lastId':0})


def getCurrentNumbers():
    id = currentId.find_one()
    num = int(id['lastId'])
    return num


def getNextAvilId():
    id = currentId.find_one()
    nextId = int(id['lastId']) + 1
    currentId.update_one(id, {'$set': {'lastId': nextId}})
    return nextId


def escapeHtml(input):
    s = input
    s = s.replace("&", "&amp;")
    s = s.replace("<", "&lt;")
    s = s.replace(">", "&gt;")
    s = s.replace('"', "&quot;")
    s = s.replace('\'', "&#x27;")

    return s


def splitHeaders(input):
    end = b'\r\n\r\n'
    index = input.find(end)
    headers = input[:index]
    rest = input[(index + len(end)):]
    arr = [headers, rest]
    return arr


def newToken():
    token = ""
    for i in range(8):
        token += random.choice(string.ascii_letters)

    xsrfTokens.insert_one({token:1})

    return token


def receiveHeaderInfo(header):
    lines = header.decode("utf-8").split("\r\n")
    receiveRequest = lines[0]
    # print(receiveRequest)
    lenIndex = 0
    lenExist = False
    bIndex = 0
    bExist = False
    count = 0
    for line in lines:
        if "Content-Length:" in line:
            lenIndex = count
            lenExist = True
        if "boundary=" in line:
            bIndex = count
            bExist = True
        count += 1

    if lenExist:
        length = int(lines[lenIndex].split("Content-Length: ",1)[1])
    else:
        length = 0
    # print(length)
    if bExist:
        boundary = lines[bIndex].split("boundary=",1)[1]
    else:
        boundary = ''
    # print(boundary)

    # array of [received request, length of body, boundary in str, whether the form is multipart]
    return [receiveRequest, length, boundary, bExist]


class TCP_Handler(socketserver.BaseRequestHandler):

    def handle(self):
        content = self.request.recv(2048)
        print(content)
        # print(content.decode('utf-8') + " len:" + str(len(content)))
        firstReceive = splitHeaders(content)
        header = firstReceive[0]

        rest = firstReceive[1]
        # print(len(rest))

        infoFromHeader = receiveHeaderInfo(header)
        request = infoFromHeader[0]
        print(request)
        length = infoFromHeader[1]
        # print(length)
        boundary = infoFromHeader[2].encode('utf-8')
        multiOrNot = infoFromHeader[3]

        if 0 < length != len(rest):
            leftBits = length - len(rest)
        else:
            leftBits = 0

        # print(len(rest))
        # print(len(rest)==length)
        # print(leftBits)

        # while haven't read all bytes keep going
        while leftBits > 0:
            if leftBits > 2048:
                newContent = self.request.recv(2048)
                if len(newContent)>0:
                    rest += newContent
                leftBits -= 2048
            else:
                newContent = self.request.recv(leftBits)
                if len(newContent)>0:
                    rest += newContent
                leftBits -= leftBits
            # print(newContent.decode())

        toSend = reply.response(request, multiOrNot)
        # print(toSend.decode())

        self.request.sendall(toSend)
        # print("sending message")

# docker compose-up file, mongodb
#some 

if __name__ == '__main__':
    serv = socketserver.ThreadingTCPServer(('0.0.0.0', 8080), TCP_Handler)

    # deletedID.delete_many({})
    serv.serve_forever()
