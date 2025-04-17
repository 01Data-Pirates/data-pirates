from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import torch
from torchvision import models, transforms
from PIL import Image
import logging
import json

# Initialize Flask app with correct template and static folders
app = Flask(__name__, 
           template_folder='templates',
           static_url_path='',
           static_folder='static')

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize model
model = None
class_names = None
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

def load_model():
    global model, class_names
    try:
        # Load the model
        model_path = Path(__file__).parent.parent / 'models' / 'final_model.pt'
        checkpoint = torch.load(model_path, map_location=device)
        
        # Initialize model
        model = models.resnet18(pretrained=False)
        num_classes = len(checkpoint['class_names'])
        model.fc = torch.nn.Linear(model.fc.in_features, num_classes)
        
        # Load state dict
        model.load_state_dict(checkpoint['model_state_dict'])
        model = model.to(device)
        model.eval()
        
        class_names = checkpoint['class_names']
        logger.info(f"Model loaded successfully. Classes: {class_names}")
        
    except Exception as e:
        logger.error(f"Error loading model: {str(e)}")
        raise

def preprocess_image(image_path):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    
    image = Image.open(image_path).convert('RGB')
    image = transform(image)
    image = image.unsqueeze(0)  # Add batch dimension
    return image.to(device)

def predict_image(image_path):
    try:
        # Preprocess image
        image = preprocess_image(image_path)
        
        # Make prediction
        with torch.no_grad():
            outputs = model(image)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Get results
        predicted_class = class_names[predicted.item()]
        confidence_score = confidence.item()
        
        # Get probabilities for all classes
        class_probabilities = {
            class_name: prob.item() 
            for class_name, prob in zip(class_names, probabilities[0])
        }
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence_score,
            'class_probabilities': class_probabilities
        }
        
    except Exception as e:
        logger.error(f"Error making prediction: {str(e)}")
        raise

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file:
            # Save the uploaded file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get additional symptoms data
            age = request.form.get('age', '')
            duration = request.form.get('duration', '')
            symptoms = request.form.get('symptoms', '{}')
            notes = request.form.get('notes', '')
            
            try:
                symptoms = json.loads(symptoms)
            except:
                symptoms = {}
            
            # Make prediction
            result = predict_image(filepath)
            
            # Add image path and symptoms to result
            result['image_path'] = f'/static/uploads/{filename}'
            result['patient_data'] = {
                'age': age,
                'duration': duration,
                'symptoms': symptoms,
                'notes': notes
            }
            
            return jsonify(result)
            
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Load the model
    load_model()
    
    # Run the app
    logger.info("Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5000) 