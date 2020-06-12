from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    if query:
        return render_template("result.html")    
    return render_template("home.html")

@app.route('/chess')
def chess():
    return render_template("chess.html")



if __name__ == "__main__":
    app.run(debug=True)
