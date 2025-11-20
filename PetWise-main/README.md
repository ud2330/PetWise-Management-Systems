
---

# PetWise — Pet Management & Recommendation System

PetWise is a Flask-based platform that manages users, pets, adopters, sellers, and feedback using MongoDB.
It also provides product recommendations, pet training guides, breed information, and first-aid resources.
PetWise integrates external APIs to suggest pet products based on breed and user behavior.

---

## Features

* User Authentication (Signup, Login, Sessions)
* Manage Pet Listings (Dogs, Cats, Birds, Rabbits, etc.)
* Adopter & Seller Registration
* Store & Retrieve Data in MongoDB
* Product Search (Flipkart API)
* Pet Training Guides
* Breed Information Library
* First Aid & Health Guides
* Feedback System with Rating and Features
* Personalized Recommendation Logic (Rule-based + User Preferences)

---

## Tech Stack

* Python
* Flask
* MongoDB
* HTML, CSS, JavaScript
* RapidAPI (Flipkart Product Search)

---

## Project Structure

```
app.py
templates/
static/
uploads/
README.md
```

---

## Setup

### 1. Clone the repository

```
git clone https://github.com/yourusername/petwise.git
cd petwise
```

### 2. Create virtual environment

```
python -m venv venv
```

### 3. Activate environment

Windows PowerShell:

```
venv\Scripts\Activate
```

Windows CMD:

```
venv\Scripts\activate.bat
```

Linux/Mac:

```
source venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Start MongoDB

Make sure MongoDB is running locally:

```
mongod
```

### 6. Run the Flask application

```
python app.py
```

Visit the application at:

```
http://127.0.0.1:5000
```

---

## Core Modules

### User Management

* Login, logout, signup
* Session-based dashboard
* Store user details in MongoDB

### Pet Management

* Add pet details (name, breed, age, temperament, health, etc.)
* Link pets to registered users
* Store and retrieve pet profiles

### Adoption Module

* Adopter registration form
* Seller registration form
* View available sellers
* Adopt pet workflow

### Recommendation Engine

PetWise uses:

* Content-based filtering (breed → product suggestions)
* Rule-based logic (age, lifestyle → pet type suggestions)
* API-based product recommendations

### Product Search (API)

Fetches real-time pet products based on breed.

### Feedback System

Users can submit:

* Ratings
* Features
* Detailed feedback

All feedback is stored and displayed from MongoDB.

### Information Modules

* Breed Information
* Training Guides (all animals)
* First Aid
* Pet Health
* Product Categories

---

## API Configuration

Set your RapidAPI keys inside the code:

```
'x-rapidapi-key': 'YOUR_API_KEY'
'x-rapidapi-host': 'real-time-flipkart-api.p.rapidapi.com'
```

---

## Notes

* Ensure MongoDB is installed and running locally before launching the app.
* All templates must be placed in the `templates/` folder.
* Static files (CSS, JS, Images) must be stored inside `static/`.

---
