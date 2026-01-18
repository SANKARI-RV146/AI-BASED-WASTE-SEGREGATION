"""Waste classification module - Lightweight version"""

import numpy as np
from PIL import Image
import streamlit as st
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import WASTE_CATEGORIES, MODEL_CONFIG

class WasteClassifier:
    def __init__(self):
        """Initialize lightweight classifier"""
        self.waste_keywords = {
            "Biodegradable": ["banana", "fruit", "food", "green", "leaf", "plant", "wood", "paper", "apple", "orange"],
            "Recyclable": ["plastic", "bottle", "can", "aluminum", "glass", "metal", "blue", "transparent", "shiny"],
            "Hazardous": ["red", "danger", "wire", "battery", "chemical", "dark"],
            "E-Waste": ["black", "electronic", "device", "computer", "circuit", "gray"],
        }
    
    def classify_image(self, image):
        """Classify image using lightweight color/feature analysis"""
        try:
            st.info("🔄 Analyzing image...")
            
            # Resize image for analysis
            img_resized = image.resize((100, 100))
            img_array = np.array(img_resized)
            
            # Extract color features
            avg_color = img_array.mean(axis=(0, 1))
            r, g, b = avg_color[0], avg_color[1], avg_color[2]
            
            st.info("🤖 Running analysis...")
            
            # Simple color-based classification
            predictions = self._analyze_colors(r, g, b)
            
            st.success("✅ Analysis complete!")
            
            if predictions:
                top_pred = predictions[0]
                return top_pred[0], top_pred[1], predictions
            
            return None, 0, []
            
        except Exception as e:
            st.error(f"❌ Classification error: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, 0, str(e)
    
    def _analyze_colors(self, r, g, b):
        """Analyze image colors to predict waste type"""
        scores = {
            "Biodegradable": 0,
            "Recyclable": 0,
            "Hazardous": 0,
            "E-Waste": 0,
            "Non-Recyclable": 0
        }
        
        # Green = Biodegradable
        if g > r and g > b:
            scores["Biodegradable"] = 85.0
            scores["Recyclable"] = 10.0
            scores["E-Waste"] = 3.0
            scores["Hazardous"] = 2.0
        
        # Blue = Recyclable
        elif b > r and b > g:
            scores["Recyclable"] = 80.0
            scores["Biodegradable"] = 10.0
            scores["Non-Recyclable"] = 5.0
            scores["E-Waste"] = 5.0
        
        # Red = Hazardous
        elif r > g and r > b and r > 150:
            scores["Hazardous"] = 75.0
            scores["E-Waste"] = 15.0
            scores["Recyclable"] = 7.0
            scores["Non-Recyclable"] = 3.0
        
        # Dark/Gray = E-Waste or Non-recyclable
        elif r < 100 and g < 100 and b < 100:
            scores["E-Waste"] = 70.0
            scores["Non-Recyclable"] = 20.0
            scores["Hazardous"] = 10.0
        
        # Bright/Light = Recyclable
        elif r > 150 and g > 150 and b > 150:
            scores["Recyclable"] = 60.0
            scores["Biodegradable"] = 20.0
            scores["Non-Recyclable"] = 20.0
        
        # Default
        else:
            scores["Non-Recyclable"] = 40.0
            scores["Recyclable"] = 30.0
            scores["Biodegradable"] = 15.0
            scores["E-Waste"] = 10.0
            scores["Hazardous"] = 5.0
        
        # Sort by confidence
        sorted_predictions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Format as [(index, label, confidence), ...]
        predictions = []
        for label, conf in sorted_predictions:
            predictions.append((0, label, conf / 100.0))
        
        return predictions
    
    def get_waste_category(self, prediction):
        """Map prediction to waste category"""
        pred_lower = prediction.lower()
        
        for category, details in WASTE_CATEGORIES.items():
            if category.lower() in pred_lower or pred_lower in category.lower():
                return category, details
        
        return "Non-Recyclable", WASTE_CATEGORIES["Non-Recyclable"]

    
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
