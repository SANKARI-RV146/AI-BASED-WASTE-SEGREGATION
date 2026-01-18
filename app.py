"""
Main Streamlit App - AI-Based Waste Segregation
"""

import sys
import os

# Add the current directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import streamlit as st
from PIL import Image

# Import configuration
try:
    from config import APP_CONFIG, WASTE_CATEGORIES
except ImportError as e:
    st.error(f"Failed to import config: {e}")
    st.stop()

# Import classifier
try:
    from utils.classifier import WasteClassifier
except ImportError as e:
    st.error(f"Failed to import WasteClassifier: {e}")
    st.stop()

# Import UI components
try:
    from utils.ui_components import (
        display_header, 
        display_waste_info,
        display_single_result,
        display_batch_statistics,
        display_batch_gallery,
        display_footer
    )
except ImportError as e:
    st.error(f"Failed to import UI components: {e}")
    st.stop()


# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title=APP_CONFIG["page_title"],
    page_icon=APP_CONFIG["page_icon"],
    layout=APP_CONFIG["layout"]
)

# ===== INITIALIZE CLASSIFIER =====
classifier = WasteClassifier()

# ===== MAIN APP =====
def main():
    # Display header
    display_header()
    
    # Display waste categories info
    display_waste_info()
    
    st.markdown("---")
    
    # Create tabs for different modes
    tab1, tab2 = st.tabs(["📷 Single Image", "🗂️ Batch Analysis"])
    
    # ===== TAB 1: SINGLE IMAGE ANALYSIS =====
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            uploaded_file = st.file_uploader(
                "Upload a waste image",
                type=["jpg", "jpeg", "png"],
                key="single_image",
                help="Choose a clear image of waste to classify"
            )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.image(image, caption="Uploaded Image", use_container_width=True)
            
            with col2:
                if st.button("🔍 Analyze", use_container_width=True, key="analyze_single"):
                    try:
                        with st.spinner("⏳ Analyzing image..."):
                            prediction, confidence, all_predictions = classifier.classify_image(image)
                            
                            if prediction and confidence >= 10:
                                waste_type, bin_info = classifier.get_waste_category(prediction)
                                display_single_result(prediction, confidence, waste_type, bin_info)
                                
                                # Show all predictions
                                with st.expander("📋 All Predictions"):
                                    for pred, class_name, conf in all_predictions:
                                        conf_pct = conf * 100
                                        st.text(f"{class_name.title()}: {conf_pct:.2f}%")
                                
                                # Sustainability message
                                st.info(
                                    "🌍 **Did you know?** Proper waste segregation can reduce "
                                    "pollution by 50% and improve recycling efficiency by up to 3x!"
                                )
                            else:
                                st.warning("⚠️ Could not classify with high confidence. Try a clearer image.")
                    except Exception as e:
                        st.error(f"❌ Error during analysis: {str(e)}")
                        import traceback
                        st.error(traceback.format_exc())
    
    # ===== TAB 2: BATCH ANALYSIS =====
    with tab2:
        st.markdown("Upload multiple waste images for batch classification and segregation.")
        
        uploaded_files = st.file_uploader(
            "Upload multiple waste images",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True,
            key="batch_images",
            help="Select 2-20 waste images to process at once"
        )
        
        if uploaded_files and st.button("🔍 Analyze Batch", use_container_width=True, key="analyze_batch"):
            with st.spinner(f"Processing {len(uploaded_files)} images..."):
                # Initialize segregation dictionary
                segregated = {details["bin"]: [] for details in WASTE_CATEGORIES.values()}
                
                # Process each image
                progress_bar = st.progress(0)
                for idx, uploaded_file in enumerate(uploaded_files):
                    image = Image.open(uploaded_file)
                    prediction, confidence, _ = classifier.classify_image(image)
                    
                    if prediction and confidence >= 10:
                        waste_type, bin_info = classifier.get_waste_category(prediction)
                        segregated[bin_info["bin"]].append({
                            "image": image,
                            "name": uploaded_file.name,
                            "prediction": prediction,
                            "confidence": confidence,
                            "waste_type": waste_type
                        })
                    
                    progress_bar.progress((idx + 1) / len(uploaded_files))
                
                # Display summary
                st.success("✅ Batch analysis complete!")
                
                # Show statistics
                display_batch_statistics(segregated)
                
                st.markdown("---")
                
                # Show detailed results
                st.markdown("### 📸 Segregated Results")
                display_batch_gallery(segregated)
    
    st.markdown("---")
    display_footer()

if __name__ == "__main__":
    main()
