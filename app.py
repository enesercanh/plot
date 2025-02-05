import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os
from flask import Flask, render_template, request
from flask_babel import Babel, _

# Initialize the Flask app and Babel for language support
app = Flask(__name__)
app.config['BABEL_DEFAULT_LOCALE'] = 'en'  # Set the default language
babel = Babel(app)

# Function to download stock data and create the plot
def create_stock_plot(stock_symbol):
    # Download stock data
    stock_data = yf.download(stock_symbol, start="2020-01-01", end="2023-01-01")
    
    # Calculate moving averages
    stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
    stock_data['SMA_200'] = stock_data['Close'].rolling(window=200).mean()
    
    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(stock_data['Close'], label=_('Close Price'), color='blue')
    plt.plot(stock_data['SMA_50'], label=_('50-Day SMA'), color='red', linestyle='--')
    plt.plot(stock_data['SMA_200'], label=_('200-Day SMA'), color='green', linestyle='--')
    plt.title(f'{stock_symbol} ' + _('Stock Price with Moving Averages'))
    plt.xlabel(_('Date'))
    plt.ylabel(_('Price in USD'))
    plt.legend()
    plt.grid()
    
    # Save the plot as an image file
    plot_filename = 'static/stock_plot.png'  # Save to the "static" folder
    plt.savefig(plot_filename)
    plt.close()  # Close the plot to avoid display issues

    return plot_filename

# Function to determine the language
@babel.localeselector
def get_locale():
    # Automatically select the language from the request headers, or use 'en' if not available
    return request.accept_languages.best_match(['en', 'ar'])

@app.route('/', methods=['GET', 'POST'])
def home():
    plot_path = None
    if request.method == 'POST':
        stock_symbol = request.form.get('stock_symbol')  # Get the stock ticker from form
        if stock_symbol:
            plot_path = create_stock_plot(stock_symbol)  # Generate the plot
    
    # Render the webpage with the plot path
    return render_template('index.html', plot_path=plot_path)

if __name__ == '__main__':
    app.run(debug=True)
