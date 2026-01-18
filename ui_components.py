"""UI components and styling for the app"""

import streamlit as st
from config import WASTE_CATEGORIES

def display_header():
    """Display app header"""
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1>♻️ AI-Based Waste Segregation</h1>
            <p style='font-size: 18px; color: #666;'>
                Intelligent waste classification using Artificial Intelligence
            </p>
        </div>
    """, unsafe_allow_html=True)

def display_waste_info():
    """Display waste categories information"""
    st.markdown("### 📚 Waste Categories")
    
    cols = st.columns(5)
    for idx, (category, details) in enumerate(WASTE_CATEGORIES.items()):
        with cols[idx]:
            st.markdown(f"""
                <div style='
                    border: 2px solid {details["color"]};
                    border-radius: 10px;
                    padding: 15px;
                    text-align: center;
                    background-color: #f9f9f9;
                '>
                    <h3>{details["bin"]}</h3>
                    <p style='font-size: 12px; color: #666;'>{details["description"]}</p>
                </div>
            """, unsafe_allow_html=True)

def display_single_result(prediction, confidence, waste_type, bin_info):
    """Display single image classification result"""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Detected Object")
        st.info(f"**{prediction.title()}**")
        st.metric("Confidence", f"{confidence:.2f}%")
    
    with col2:
        st.markdown("### 🗑️ Segregation")
        st.success(f"**Waste Type:** {waste_type}")
        st.success(f"**Bin:** {bin_info['bin']}")
        st.write(f"*{bin_info['description']}*")

def display_batch_statistics(segregated):
    """Display batch processing statistics"""
    st.markdown("### 📊 Segregation Summary")
    
    cols = st.columns(5)
    colors = ["green", "blue", "red", "yellow", "black"]
    
    for idx, (category, details) in enumerate(WASTE_CATEGORIES.items()):
        with cols[idx]:
            count = len(segregated.get(details["bin"], []))
            st.metric(details["bin"], count)

def display_batch_gallery(segregated):
    """Display batch results in organized gallery"""
    for bin_name, items in segregated.items():
        if items:
            with st.expander(f"{bin_name} - {len(items)} items", expanded=True):
                # Create columns for images
                num_cols = min(3, len(items))
                cols = st.columns(num_cols)
                
                for idx, item in enumerate(items):
                    with cols[idx % num_cols]:
                        st.image(item["image"], caption=item["name"], use_container_width=True)
                        st.markdown(f"""
                            **Object:** {item['prediction'].title()}  
                            **Confidence:** {item['confidence']:.2f}%  
                            **Type:** {item['waste_type']}
                        """)

def display_footer():
    """Display app footer"""
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <p>♻️ <b>SDG 12:</b> Responsible Consumption and Production</p>
            <p style='font-size: 12px; color: #999;'>Powered by AI | TensorFlow InceptionV3</p>
        </div>
    """, unsafe_allow_html=True)
