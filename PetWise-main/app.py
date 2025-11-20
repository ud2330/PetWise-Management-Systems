from flask import Flask, render_template, request, redirect, url_for, flash # type: ignore
from pymongo import MongoClient # type: ignore
from flask import session # type: ignore
from bson import ObjectId # type: ignore


def get_current_user_id():
    return session.get('user_id')  # Assume you store user ID in the session when they log in

app = Flask(__name__)
app.secret_key = 'passwords'  # Necessary for flashing messages


# MongoDB connection string (replace with your actual connection string)
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]  # Database name
users_collection = db["user"]  # Collection for user details
pets_collection = db["pets"]  # Collection for pet details
adopters_collection = db["adopter"]  # Collection for adopters
sellers_collection = db["seller"]  # Collection for sellers
feedback_collection = db["feedback"] 
feedback_collection.insert_one({'test': 'data'})
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/index')
def get_started():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({"email": email, "password": password})
        
        if user:
            user_id=str(user["_id"])
            session['user_id']=user_id
            session['full_name'] = user.get('full_name', 'Guest')  # Ensure name is stored
            session['email'] = user.get('email', 'No Email')
           
            flash(f"Welcome, {session['full_name']}!", "success")
            return redirect(url_for('dashboard',user_id=user_id))

        else:
            flash("Invalid email or password.", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# 🔹 Feedback Route
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if 'full_name' not in session:  # Ensure user is logged in
        flash("Please log in to give feedback!", "warning")
        return redirect(url_for('login'))

    full_name = session.get('full_name', 'Guest')  # Fetch stored username

    if request.method == 'POST':
        features = request.form.getlist('features')  # Get selected features
        rating = request.form.get('rating', '0')
        feedback_text = request.form.get('feedback', '')

        feedback_data = {
            "full_name": full_name,  # Use session's username instead of defaulting to 'Guest'
            "features": features,
            "rating": rating,
            "feedback": feedback_text
        }
        
        feedback_collection.insert_one(feedback_data)  # Store feedback in DB
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for('feedback'))

    all_feedback = list(feedback_collection.find())  # Fetch all feedback

    return render_template('feedback.html', full_name=full_name, all_feedback=all_feedback)



@app.route('/details_forum', methods=['GET', 'POST'])
def details_forum():
    if request.method == 'POST':
        # Log the form data to check if it's being received correctly
        print(request.form)

        # Get the user details from the form
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone_number = request.form.get('phone_number')

        # Validate the data
        if not email or not password or not full_name or not phone_number:
            return "Some fields are missing", 400

        # Insert user details into MongoDB
        user = {
            "email": email,
            "password": password,
            "full_name": full_name,
            "phone_number": phone_number
        }
        user_id = users_collection.insert_one(user).inserted_id  # Get the user_id

        # Redirect to the pet details page and pass the user_id
        return redirect(url_for('login', user_id=user_id))

    return render_template('index.html')

@app.route('/dashboard/<user_id>')
def dashboard(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id) })  # Find user by ID
    # Check if user is found, else return a 404 error
    if user:
        return render_template('dashboard.html', user=user)
    else:
        return "User not found", 404
    
@app.route('/logout')
def logout():
    # Implement your logout logic here
    session.clear()  # Clear session data
    return redirect(url_for('login'))  # Redirect to the dashboard or login page
@app.route('/pet_details/<user_id>', methods=['GET', 'POST'])
def pet_details(user_id):
    if request.method == 'POST':
        # Collect pet details from the form
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        pet_type = request.form.get('petType')
        breed = request.form.get('breed')
        age = request.form.get('age')
        gender = request.form.get('gender')
        health = request.form.get('health')
        color = request.form.get('color')
        temperament = request.form.getlist('temperament')  # Multiple checkbox values
        product_use = request.form.get('productUse')

        # Store pet details in MongoDB, linking to the user_id
        pet_details = {
            "user_id": user_id,
            "name": name,
            "email": email,
            "phone": phone,
            "address": address,
            "pet_details": {
                "pet_type": pet_type,
                "breed": breed,
                "age": age,
                "gender": gender,
                "health": health,
                "color": color,
                "temperament": temperament,
                "product_use": product_use
            }
        }
        pets_collection.insert_one(pet_details)  # Insert pet details into MongoDB

        return redirect(url_for('dashboard', user_id=user_id))  # Redirect to dashboard after form submission
    return render_template('pet_details.html', user_id=user_id)
@app.route('/adopt/ ', methods=['GET'])
def adopt():
    user_id = get_current_user_id()  # Replace with your logic to get the current user's ID
    return render_template('adopt.html', user_id=user_id)

