# ♻️ AI-Based Waste Segregation

An intelligent waste classification system using deep learning to automatically categorize waste into appropriate bins.

## 🎯 Features

- **Single Image Analysis**: Classify individual waste items with confidence scores
- **Batch Processing**: Process multiple images at once for faster segregation
- **Real-time Classification**: Using InceptionV3 pre-trained neural network
- **Visual Feedback**: Color-coded waste categories and sustainability tips
- **Web Interface**: Built with Streamlit for easy access

## 📂 Waste Categories

- 🟢 **Biodegradable**: Food waste, leaves, paper, cardboard
- 🔵 **Recyclable**: Plastic, glass, metal, aluminum
- 🔴 **Hazardous**: Batteries, medicines, chemicals, syringes
- 🟡 **E-Waste**: Computers, phones, electronics
- ⚫ **Non-Recyclable**: General waste

## 🚀 Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-waste-segregation.git
cd ai-waste-segregation
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. Push this repository to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Click "New app" and select your repository
4. Choose `app.py` as the main file
5. Deploy!

## 📁 Project Structure

```
ai-waste-segregation/
├── app.py                    # Main Streamlit application
├── config.py                 # Configuration and waste categories
├── requirements.txt          # Python dependencies
├── .gitignore               # Git ignore rules
├── README.md                # This file
│
├── utils/
│   ├── __init__.py
│   ├── classifier.py        # ML classifier logic
│   └── ui_components.py     # UI elements and styling
│
└── .streamlit/
    └── config.toml          # Streamlit configuration
```

## 🔧 Configuration

Edit `config.py` to customize:
- Waste categories and keywords
- Model confidence threshold
- UI appearance and messages

## 📊 Model Details

- **Model**: InceptionV3 (pre-trained on ImageNet)
- **Input Size**: 299x299 pixels
- **Confidence Threshold**: 10%
- **Top Predictions**: 5 results

## 🤝 How It Works

1. **Upload Image**: User uploads a waste image
2. **Preprocessing**: Image is resized and normalized
3. **Classification**: InceptionV3 model predicts waste type
4. **Categorization**: Prediction is mapped to waste categories
5. **Results**: Display classification with confidence score and bin info

## 📦 Dependencies

- **streamlit**: Web app framework
- **tensorflow**: Deep learning framework
- **pillow**: Image processing
- **numpy**: Numerical computations
- **opencv-python**: Computer vision library

## 🐛 Troubleshooting

### ModuleNotFoundError
Ensure all files are in correct directories and run `pip install -r requirements.txt`

### Model Loading Issues
First run may take time downloading InceptionV3. Be patient or restart app.

### Memory Issues
If running on limited resources, reduce image batch size in `config.py`

## 🌍 Environmental Impact

Proper waste segregation can:
- Reduce pollution by 50%
- Improve recycling efficiency by up to 3x
- Decrease landfill waste significantly

## 📝 License

This project is open source and available under the MIT License.

## 🙋 Support

For issues or questions, please open an issue on GitHub.

---

**Made with ♻️ for a sustainable future**
