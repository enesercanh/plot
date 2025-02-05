from flask import Flask, render_template, request
import yfinance as yf

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    stock_info = None
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        stock = yf.Ticker(symbol)
        stock_info = stock.history(period="1d")
        stock_info = stock_info.tail(1)  # Get the most recent day data
        stock_info = stock_info.to_dict(orient="records")[0]  # Convert to dictionary for easy access

    return render_template("index.html", stock_info=stock_info)

if __name__ == "__main__":
    app.run(debug=True)
