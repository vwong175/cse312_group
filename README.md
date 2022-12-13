# cse312_group

Link to our site: www.rokpepersizzors.me or http://54.221.252.1:8080/

This repo has been updated to work with `Python v3.8` and up.

## How To Run
1. Install `virtualenv`:
```
$ pip install virtualenv
```

2. Open a terminal in the project root directory and create a venv folder by running:
```
$ py -3 -m venv venv
```

3. Then run the command to activate your virtual environment:
```
$ venv\Scripts\activate
```

4. Then install the dependencies:
```
$ (env) pip install -r requirements.txt
```

5. Finally start the web server:
```
$ (env) python server.py
```

This server will start on port 5000 by default. You can change this in `server.py` by changing the following line to this:

```python
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=<desired port>)
```

6. The below HTML head code is what works for me when I am implementing and working with socketio
```HTML
<meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script> <!--Client bundle-->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js"></script>
```

## Notes
If you are running into issues with cant import certain thing, make sure your Python interpreter is the one in venv
- Cntrl + shift + p -> click the one in the venv

## Contribution
Feel free to add to this readme
