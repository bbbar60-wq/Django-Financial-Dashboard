# Django Financial Dashboard Project

This project is a Django-based financial dashboard that allows users to visualize and analyze financial data. The application fetches data from Alpha Vantage, processes it using pandas, and displays interactive charts using Plotly.

---
## 📜 Description

The primary goal of this project is to provide a user-friendly interface for tracking stock prices and other financial metrics. Users can select a stock symbol, and the dashboard will dynamically update to show historical price data, moving averages, and trading volumes. The backend is built with Django, handling API requests and data management, while the frontend uses Bootstrap for styling and Plotly for data visualization.

---
## ✨ Key Features

* **User Registration and Authentication**: Secure login and registration system for personalized access.
* **Dynamic Stock Symbol Selection**: Users can choose from a predefined list of popular stock symbols (e.g., AAPL, GOOGL, MSFT).
* **Interactive Financial Charts**: Visualizations include:
    * Candlestick charts for stock prices (Open, High, Low, Close).
    * Moving averages to identify trends.
    * Bar charts for trading volume.
* **External API Integration**: Fetches real-time and historical financial data from the Alpha Vantage API.
* **Data Processing with Pandas**: Efficiently handles and structures time-series data for analysis and visualization.
* **Asynchronous Updates**: The dashboard content is loaded dynamically, providing a smooth user experience.

---
## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

* Python 3.8+
* Django 3.0+
* Pandas
* Plotly
* Alpha Vantage API Key

### Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repository-url>
    cd <your-repository-name>
    ```

2.  **Install the required packages**:
    ```bash
    pip install django pandas plotly alpha-vantage
    ```

3.  **Get an Alpha Vantage API Key**:
    * Visit the [Alpha Vantage website](https://www.alphavantage.co/) to get your free API key.
    * Once you have the key, open `dashboard/views.py` and replace `'demo'` with your actual API key:
    ```python
    # In dashboard/views.py
    ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
    ```

4.  **Apply database migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Run the development server**:
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000/`.

---
## 🛠️ Usage

* Navigate to the homepage to see the main dashboard.
* Use the dropdown menu to select a stock symbol.
* The charts will automatically update to reflect the data for the chosen symbol.
* You can register a new account or log in to access personalized features in the future.

---
## 💻 Project Structure

* **`finance_project/`**: The main Django project directory.
    * `settings.py`: Project settings, including database and app configurations.
    * `urls.py`: Main URL routing for the project.
* **`dashboard/`**: The Django app for the financial dashboard.
    * `views.py`: Contains the logic for fetching data and rendering views.
    * `urls.py`: URL routing specific to the dashboard app.
    * `templates/`: HTML templates for the dashboard pages.
* **`users/`**: The Django app for user management.
    * `views.py`: Handles user registration and login.
    * `templates/`: HTML templates for registration and login forms.

---
## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or find any issues, please feel free to open an issue or submit a pull request.

---
## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
