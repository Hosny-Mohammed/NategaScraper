import requests
from bs4 import BeautifulSoup
import csv


def get_token(url):
    session = requests.Session()
    response = session.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    token = soup.find('input', {'name': '__RequestVerificationToken'})
    if token:
        return session, token['value']
    return None, None


def scrape_grades(session, seat_number, token):
    url = "https://nategafany.emis.gov.eg/"
    data = {"SeatNumber": seat_number, "__RequestVerificationToken": token}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": url,
        "Origin": "https://nategafany.emis.gov.eg"
    }
    try:
        response = session.post(url, data=data, headers=headers, allow_redirects=True)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error requesting seat number {seat_number}: {str(e)}")
        return {"Seat Number": seat_number, "Error": str(e)}

    soup = BeautifulSoup(response.content, 'html.parser')
    results = {"Seat Number": seat_number}
    try:
        error_message = soup.find('span', {'id': 'seatNumberError'})
        if error_message and error_message.text:
            print(f"Error message for seat number {seat_number}: {error_message.text}")
            results["Error"] = error_message.text
            return results
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all(['th', 'td'])
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    results[key] = value
    except Exception as e:
        print(f"Error parsing results for seat number {seat_number}: {str(e)}")
        results["Error"] = str(e)
    return results


def main():
    url = "https://nategafany.emis.gov.eg/"
    session, token = get_token(url)
    if token:
        start_seat = int(input("Enter the start seat number: "))
        end_seat = int(input("Enter the end seat number: "))
        results_data = []
        for seat_number in range(start_seat, end_seat + 1):
            results = scrape_grades(session, seat_number, token)
            results_data.append(results)
        fieldnames = set()
        for row in results_data:
            fieldnames.update(row.keys())
        fieldnames = sorted(list(fieldnames))
        with open('grades.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in results_data:
                writer.writerow(row)
    else:
        print("Failed to capture the token.")


if __name__ == "__main__":
    main()