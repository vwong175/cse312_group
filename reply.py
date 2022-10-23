# import dynamicServer


def response(request, isMulti):
    requestType = request[:4]
    result = b''
    if 'GET' in requestType:
        result = dealGet(request)
    elif 'POST' in requestType:
        result = dealPost(request,isMulti)
    else:
        result = dealOthers

    return result


def dealGet(request):
    #if "/root" not in request:
    return simplyCheck(request)
    #else:
    #return templateCheck(request)

def simplyCheck(request):
    str1 = 'GET / HTTP/1.1'
    str2 = 'GET /style.css HTTP/1.1'
    str3 = 'GET /functions.js HTTP/1.1'
    str4 = '/image'

    htmlFile = open('./static/index.html','rb').read()
    cssFile = open('./static/style.css','rb').read()
    jsFile = open('./static/functions.js','rb').read()
    image = './static'

    result = b''
    if request==str1:
        #rendered = dynamicServer.getRenderedHTML().encode()
        #result = rOK(len(rendered),rendered,"text/html")
        result = rOK(len(htmlFile),htmlFile,"text/html")
    elif request==str2:
        result = rOK(len(cssFile),cssFile,"text/css")
    elif request==str3:
        result = rOK(len(jsFile),jsFile,"text/javascript")
    elif str4 in request:
        if request.endswith('.jpg HTTP/1.1'):
            newline = (request.replace('.jpg HTTP/1.1','')+'.jpg')[4:]
        elif request.endswith(' HTTP/1.1'):
            newline = (request.replace(' HTTP/1.1','')+'.jpg')[4:]
        pic = open(image + newline,'rb').read()
        result = rOK(len(pic),pic,"image/jpeg")
    else:
        result = r404()

    return result



def dealPost(request,isMulti):
    if 'POST / HTTP/1.1' == request:
        result = rRedirect('/')
    else:
        result = r404()

    return result

def dealOthers():
    return r404()

def rOK(length,body,contentType):
    strLen = str(length)
    newLen = strLen.encode()
    type = contentType.encode()
    result = b"HTTP/1.1 200 OK\r\nContent-Length: "
    result += newLen
    result += b"\r\nX-Content-Type-Options: nosniff\r\nContent-Type: "
    result += type
    result += b"; charset=utf-8\r\n\r\n"
    result += body
    return result

def rRedirect(newLocate):
    result = b"HTTP/1.1 301 Moved Permanently\r\nContent-Length: 0\r\nLocation: " + newLocate.encode()
    return result

def r404():
    result = b"HTTP/1.1 404 Not Found\r\nContent-Length: 40\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nX_X The requested content does not exist"
    return result

def r403():
    result = b"HTTP/1.1 403 Forbidden\r\nContent-Length: 23\r\nContent-Type: text/plain; charset=utf-8\r\n\r\nX_X submission rejected"
    return result
