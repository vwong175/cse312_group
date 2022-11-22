# cse312_group

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

## Notes
If you are running into issues with cant import certain thing, make sure your Python interpreter is the one in venv
- Cntrl + shift + p -> click the one in the venv

## Contribution
Feel free to add to this readme