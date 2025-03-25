import flask
from flask import Flask, request, render_template
from demo import enhanced_news_search  # New module we just created

# Initialize Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/main")
def about():
    return render_template("main.html")

@app.route("/prediction", methods=['GET', 'POST'])
def prediction():
    if request.method == "POST":
        news_headline = request.form['chatInput']
        print("Received headline:", news_headline)

        try:
            # Use the new enhanced search function
            search_results = enhanced_news_search(news_headline)

            return render_template("main.html",
                prediction_text="Most representative word: {}<br>Subtopics: {}".format(
                    search_results['primary_topic'],
                    ', '.join(search_results['subtopics'])
                ),
                similarities=search_results['similarities'],
                combined_score=search_results['combined_score']
            )

        except Exception as e:
            print(f"Error occurred during news search: {e}")
            return render_template("main.html", error="An error occurred while fetching news articles.")

    else:
        return render_template("main.html")

if __name__ == "__main__":
    app.run(debug=True)