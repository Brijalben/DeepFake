import dill
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder = 'template')

# Load the model
with open('model/model.pkl', 'rb') as file:
    model = dill.load(file)
    
@app.route('/')
def index():
    return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from the request
    data = request.files['image']

    # Perform prediction using the loaded model
    prediction = model.predict(data)

    # Return the prediction as JSON
    return jsonify({'prediction': prediction})

if __name__ == '__main__':
    app.run(debug=True)
