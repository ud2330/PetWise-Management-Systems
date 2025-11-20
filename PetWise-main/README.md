# PetWise

**PetWise** is an intelligent pet recommendation system that helps users find pets, products, and services tailored to their lifestyle, preferences, and environment.

## Features

- Pet recommendations based on user preferences
- Lifestyle and environment-based matching
- Suggests products and services for pet care
- Responsive interface with clean design

## Tech Stack

- **Frontend:** HTML, CSS, Bootstrap
- **Backend:** Python (Flask)
- **Templates:** HTML in `templates/` folder
- **Static Assets:** Images, CSS, JS in `static/`
- **Dependency Management:** `requirements.txt`

## Project Structure
  ```bash
  PetWise/
  ├── static/                  # Static files (CSS, images, JS)
  │   └── images/              # Images used in the project
  ├── templates/               # HTML templates
  ├── app.py                   # Main Flask application
  ├── package.json             # Node.js package info (if applicable)
  ├── package-lock.json        # Node.js lock file
  ├── requirements.txt         # Python dependencies
  └── README.md                # Project documentation
  ```

 ## Setup Instructions

- Clone the repository:
  ```bash
  git clone https://github.com/laradharshini/PetWise.git
  cd PetWise
- Create and activate a virtual environment:

  ```bash
  python -m venv env
  env\Scripts\activate      # For Windows
  # OR
  source env/bin/activate   # For macOS/Linux

- Install dependencies:

  ```bash
  pip install -r requirements.txt

- Run the Flask app:

  ```bash
  python app.py

- Open your browser and go to:
  ```bash
  http://localhost:5000/
