import os
import gc

# =========================================================
# LIMIT CPU / MEMORY USAGE
# =========================================================

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image


# =========================================================
# TORCH CPU THREAD LIMIT
# =========================================================

try:
    torch.set_num_threads(1)
    torch.set_num_interop_threads(1)
except RuntimeError:
    pass


# =========================================================
# MODEL PATH
# =========================================================

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "models",
    "smart_recycling_model1.pth",
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
    "Other",
]


# =========================================================
# IMAGE TRANSFORM
# =========================================================

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# =========================================================
# MODEL
# =========================================================

model = None


# =========================================================
# LOAD MODEL
# =========================================================

def load_model():

    global model

    # Already loaded
    if model is not None:
        return model

    # Check model file
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            f"Model file not found: {MODEL_PATH}"
        )

    print("Loading waste AI model...")

    # -----------------------------------------------------
    # Create ResNet50 WITHOUT pretrained weights
    # -----------------------------------------------------

    loaded_model = models.resnet50(
        weights=None
    )

    # -----------------------------------------------------
    # 6 output classes
    # -----------------------------------------------------

    loaded_model.fc = nn.Linear(
        loaded_model.fc.in_features,
        len(CLASSES),
    )

    # -----------------------------------------------------
    # Load checkpoint on CPU
    # -----------------------------------------------------

    checkpoint = torch.load(
        MODEL_PATH,
        map_location="cpu",
        weights_only=True,
    )

    # -----------------------------------------------------
    # Load model weights
    # -----------------------------------------------------

    loaded_model.load_state_dict(
        checkpoint,
        strict=True,
    )

    # -----------------------------------------------------
    # Evaluation mode
    # -----------------------------------------------------

    loaded_model.eval()

    # -----------------------------------------------------
    # CPU only
    # -----------------------------------------------------

    loaded_model.to("cpu")

    model = loaded_model

    # Free checkpoint memory
    del checkpoint
    del loaded_model

    gc.collect()

    print("Waste AI model loaded successfully.")

    return model


# =========================================================
# PREDICTION
# =========================================================

def predict_waste(image):

    image_obj = None

    try:

        # -------------------------------------------------
        # Load model only when user scans waste
        # -------------------------------------------------

        current_model = load_model()

        # -------------------------------------------------
        # Reset uploaded file
        # -------------------------------------------------

        if hasattr(image, "seek"):
            image.seek(0)

        # -------------------------------------------------
        # Open image
        # -------------------------------------------------

        image_obj = Image.open(image).convert("RGB")

        # -------------------------------------------------
        # Transform image
        # -------------------------------------------------

        image_tensor = transform(image_obj)

        image_tensor = image_tensor.unsqueeze(0)

        # -------------------------------------------------
        # Prediction
        # -------------------------------------------------

        with torch.inference_mode():

            output = current_model(
                image_tensor
            )

            probabilities = torch.softmax(
                output,
                dim=1,
            )

            confidence, predicted = torch.max(
                probabilities,
                dim=1,
            )

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        predicted_index = predicted.item()

        waste_type = CLASSES[predicted_index]

        confidence_score = round(
            confidence.item() * 100,
            2,
        )

        result = {
            "waste_type": waste_type,

            "confidence_score": confidence_score,

            "recommendation":
                get_recommendation(waste_type),
        }

        # -------------------------------------------------
        # Cleanup
        # -------------------------------------------------

        del output
        del probabilities
        del confidence
        del predicted
        del image_tensor

        image_obj.close()

        gc.collect()

        return result

    except Exception as e:

        print(
            f"Waste prediction error: {str(e)}"
        )

        try:

            if image_obj is not None:
                image_obj.close()

        except Exception:
            pass

        gc.collect()

        return {
            "error": str(e)
        }


# =========================================================
# RECOMMENDATIONS
# =========================================================

def get_recommendation(waste_type):

    recommendations = {

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
            "Dispose this waste properly.",
    }

    return recommendations.get(
        waste_type,
        "Dispose waste properly.",
    )