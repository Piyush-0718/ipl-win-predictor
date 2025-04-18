# 🏏 IPL Win Predictor

[![Live Demo](https://img.shields.io/badge/Live-Demo-brightgreen)](https://ipl-win-predictor-0o90.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3%2B-lightgrey)](https://flask.palletsprojects.com/)
[![Machine Learning](https://img.shields.io/badge/ML-Logistic%20Regression-orange)](https://scikit-learn.org/stable/modules/linear_model.html#logistic-regression)

A real-time win probability predictor for IPL matches powered by machine learning.

![Application Screenshot](./Screenshot%202025-04-18%20175652.png)

## ✨ Features

- **Live Prediction**: Calculates win probability during matches.
- **Interactive UI**: Dropdown selectors for teams and cities.
- **Input Validation**: Ensures proper over increments (0.5).
- **Persistent Form**: Retains all inputs after submission.
- **Responsive Design**: Works on desktop and mobile.

## 🛠️ Tech Stack

| Component        | Technology                |
|------------------|---------------------------|
| Frontend         | HTML5, Bootstrap 5        |
| Backend          | Python Flask              |
| Machine Learning | Scikit-learn (Logistic Regression) |
| Deployment       | Render                    |

## 🚀 Try It Out

1. Visit the live demo: [ipl-win-predictor-0o90.onrender.com](https://ipl-win-predictor-0o90.onrender.com)
2. Fill the form:
   - Select batting/bowling teams.
   - Choose host city.
   - Enter match details.
3. Click "Predict Probability".

## 📦 Local Setup

```bash
# 1. Clone repository
git clone https://github.com/Piyush-0718/ipl-win-predictor.git
cd ipl-win-predictor

# 2. Create virtual environment
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run application
python app.py

