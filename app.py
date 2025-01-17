from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from src.get_astrology import GetAstrology
from src.chat import AstrologyChatHandler
from dotenv import load_dotenv
import os 

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("GEMINI_API_KEY")  # Make sure to change this to a strong secret key

astrology = GetAstrology()
chat_handler = AstrologyChatHandler()

# Initialize the chat system when the app starts
chat_handler.initialize_system()
@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard.html')

@app.route('/horoscope', methods=['GET', 'POST'])
def horoscope():
    if request.method == 'POST':
        # User inputs their name, birth details, city, and country
        name = request.form['name']
        city = request.form['city']
        country = request.form['country']
        birth_data = {
            'year': int(request.form['year']),
            'month': int(request.form['month']),
            'day': int(request.form['day']),
            'hour': int(request.form['hour']),
            'minute': int(request.form['minute'])
        }

        # Fetch horoscope details
        horoscope_details = astrology.fetch_horoscope(name, birth_data, city, country)
        
        if "error" not in horoscope_details:
            # Generate a detailed description based on horoscope
            detailed_description = astrology.generate_detailed_description(horoscope_details)
            detailed_description = detailed_description.replace('**', '<br>')  # Format description

            return render_template('horoscope.html', horoscope=horoscope_details, detailed_description=detailed_description)
        else:
            return render_template('horoscope.html', error=horoscope_details["error"])

    return render_template('horoscope.html')


@app.route('/birth_chart', methods=['GET', 'POST'])
def birth_chart():
    error = None
    horoscope = None
    name = None
    city = None
    country = None
    birth_data = {}

    if request.method == 'POST':
        # Get form data and convert to appropriate types
        try:
            name = request.form['name']
            city = request.form['city']
            country = request.form['country']
            birth_data['year'] = int(request.form['year'])  # Convert year to int
            birth_data['month'] = int(request.form['month'])  # Convert month to int
            birth_data['day'] = int(request.form['day'])  # Convert day to int
            birth_data['hour'] = int(request.form['hour'])  # Convert hour to int
            birth_data['minute'] = int(request.form['minute'])  # Convert minute to int

            # Fetch horoscope
            horoscope_details = astrology.fetch_horoscope(name, birth_data, city, country)
            if "error" in horoscope_details:
                error = horoscope_details["error"]
            else:
                horoscope = horoscope_details
                # Generate detailed description
                detailed_description = astrology.generate_detailed_description(horoscope)
                detailed_description = detailed_description.replace('**', '<br>')

                # Pass horoscope and detailed description to the template
                return render_template('birth_chart.html', horoscope=horoscope, 
                                       name=name, city=city, country=country, 
                                       birth_data=birth_data, detailed_description=detailed_description)
        except ValueError as ve:
            error = f"Invalid input data: {str(ve)}"
        except Exception as e:
            error = f"Error generating horoscope: {str(e)}"

    return render_template('birth_chart.html', error=error, horoscope=horoscope,
                           name=name, city=city, country=country, birth_data=birth_data)

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chat.html')

@app.route('/chat/send', methods=['POST'])
def chat_send():
    if 'user' not in session:
        return jsonify({'error': 'Please login first'}), 401
        
    data = request.json
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        result = chat_handler.process_query(data['message'])
        if result['status'] == 'success':
            return jsonify({'response': result['response']})
        else:
            return jsonify({'error': result['message']}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/compare', methods=['GET', 'POST'])
def compare():
    if request.method == 'POST':
        person1_details = {
            "name": request.form.get("person1_name"),
            "date": request.form.get("person1_date"),
            "time": request.form.get("person1_time"),
            "location": request.form.get("person1_location")
        }
        
        person2_details = {
            "name": request.form.get("person2_name"),
            "date": request.form.get("person2_date"),
            "time": request.form.get("person2_time"),
            "location": request.form.get("person2_location")
        }

        # Add logic to process the data and generate compatibility results
        compatibility_score = 75  # Example score
        analysis = "This is a sample compatibility analysis."
        print(person1_details)
        print(person2_details)
        return render_template(
            'compare.html', 
            person1_details=person1_details, 
            person2_details=person2_details, 
            compatibility_score=compatibility_score, 
            analysis=analysis
        )
        
    return render_template('compare.html')

if __name__ == '__main__':
    app.run(debug=True)
