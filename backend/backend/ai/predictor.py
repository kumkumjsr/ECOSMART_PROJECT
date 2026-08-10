
import os

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "smart_recycling_model1.pth"
)


# =========================================================
# MODEL CLASSES
# =========================================================

CLASSES = [
    "Plastic",
    "Paper",
    "Glass",
    "Metal",
    "Organic",
    "Other"
]


# =========================================================
# IMAGE PREPROCESSING
# =========================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# =========================================================
# MODEL VARIABLE
# =========================================================

model = None


# =========================================================
# LOAD MODEL ONLY WHEN NEEDED
# =========================================================

def load_model():

    global model

    # If model is already loaded, reuse it
    if model is not None:
        return model

    # Create ResNet50
    model = models.resnet50(weights=None)

    # Change final layer for 6 classes
    model.fc = nn.Linear(
        model.fc.in_features,
        len(CLASSES)
    )

    # Load trained weights
    checkpoint = torch.load(
        MODEL_PATH,
        map_location="cpu"
    )

    model.load_state_dict(checkpoint)

    # Evaluation mode
    model.eval()

    return model


# =========================================================
# PREDICTION
# =========================================================

def predict_waste(image):

    try:

        # Load model only when prediction is requested
        current_model = load_model()

        # Open image
        if isinstance(image, str):
            image = Image.open(image)
        else:
            image = Image.open(image)

        # Make sure image is RGB
        image = image.convert("RGB")

        # Transform image
        image_tensor = transform(image)

        # Add batch dimension
        image_tensor = image_tensor.unsqueeze(0)

        # Prediction
        with torch.inference_mode():

            output = current_model(image_tensor)

            probabilities = torch.softmax(
                output,
                dim=1
            )

            confidence, predicted = torch.max(
                probabilities,
                1
            )

        # Get predicted class
        waste_type = CLASSES[predicted.item()]

        # Convert confidence to percentage
        confidence_score = round(
            confidence.item() * 100,
            2
        )

        return {
            "waste_type": waste_type,
            "confidence_score": confidence_score,
            "recommendation": get_recommendation(waste_type)
        }

    except Exception as e:

        return {
            "error": str(e)
        }


# =========================================================
# RECOMMENDATIONS
# =========================================================

def get_recommendation(waste_type):

    data = {

        "Plastic":
            "Recycle this plastic waste properly.",

        "Paper":
            "Send paper waste for recycling.",

        "Glass":
            "Reuse or recycle glass items.",

        "Metal":
            "Collect metal waste for recycling.",

        "Organic":
            "Use organic waste for composting.",

        "Other":
            "Dispose this waste properly."
    }

    return data.get(
        waste_type,
        "Dispose waste properly."
    )
