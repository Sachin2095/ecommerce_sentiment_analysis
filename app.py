from flask import Flask, render_template, request
from pipelines.process import AnalysisText
app = Flask(__name__)



@app.route("/", methods=["GET", "POST"])
def text():
    
    if request.method == "POST":
        review = request.form.get("review")
        sentiment = AnalysisText(review)
        return render_template("index.html", sentiment=sentiment)
    
    elif request.method == 'GET':
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True,port=8000)
