import os
import django
import random
from faker import Faker
from django.contrib.auth.hashers import make_password

# Setup Django settings and initialize the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Assessment.settings')
django.setup()

# Now we can import our models
from Phonebook.models import User, Contact, SpamNumber

# Initialize Faker to generate fake data
fake = Faker()


# Function to populate the database
def populate_data():
    # Number of users, contacts, and spam numbers to generate
    num_users = 50
    num_contacts_per_user = 5
    spam_probability = 0.3  # 30% chance to mark a phone number as spam

    # Create random users
    for _ in range(num_users):
        name = fake.name()
        phone_number = fake.phone_number()
        email = fake.email()

        # Create user with a random password (adjusted for CustomUser model)
        user = User.objects.create(
            name=name,  # Use 'name' instead of 'username' or 'first_name'
            password=make_password(fake.password()),  # Ensure passwords are hashed
            phone_number=phone_number,  # Assuming you have this field in CustomUser
            email=email  # Assuming email exists in your CustomUser model
        )

        print(f"Created user: {name} - {phone_number}")

        # Create random contacts for this user
        for _ in range(num_contacts_per_user):
            contact_name = fake.name()
            contact_phone = fake.phone_number()

            # Add contact to the user's contact list
            Contact.objects.create(
                user=user,
                contact_name=contact_name,
                contact_number=contact_phone
            )

        # Randomly mark the phone number as spam
        if random.random() < spam_probability:
            # Ensure the user who reports the spam is included as 'reported_by'
            SpamNumber.objects.create(
                phone_number=phone_number,
                spam_status=True,
                reported_by=user  # Make sure the user is recorded as the one reporting spam
            )

    print("Database populated successfully!")


# Run the function to populate the database
if __name__ == '__main__':
    populate_data()
