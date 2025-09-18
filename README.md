# 📊 Egyptian Education Grades Scraper

A web-based application built with Streamlit to scrape student results from the Egyptian Ministry of Education's technical diploma results website (`nategafany.emis.gov.eg`). This tool provides an interactive user interface to specify a range of seat numbers, visualize the scraping progress in real-time, and view, filter, and download the collected data.

## Live Demo 🚀

You can access and use a live version of this scraper here:
**[https://2e71e800-e701-40a7-ad5d-7afa34dd5dcd-00-1sx5yjqgz3fze.janeway.replit.dev/](https://2e71e800-e701-40a7-ad5d-7afa34dd5dcd-00-1sx5yjqgz3fze.janeway.replit.dev/)**

-----

## ✨ Key Features

  * **Interactive Web Interface:** A user-friendly UI built with Streamlit for easy configuration and operation.
  * **Live & Demo Modes:**
      * **Live Mode:** Scrapes data directly from the official website.
      * **Demo Mode:** Uses simulated data, perfect for testing or when the official website is unavailable.
  * **Real-Time Progress Tracking:** Monitor the scraping process with a progress bar and live metrics for the current seat number and completion status.
  * **Asynchronous Scraping:** Utilizes threading to perform the scraping in the background, ensuring the UI remains responsive and doesn't freeze.
  * **Start/Stop Functionality:** Users can start and stop the scraping process at any time.
  * **Interactive Results Table:** View the scraped data instantly in the app.
  * **Data Filtering:** Easily filter results to show only successful scrapes, only errors, or search for a specific seat number.
  * **CSV Export:** Download the final, filtered results to a CSV file for offline analysis.

-----

## ⚙️ How It Works

The application is composed of two main components:

1.  **`app.py` (Streamlit Frontend):**

      * Manages the user interface, including input fields for seat numbers and control buttons.
      * Initializes and manages a separate thread for the scraping task to keep the UI responsive.
      * Uses a queue to receive real-time updates (progress, results, errors) from the scraping thread.
      * Displays progress, metrics, and final results in an interactive DataFrame.

2.  **`scraper.py` (Scraping Backend):**

      * Contains the `GradeScraper` class which encapsulates all the scraping logic.
      * **Session Initialization:** Establishes a session with the target website and retrieves a `__RequestVerificationToken` required for POST requests.
      * **Iterative Scraping:** Sends POST requests for each seat number in the user-defined range.
      * **Data Parsing:** Uses BeautifulSoup to parse the HTML response and extract student information and grades.
      * **Error Handling:** Catches and reports common issues like invalid seat numbers, network errors, or parsing failures.
      * **Demo Data Simulation:** Generates realistic-looking fake data when running in Demo Mode.

-----

## 🚀 How to Run Locally

To run this application on your own machine, follow these steps:

1.  **Prerequisites:**

      * Python 3.7+

2.  **Clone the Repository:**

    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

3.  **Install Dependencies:**
    Make sure you have the required Python libraries installed.

    ```bash
    pip install streamlit pandas requests beautifulsoup4
    ```

4.  **Run the Streamlit App:**
    Execute the following command in your terminal:

    ```bash
    streamlit run app.py
    ```

    Your web browser should automatically open a new tab with the running application.

5.  **Use the Application:**

      * Choose between **Live Mode** and **Demo Mode**.
      * Enter the **Start Seat Number** and **End Seat Number**.
      * Click the **"🚀 Start Scraping"** button.
      * Monitor the progress and view the results as they appear.
      * Once complete, filter the data as needed and click the **"📥 Download Results as CSV"** button.

-----

## 📦 Dependencies

This project relies on the following Python libraries:

  * `streamlit`: For building the interactive web application.
  * `pandas`: For data manipulation and display.
  * `requests`: For making HTTP requests to the website.
  * `beautifulsoup4`: For parsing the HTML content.

-----

## 📄 Output File

The application allows you to download the scraped data as a CSV file (e.g., `grades_3025301_3025399.csv`). The file will contain the results, with each row corresponding to a single student's record. The columns may include:

  * `Seat Number`
  * `اسم الطالب` (Student Name)
  * `المجموع الكلي` (Total Grade)
  * `النسبة المئوية` (Percentage)
  * `النتيجة` (Result: Pass/Fail)
  * And individual columns for each subject's grade.
  * `Error`: This column will describe any issue encountered while scraping that specific seat number.
