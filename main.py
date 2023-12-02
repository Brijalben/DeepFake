import torch
from torchvision import transforms
from PIL import Image
import io
import dill
from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import BadRequestKeyError


app = Flask(__name__, template_folder='template')

# Load the model
with open('model.pkl', 'rb') as file:
    model = dill.load(file)
    
# Define the image preprocessing pipeline
transform = transforms.Compose([ transforms.Resize((224, 224)),
                                transforms.ToTensor(),
                                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])])

def process_image(file):
    # Open the image using PIL
    image = Image.open(io.BytesIO(file.read()))
    
    # Preprocess the image
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)  # Add a batch dimension

    return input_batch


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the request
#         print(request.files)  # Debugging statement
        data = request.files['image']
        
        
         # Process the image
        input_batch = process_image(data)

        # Ensure the model is in evaluation mode
        model.eval()

        # Make predictions
        with torch.no_grad():
            _, output = model(input_batch)

        # Convert output to probabilities and get the predicted class
#         probabilities = torch.nn.functional.softmax(output[0], dim=0)
#         predicted_class = torch.argmax(probabilities).item()
            predicted_class = torch.argmax(output, dim=1).cpu().numpy()

        
        if predicted_class == 0:
            return "Image is real"
        else:
            return "Image is fake"
        # Return the prediction as JSON
#         return jsonify({'prediction': predicted_class}) #, 'probabilities': probabilities.tolist()})

        
    except BadRequestKeyError:
        return 'Bad Request: Image file not provided or with incorrect key', 400

if __name__ == '__main__':
    app.run(debug=True)