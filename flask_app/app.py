from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    if query:
        res = resML(query)
        return render_template("result.html", result=res)    
    return render_template("home.html")

def resML(query):
    """
    This takes in the query from the user and return top 5 words and meaning
    INPUT: string query
    OUTPUT: list 5 tuples [('word', 'meaning')]
    """
    res = [
        ('petrichor', 'smell of mud after rain'),
        ('rain', 'drops of water in sky'),
        ('water', 'chemical consisting of hydrogen and oxygen'),
        ('sand','particles that sedimented from rocks'),
        ('mud', 'layer of soil containing dirt, rocks and other stuff'),
    ]
    return res

@app.route('/chess')
def chess():
    return render_template("chess.html")

if __name__ == "__main__":
    app.run(debug=True)