@app.route('/adopter_details/<user_id>', methods=['GET', 'POST'])
def adopter_details(user_id):
    # Fetch seller details from MongoDB for both GET and POST requests
    sellers = list(sellers_collection.find())  # Fetch all seller records from the collection
    
    if request.method == 'POST':
        try:
            # Get form data
            adopter_data = {
                'user_id': user_id,  # Optional: link to user_id
                'name': request.form['adopter-name'],  # Correctly retrieving names from form
                'phone': request.form['adopter-phone'],
                'email': request.form['adopter-email'],
                'address': request.form['adopter-address'],
                'preferences': request.form['adopter-preferences']
            }
            # Insert data into MongoDB
            adopters_collection.insert_one(adopter_data)
            flash('Adopter details submitted successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while submitting details: {str(e)}', 'error')

        return redirect(url_for('adopter_details', user_id=user_id))  # Redirect with user_id
    
    # Render the adopter details page, with sellers data passed
    return render_template('adopter_details.html', user_id=user_id, sellers=sellers)

@app.route('/adopt_pet/<seller_id>', methods=['POST'])
def adopt_pet(seller_id):
    # Logic for adopting the pet
    # You can add logic here to handle what happens when a user adopts a pet
    return redirect(url_for('adopter_details', user_id=user_id))
    
    return render_template('adopter_details.html', user_id=user_id, sellers=sellers)
@app.route('/seller_details/<user_id>', methods=['GET', 'POST'])
def seller_details(user_id):
    if request.method == 'POST':
        try:
            # Get form data
            seller_data = {
                'user_id': user_id,  # Link to user_id
                'name': request.form['seller-name'],
                'phone': request.form['seller-phone'],
                'email': request.form['seller-email'],
                'address': request.form['seller-address'],
                'pet': {
                    'type': request.form['pet-type'],
                    'gender': request.form['pet-gender'],
                    'age': request.form['pet-age'],
                    'breed': request.form['pet-breed'],
                    'health': request.form['pet-health'],
                    'color': request.form['pet-color']
                }
            }
            # Insert data into MongoDB
            sellers_collection.insert_one(seller_data)
            flash('Seller details submitted successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred while submitting details: {str(e)}', 'error')
        
        # Redirect with user_id
        return redirect(url_for('seller_details', user_id=user_id))
    return render_template('seller_details.html', user_id=user_id)

@app.route('/pet_health/', methods=['GET', 'POST'])
def pet_health():
    return render_template('pet_health.html')
@app.route('/firstaid', methods=['GET', 'POST'])
def firstaid():
    return render_template('firstaid.html')
@app.route('/pet_products/', methods=['GET', 'POST'])
def pet_products():
    return render_template('pet_products.html')
@app.route('/pettraining/', methods=['GET', 'POST'])
def pettraining():
    return render_template('pettraining.html')

# Pet Training Guides Routes
@app.route('/bird_products/')
def bird_products():
    return render_template('bird_products.html')
@app.route('/cat_products/')
def cat_products():
    return render_template('cat_products.html')  # Replace 'cat_training.html' with the actual template

@app.route('/dog_products/')
def dog_products():
    return render_template('dog_products.html')  # Replace 'dog_training.html' with the actual template

@app.route('/fish_products/')
def fish_products():
    return render_template('fish_products.html')  # Replace 'fish_training.html' with the actual template

@app.route('/hamster_products/')
def hamster_products():
    return render_template('hamster_products.html')  # Replace 'hamster_training.html' with the actual template

@app.route('/horse_products/')
def horse_products():
    return render_template('horse_products.html')  # Replace 'horse_training.html' with the actual template

@app.route('/pig_products/')
def pig_products():
    return render_template('pig_products.html')  # Replace 'pig_training.html' with the actual template

@app.route('/rabbit_products/')
def rabbit_products():
    return render_template('rabbit_products.html')  # Replace 'rabbit_training.html' with the actual template

@app.route('/squirrel_products/')
def squirrel_products():
    return render_template('squirrel_products.html')  # Replace 'squirrel_training.html' with the actual template

@app.route('/turtle_products/')
def turtle_products():
    return render_template('turtle_products.html')
@app.route('/breed_info/', methods=['GET', 'POST'])
def breed_info():
    return render_template('breed_info.html')
@app.route('/bird_info/')
def bird_info():
    return render_template('bird_info.html')  # Replace 'bird_training.html' with the actual template

