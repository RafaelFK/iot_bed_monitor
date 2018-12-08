from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        print(request.json)

        return "Received!"
    else:
        return 'hello!'