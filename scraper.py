import requests
from bs4 import BeautifulSoup
import time

class GradeScraper:
    def __init__(self, demo_mode=False):
        self.session = None
        self.token = None
        self.base_url = "https://nategafany.emis.gov.eg/"
        self.demo_mode = demo_mode
        
    def initialize_session(self):
        """Initialize session and get verification token"""
        if self.demo_mode:
            # Demo mode - simulate successful initialization
            self.session = requests.Session()
            self.token = "demo_token_123456"
            return True
            
        try:
            self.session = requests.Session()
            response = self.session.get(self.base_url, timeout=10)  # Reduced timeout
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            token_input = soup.find('input', {'name': '__RequestVerificationToken'})
            
            if token_input and hasattr(token_input, 'get') and token_input.get('value'):
                self.token = token_input['value']
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error initializing session: {str(e)}")
            return False
    
    def scrape_grades(self, seat_number):
        """Scrape grades for a specific seat number"""
        if not self.session or not self.token:
            return {"Seat Number": seat_number, "Error": "Session not initialized"}
            
        if self.demo_mode:
            # Demo mode - return simulated data
            import random
            time.sleep(0.1)  # Simulate processing time
            
            # Simulate some errors for realistic demo
            if random.randint(1, 10) <= 2:  # 20% error rate
                return {
                    "Seat Number": seat_number,
                    "Error": "رقم الجلوس غير صحيح" if random.choice([True, False]) else "No grade data found"
                }
            
            # Simulate successful results with realistic Arabic grade data
            subjects = ["الرياضيات", "اللغة العربية", "اللغة الإنجليزية", "العلوم", "الدراسات الاجتماعية"]
            grades = ["أ", "ب+", "ب", "ج+", "ج"]
            
            result = {
                "Seat Number": seat_number,
                "اسم الطالب": f"طالب رقم {seat_number}",
                "المجموع الكلي": str(random.randint(200, 300)),
                "النسبة المئوية": f"{random.randint(60, 95)}%",
                "النتيجة": random.choice(["ناجح", "راسب"])
            }
            
            # Add some subject grades
            for i in range(random.randint(3, 5)):
                subject = random.choice(subjects)
                grade = random.choice(grades)
                result[subject] = grade
                
            return result
        
        data = {
            "SeatNumber": seat_number, 
            "__RequestVerificationToken": self.token
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": self.base_url,
            "Origin": "https://nategafany.emis.gov.eg"
        }
        
        try:
            response = self.session.post(
                self.base_url, 
                data=data, 
                headers=headers, 
                allow_redirects=True,
                timeout=10  # Reduced timeout
            )
            response.raise_for_status()
            
        except requests.RequestException as e:
            return {"Seat Number": seat_number, "Error": f"Request failed: {str(e)}"}
        
        # Parse response
        soup = BeautifulSoup(response.content, 'html.parser')
        results = {"Seat Number": seat_number}
        
        try:
            # Check for error messages
            error_message = soup.find('span', {'id': 'seatNumberError'})
            if error_message and error_message.text.strip():
                results["Error"] = error_message.text.strip()
                return results
            
            # Look for validation error messages
            validation_errors = soup.find_all('span', class_='field-validation-error')
            if validation_errors:
                error_text = ', '.join([err.text.strip() for err in validation_errors if err.text.strip()])
                if error_text:
                    results["Error"] = error_text
                    return results
            
            # Parse tables for grade information
            tables = soup.find_all('table')
            
            for table in tables:
                if hasattr(table, 'find_all'):
                    rows = table.find_all('tr')
                else:
                    continue
                for row in rows:
                    if hasattr(row, 'find_all'):
                        cols = row.find_all(['th', 'td'])
                    else:
                        continue
                    if len(cols) == 2:
                        key = cols[0].text.strip()
                        value = cols[1].text.strip()
                        if key and value:  # Only add non-empty key-value pairs
                            results[key] = value
            
            # If no meaningful data was found besides seat number
            if len(results) == 1:  # Only seat number
                results["Error"] = "No grade data found"
                
        except Exception as e:
            results["Error"] = f"Parsing failed: {str(e)}"
        
        return results
