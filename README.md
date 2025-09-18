# Egyptian Technical Diploma Results Scraper

This Python script, `NategaScraper.py`, is designed to scrape the results of Egyptian technical diploma students from the official results website (`nategafany.emis.gov.eg`). It iterates through a range of seat numbers provided by the user, extracts the results for each student, and saves the collected data into a CSV file named `grades.csv`.

## Live Website 🚀

You can access and use a live version of this scraper here:
**[https://2e71e800-e701-40a7-ad5d-7afa34dd5dcd-00-1sx5yjqgz3fze.janeway.replit.dev/](https://2e71e800-e701-40a7-ad5d-7afa34dd5dcd-00-1sx5yjqgz3fze.janeway.replit.dev/)**

---

## How It Works

The script performs the following actions:
1.  **Establishes a Session:** It initiates a session with the results website to maintain cookie persistence.
2.  **Retrieves Security Token:** It fetches a `__RequestVerificationToken` from the website's homepage. This token is crucial for authenticating subsequent POST requests.
3.  **User Input:** It prompts the user to enter a starting and an ending seat number.
4.  **Iterative Scraping:** It loops through each seat number in the specified range. For each number, it sends a POST request containing the seat number and the security token to retrieve the student's results.
5.  **Data Parsing:** It uses BeautifulSoup to parse the HTML response and extract the student's information, such as their name, school, and grades for each subject.
6.  **Error Handling:** If a seat number is invalid or if there's an issue with the request, the script records the error and continues to the next seat number.
7.  **CSV Export:** After processing all the seat numbers, it compiles all the collected data and saves it into a `grades.csv` file, with appropriate headers for each piece of information.

---

## How to Use

To use this script, follow these steps:

1.  **Install Dependencies:** Make sure you have the required Python libraries installed. You can install them using pip:
    ```bash
    pip install requests beautifulsoup4
    ```

2.  **Run the Script:** Execute the script from your terminal:
    ```bash
    python NategaScraper.py
    ```

3.  **Enter Seat Numbers:** When prompted, enter the starting and ending seat numbers for the range of students you want to look up.

    ```
    Enter the start seat number: 1001
    Enter the end seat number: 1050
    ```

4.  **Check the Output:** Once the script finishes, you will find a `grades.csv` file in the same directory. This file will contain the scraped results for all the seat numbers in the range you provided.

---

## Dependencies

This script relies on the following Python libraries:

* `requests`: For making HTTP requests to the website.
* `beautifulsoup4`: For parsing the HTML content of the web pages.
* `csv`: For writing the scraped data into a CSV file (this is a standard library and does not need to be installed separately).

---

## Output File: `grades.csv`

The script will generate a `grades.csv` file. This file will contain the results, with each row corresponding to a single student's record. The columns will include:

* Seat Number
* Student Name (اسم الطالب)
* School (المدرسة)
* Specialization (التخصص)
* Total Grade (المجموع الكلى)
* And individual columns for each subject's grade.

If an error occurred for a specific seat number (e.g., the seat number does not exist), the "Error" column will contain a description of the issue.
