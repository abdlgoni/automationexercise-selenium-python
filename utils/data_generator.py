from faker import Faker
import random
import time

class TestDataGenerator:
    
    def __init__(self, locale='id_ID'):
        self.fake = Faker(locale)
        
    def generate_user_data(self):
        """
        Generate random user data untuk registration
        Returns: Dict dengan user information
        """
        timestamp = int(time.time())
        
        return {
            'name': f"{self.fake.first_name()} {self.fake.last_name()}",
            'email': f"testuser{timestamp}@{self.fake.free_email_domain()}",
            'password': self.generate_password(),
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'company': self.fake.company(),
            'address1': self.fake.street_address(),
            'address2': "",
            'city': self.fake.city(),
            'state': self.fake.state(),
            'zipcode': self.fake.postcode(),
            'mobile': self.fake.phone_number(),
            'country': random.choice(['United States', 'Canada', 'India']),
        }
    
    def generate_password(self, length=10):
        """
        Generate random password yang memenuhi requirements
        Returns: Password string
        """
        # Password biasanya butuh: huruf besar, kecil, angka, simbol
        password = (
            self.fake.password(
                length=length,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True
            )
        )
        return password
    
    def generate_birth_date(self):
        """
        Generate random date of birth
        Returns: Dict dengan day, month, year
        """
        date = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
        
        months = [
            'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ]
        
        return {
            'day': str(date.day),
            'month': months[date.month - 1],
            'year': str(date.year)
        }
    
    def generate_title(self):
        """
        Generate random title (Mr/Mrs)
        Returns: 'Mr' or 'Mrs'
        """
        return random.choice(['Mr', 'Mrs'])
    
    def generate_unique_email(self):
        """
        Generate unique email dengan timestamp
        Returns: Email string
        """
        timestamp = int(time.time())
        username = self.fake.user_name()
        domain = self.fake.free_email_domain()
        return f"{username}{timestamp}@{domain}"
    
    
if __name__ == "__main__":
    # Example usage
    generator = TestDataGenerator()
    
    print("=" * 50)
    print("GENERATED USER DATA")
    print("=" * 50)
    user_data = generator.generate_user_data()
    for key, value in user_data.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 50)
    print("GENERATED BIRTH DATE")
    print("=" * 50)
    birth_date = generator.generate_birth_date()
    print(f"Day: {birth_date['day']}")
    print(f"Month: {birth_date['month']}")
    print(f"Year: {birth_date['year']}")
    
    print("\n" + "=" * 50)
    print("GENERATED CREDIT CARD")
    print("=" * 50)
    card_data = generator.generate_credit_card_data()
    for key, value in card_data.items():
        print(f"{key}: {value}")
    
    print("\n" + "=" * 50)
    print("GENERATED CONTACT FORM DATA")
    print("=" * 50)
    contact_data = generator.generate_contact_form_data()
    for key, value in contact_data.items():
        print(f"{key}: {value}")

