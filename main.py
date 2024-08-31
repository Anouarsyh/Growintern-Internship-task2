from flask import Flask, render_template, request
from passlib.context import CryptContext

app = Flask(__name__)

# Configuration du contexte de chiffrement
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    deprecated="auto"
)

# Fonction pour évaluer la force du mot de passe
def check_password_strength(password):
    length_score = len(password) >= 8
    digit_score = any(char.isdigit() for char in password)
    upper_score = any(char.isupper() for char in password)
    lower_score = any(char.islower() for char in password)
    special_char_score = any(not char.isalnum() for char in password)
    
    score = sum([length_score, digit_score, upper_score, lower_score, special_char_score])
    
    if score == 5:
        return "Very Strong"
    elif score >= 3:
        return "Strong"
    elif score >= 2:
        return "Weak"
    else:
        return "Very Weak"

@app.route('/', methods=['GET', 'POST'])
def index():
    strength = None
    password = None
    
    if request.method == 'POST':
        password = request.form['password']
        strength = check_password_strength(password)
    
    return render_template('index.html', password=password, strength=strength)

if __name__ == '__main__':
    app.run(debug=True)
