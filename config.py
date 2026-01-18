# Configuration file for the Waste Segregation App

# Waste Categories and their properties
WASTE_CATEGORIES = {
    "Biodegradable": {
        "bin": "🟢 Green Bin",
        "color": "green",
        "description": "Food waste, leaves, paper, cardboard",
        "keywords": ["food", "banana", "fruit", "vegetable", "leaf", "plant", "paper", "wood", "cardboard", "cloth", "orange", "apple", "bread", "corn", "carrot"]
    },
    "Recyclable": {
        "bin": "🔵 Blue Bin",
        "color": "blue",
        "description": "Plastic, glass, metal, aluminum",
        "keywords": ["plastic", "bottle", "cup", "container", "bag", "can", "aluminum", "metal", "glass", "jar", "newspaper", "box", "wrapper"]
    },
    "Hazardous": {
        "bin": "🔴 Red Bin",
        "color": "red",
        "description": "Batteries, medicines, chemicals, syringes",
        "keywords": ["battery", "medicine", "chemical", "toxic", "hazard", "wire", "circuit", "electronic", "syringe"]
    },
    "E-Waste": {
        "bin": "🟡 Yellow Bin",
        "color": "yellow",
        "description": "Computers, phones, electronics, devices",
        "keywords": ["computer", "phone", "electronics", "device", "keyboard", "mouse", "cable", "laptop", "monitor"]
    },
    "Non-Recyclable": {
        "bin": "⚫ Black Bin",
        "color": "black",
        "description": "General waste",
        "keywords": []
    }
}

# Model Configuration
MODEL_CONFIG = {
    "model_name": "InceptionV3",
    "input_size": 299,
    "confidence_threshold": 10.0,
    "top_predictions": 5
}

# App Configuration
APP_CONFIG = {
    "page_title": "AI-Based Waste Segregation",
    "page_icon": "♻️",
    "layout": "wide",
    "theme": "light"
}
