"""Waste classification module"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input, decode_predictions
from config import WASTE_CATEGORIES, MODEL_CONFIG
import streamlit as st

class WasteClassifier:
    def __init__(self):
        self.model = None
    
    def load_model(self):
        """Load pre-trained InceptionV3 model"""
        try:
            if self.model is None:
                st.info("📥 Loading AI model for the first time (this may take a moment)...")
                self.model = InceptionV3(weights='imagenet')
                st.success("✅ Model loaded successfully!")
            return self.model
        except Exception as e:
            st.error(f"❌ Error loading model: {str(e)}")
            return None
    
    def classify_image(self, image):
        """Classify a single image"""
        try:
            st.info("🔄 Preparing image...")
            
            # Prepare image
            img_array = np.array(image.convert('RGB'))
            img_size = MODEL_CONFIG["input_size"]
            img_resized = tf.image.resize(img_array, [img_size, img_size]).numpy()
            img_batch = np.expand_dims(img_resized, axis=0)
            img_preprocessed = preprocess_input(img_batch)
            
            st.info("🤖 Running prediction...")
            
            # Get predictions
            model = self.load_model()
            if model is None:
                return None, 0, "Failed to load model"
            
            predictions = model.predict(img_preprocessed, verbose=0)
            decoded = decode_predictions(predictions, top=MODEL_CONFIG["top_predictions"])[0]
            
            st.success("✅ Prediction complete!")
            
            # Filter predictions with confidence threshold
            threshold = MODEL_CONFIG["confidence_threshold"]
            high_confidence = [p for p in decoded if float(p[2]) * 100 > threshold]
            
            if not high_confidence:
                return None, 0, []
            
            top_prediction = high_confidence[0][1]
            confidence = float(high_confidence[0][2]) * 100
            
            return top_prediction, confidence, decoded
        except Exception as e:
            st.error(f"❌ Classification error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, 0, str(e)
    
    def get_waste_category(self, prediction):
        """Map prediction to waste category"""
        pred_lower = prediction.lower()
        
        for category, details in WASTE_CATEGORIES.items():
            if any(word in pred_lower for word in details["keywords"]):
                return category, details
        
        return "Non-Recyclable", WASTE_CATEGORIES["Non-Recyclable"]
