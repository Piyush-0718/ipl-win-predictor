from flask import Flask, render_template, request
import pickle
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load the model with error handling
try:
    pipe = pickle.load(open('pipe (1).pkl', 'rb'))
    print("✅ Model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {str(e)}")
    pipe = None

# Model-supported teams
display_teams = [
    'Sunrisers Hyderabad', 'Mumbai Indians', 'Royal Challengers Bangalore',
    'Kolkata Knight Riders', 'Kings XI Punjab', 'Chennai Super Kings',
    'Rajasthan Royals', 'Delhi Daredevils'
]

cities = [
    'Bangalore', 'Chandigarh', 'Delhi', 'Mumbai', 'Kolkata', 'Jaipur',
    'Hyderabad', 'Chennai', 'Cape Town', 'Port Elizabeth', 'Durban',
    'Centurion', 'East London', 'Johannesburg', 'Kimberley',
    'Bloemfontein', 'Ahmedabad', 'Cuttack', 'Nagpur', 'Dharamsala',
    'Visakhapatnam', 'Pune', 'Raipur', 'Ranchi', 'Abu Dhabi', 'Sharjah'
]

@app.route('/')
def home():
    """Main page with form"""
    return render_template(
        'index.html',
        teams=sorted(display_teams),
        cities=sorted(cities),
        now=datetime.now(),
        form_data={}  # Initialize empty form data
    )

@app.route('/predict', methods=['POST'])
def predict():
    """Handle form submission"""
    try:
        # Get all form data
        form_data = {
            'batting_team': request.form.get('batting_team'),
            'bowling_team': request.form.get('bowling_team'),
            'city': request.form.get('city'),
            'target': request.form.get('target'),
            'score': request.form.get('score'),
            'overs': request.form.get('overs'),
            'wickets_lost': request.form.get('wickets_lost')
        }
        
        # Validate input
        errors = []
        if form_data['batting_team'] == form_data['bowling_team']:
            errors.append("Batting and Bowling teams must be different.")
        
        try:
            overs = float(form_data['overs'])
            decimal_part = overs - int(overs)
            if decimal_part not in {0.0, 0.5}:
                errors.append("Overs must be in increments of 0.5 (e.g., 10.0 or 10.5)")
            if overs == 0:
                errors.append("Overs must be greater than 0 to calculate CRR.")
        except:
            errors.append("Invalid overs value")
        
        if errors:
            return render_template(
                'index.html',
                teams=sorted(display_teams),
                cities=sorted(cities),
                errors=errors,
                form_data=form_data
            )
        
        # Convert to proper types
        target = int(form_data['target'])
        score = int(form_data['score'])
        wickets_lost = int(form_data['wickets_lost'])
        
        # Calculate match parameters
        runs_left = target - score
        balls_left = 120 - int(overs * 6)
        wickets_left = 10 - wickets_lost
        crr = score / overs
        rrr = (runs_left * 6) / balls_left if balls_left > 0 else 0

        # Create input DataFrame
        input_df = pd.DataFrame({
            'batting_team': [form_data['batting_team']],
            'bowling_team': [form_data['bowling_team']],
            'city': [form_data['city']],
            'runs_left': [runs_left],
            'balls_left': [balls_left],
            'wickets': [wickets_left],
            'total_runs_x': [target],
            'crr': [crr],
            'rrr': [rrr]
        })

        # Get prediction
        if pipe:
            result = pipe.predict_proba(input_df)
            loss = result[0][0]
            win = result[0][1]
        else:
            raise Exception("Model not loaded")
        
        return render_template(
            'index.html',
            teams=sorted(display_teams),
            cities=sorted(cities),
            batting_team=form_data['batting_team'],
            bowling_team=form_data['bowling_team'],
            selected_city=form_data['city'],
            win_probability=round(win * 100),
            loss_probability=round(loss * 100),
            prediction=True,
            form_data=form_data
        )
    
    except Exception as e:
        return render_template(
            'index.html',
            teams=sorted(display_teams),
            cities=sorted(cities),
            errors=[f"An error occurred: {str(e)}"],
            form_data=form_data if 'form_data' in locals() else {}
        )

@app.route('/test')
def test():
    """Test route to verify server is running"""
    return "✅ Server is running properly"

if __name__ == '__main__':
    try:
        print("🚀 Starting Flask server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    except Exception as e:
        print(f"❌ Failed to start server: {str(e)}")