@app.route('/cat_info/')
def cat_info():
    return render_template('cat_info.html')  # Replace 'cat_training.html' with the actual template

@app.route('/dog_info/')
def dog_info():
    return render_template('dog_info.html')  # Replace 'dog_training.html' with the actual template

@app.route('/fish_info/')
def fish_info():
    return render_template('fish_info.html')  # Replace 'fish_training.html' with the actual template

@app.route('/hamster_info/')
def hamster_info():
    return render_template('hamster_info.html')  # Replace 'hamster_training.html' with the actual template

@app.route('/horse_info/')
def horse_info():
    return render_template('horse_info.html')  # Replace 'horse_training.html' with the actual template

@app.route('/pig_info/')
def pig_info():
    return render_template('pig_info.html')  # Replace 'pig_training.html' with the actual template

@app.route('/rabbit_info/')
def rabbit_info():
    return render_template('rabbit_info.html')  # Replace 'rabbit_training.html' with the actual template

@app.route('/squirrel_info/')
def squirrel_info():
    return render_template('squirrel_info.html')  # Replace 'squirrel_training.html' with the actual template

@app.route('/turtle_info/')
def turtle_info():
    return render_template('turtle_info.html')
@app.route('/bird_training_guide')
def bird_training_guide():
    return render_template('bird_training.html')  # Replace 'bird_training.html' with the actual template

@app.route('/cat_training_guide/')
def cat_training_guide():
    return render_template('cat_training.html')  # Replace 'cat_training.html' with the actual template

@app.route('/dog_training_guide/')
def dog_training_guide():
    return render_template('dog_training.html')  # Replace 'dog_training.html' with the actual template

@app.route('/fish_training_guide/')
def fish_training_guide():
    return render_template('fish_training.html')  # Replace 'fish_training.html' with the actual template

@app.route('/hamster_training_guide/')
def hamster_training_guide():
    return render_template('hamster_training.html')  # Replace 'hamster_training.html' with the actual template

@app.route('/horse_training_guide/')
def horse_training_guide():
    return render_template('horse_training.html')  # Replace 'horse_training.html' with the actual template

@app.route('/pig_training_guide/')
def pig_training_guide():
    return render_template('pig_training.html')  # Replace 'pig_training.html' with the actual template

@app.route('/rabbit_training_guide/')
def rabbit_training_guide():
    return render_template('rabbit_training.html')  # Replace 'rabbit_training.html' with the actual template

@app.route('/squirrel_training_guide/')
def squirrel_training_guide():
    return render_template('squirrel_training.html')  # Replace 'squirrel_training.html' with the actual template

@app.route('/turtle_training_guide/')
def turtle_training_guide():
    return render_template('turtle_training.html')  # Replace 'turtle_training.html' with the actual template

@app.route('/get_products/', methods=['POST'])
def get_products():
    breed = request.json.get('breed', '')
    query = breed.replace(' ', '+')
    url = f"https://real-time-flipkart-api.p.rapidapi.com/product-search?q={query}&page=1&sort_by=popularity"
    
    headers = {
        'x-rapidapi-key': '1a19b65c7bmsh523235f128170f3p111febjsn9caaaee03f68',
        'x-rapidapi-host': 'real-time-flipkart-api.p.rapidapi.com'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an HTTPError if the status is 4xx, 5xx
        data = response.json()

        # Send data back to the client
        return jsonify({
            'success': True,
            'products': data.get('products', [])
        })
    
    except requests.RequestException as e:
        return jsonify({
            'success': False,
            'message': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        # Capture data from the form
        name = request.form.get('name', 'Anonymous')
        email = request.form.get('email')
        feedback_text = request.form.get('feedback')
        selected_features = request.form.getlist('features')
        rating = int(request.form.get('rating', 0))

        # Structure feedback data
        feedback_data = {
            "name": name,
            "email": email,
            "feedback": feedback_text,
            "features": selected_features,
            "rating": rating
        }
        feedback_collection.insert_one(feedback_data)

        flash("Thank you for your feedback!", "success")
        return redirect(url_for('feedback'))

    # Get all feedback for display
    all_feedback = list(feedback_collection.find({}))
    return render_template('feedback.html', all_feedback=all_feedback)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    data = request.json
    feedback_data = {
        "name": data.get("name", "Anonymous"),
        "email": data.get("email"),
        "feedback": data.get("feedback"),
        "features": data.get("features"),
        "rating": data.get("rating", 0)
    }
    feedback_collection.insert_one(feedback_data)
    return jsonify({"message": "Feedback submitted successfully!"}), 201