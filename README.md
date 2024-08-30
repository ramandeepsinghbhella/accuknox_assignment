# Social Network API

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd social_network

2. **Build and run the Docker containers:**
   ```bash
    docker-compose up -d --build

3. **Apply makemigrations:**
   ```bash
    docker-compose run web python manage.py makemigrations
   
4. **Apply migrations:**
   ```bash
    docker-compose run web python manage.py migrate

5. **Create a superuser (optional for admin access):**
   ```bash
    docker-compose run web python manage.py createsuperuser

6. **Access the API at:**
   ```plaintext
   http://localhost:8000/

    
