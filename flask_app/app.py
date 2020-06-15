from flask import Flask, render_template, request

model = None
app = Flask(__name__)

@app.route('/')
def home():
    query = request.args.get('query')
    if query:
        res = resML(query)
        return render_template("result.html", res=res, query=query)    
    return render_template("home.html")


def resML(query):
    """
    This takes in the query from the user and return top 5 words and meaning
    INPUT: string query
    OUTPUT: list 5 tuples [('word', 'meaning')]
    """
    words = model.get_words(query)
    result = model.get_meanings(words)
    return result


@app.route('/chess')
def chess():
    return render_template("chess.html")

if __name__ == "__main__":
    import nltk; nltk.download('wordnet'); nltk.download('punkt'); nltk.download('stopwords')
    from ml import Model; model = Model('9_june_2020_v1')
    app.run(debug=True, threaded=False)
