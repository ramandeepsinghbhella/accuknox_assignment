# Social Network API

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd social_network

2. **Build and run the Docker containers:**
   ```bash
    docker-compose up --build

3. **Apply migrations:**
   ```bash
    docker-compose run web python manage.py migrate

4. **Create a superuser (optional for admin access):**
   ```bash
    docker-compose run web python manage.py createsuperuser

5. **Access the API at:**
   ```plaintext
   http://localhost:8000/

    