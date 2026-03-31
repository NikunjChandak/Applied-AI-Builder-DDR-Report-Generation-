import streamlit as st
from extractor import extract_from_pdf
from ai_engine import generate_ddr_report
import os
import io

st.set_page_config(page_title="AI DDR Generator", layout="wide", page_icon="📄")

def render_report(report_json, images_map):
    st.markdown('<div class="report-header"><h2>📊 Detailed Diagnostic Report (DDR)</h2><p style="color:#aaa;margin-bottom:0;">Automatically Generated Analysis</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🏢 1. Property Issue Summary")
        st.info(report_json.get("property_issue_summary", "Not Available"))
        
        st.subheader("🔍 2. Probable Root Cause")
        st.write(report_json.get("probable_root_cause", "Not Available"))
        
    with col2:
        st.subheader("⚠️ 3. Severity Assessment")
        severity = report_json.get("severity_assessment", {})
        level = severity.get('level', 'Not Available')
        # Color code severity visually
        color = "red" if level.lower() in ["high", "critical"] else "orange" if level.lower() == "medium" else "green"
        st.markdown(f"**Level:** <span style='color:{color}; font-weight:bold; font-size:1.2em;'>{level}</span>", unsafe_allow_html=True)
        st.caption(f"**Reasoning:** {severity.get('reasoning', 'Not Available')}")
    
    st.divider()
    st.subheader("📍 4. Area-wise Observations")
    observations = report_json.get("area_observations", [])
    if not observations:
         st.write("Not Available")
    for idx, obs in enumerate(observations):
        st.markdown(f"#### {idx+1}. {obs.get('area_name', 'Unknown Area')}")
        st.write(obs.get("observation", "No observation details."))
        
        # Render relevant images below observation
        related_ids = obs.get("related_images", [])
        if related_ids:
            st.markdown("**Related Images:**")
            cols = st.columns(min(len(related_ids), 3))
            
            for i, img_id in enumerate(related_ids):
                with cols[i % 3]:
                    if img_id in images_map:
                        st.image(images_map[img_id], caption=f"ID: {img_id}", use_column_width=True)
                    else:
                        st.warning(f"Image {img_id} not available or not extracted.")
                        
    st.subheader("✅ 5. Recommended Actions")
    actions = report_json.get("recommended_actions", [])
    if not actions:
         st.write("Not Available")
    for action in actions:
         st.info(f"✔️ {action}")
         
    st.subheader("💡 6. Additional Notes")
    st.write(report_json.get("additional_notes", "Not Available"))
    
    st.subheader("❓ 7. Missing or Unclear Information")
    missing = report_json.get("missing_or_unclear_information", [])
    if isinstance(missing, list):
         for m in missing:
             st.warning(f"• {m}")
    else:
         st.warning(missing)


def add_custom_css():
    st.markdown("""
        <style>
        /* Modern font imports */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        .gradient-text {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
            font-size: 3.2rem;
            margin-bottom: 0px;
            padding-bottom: 0px;
            font-family: 'Inter', sans-serif;
        }
        
        .sub-gradient {
            color: #a1a1aa;
            font-size: 1.1rem;
            font-family: 'Inter', sans-serif;
            margin-bottom: 30px;
        }
        
        .report-header {
            background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #f5576c;
            margin-top: 30px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)

def main():
    add_custom_css()
    
    st.markdown('<h1 class="gradient-text">Applied AI Builder: DDR Hub ✨</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-gradient">Automate Detailed Diagnostic Reports (DDR) by beautifully merging inspection facts and thermal anomalies.</p>', unsafe_allow_html=True)
    
    # Try to load from environment first
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    
    with st.sidebar:
        st.header("Settings")
        st.info("💡 Leave API Key empty to run in **Free Demo Mode**!")
        api_key = st.text_input("Gemini API Key", value=env_api_key, type="password", help="Get this from Google AI Studio")
        st.markdown("[Get a free API Key here](https://aistudio.google.com/app/apikey)")
        st.markdown("---")
        st.header("Upload Data")
        inspection_file = st.file_uploader("Upload Inspection Report (PDF)", type=["pdf"])
        thermal_file = st.file_uploader("Upload Thermal Report (PDF)", type=["pdf"])
        
        generate_btn = st.button("Generate DDR", type="primary", use_container_width=True)
        
    if generate_btn:
        if not inspection_file or not thermal_file:
            st.error("Please upload both the Inspection Report and the Thermal Report (PDF).")
            return
            
        if not api_key:
            st.warning("⚠️ No API Key provided! Running in **FREE DEMO MODE** with simulated AI results.")
            api_key = "demo"
        
        with st.spinner("Extracting text and images from PDFs (PyMuPDF)..."):
             inspection_text, inspection_images = extract_from_pdf(inspection_file, prefix="inspection")
             thermal_text, thermal_images = extract_from_pdf(thermal_file, prefix="thermal")
             
             # Build an accessibility map for images when rendering
             all_images_map = {}
             for img in inspection_images:
                 all_images_map[img['id']] = img['image']
             for img in thermal_images:
                 all_images_map[img['id']] = img['image']
                 
        with st.expander("Show Extracted Logs", expanded=False):
             st.write(f"Inspection Extracted Images: {len(inspection_images)}")
             st.write(f"Thermal Extracted Images: {len(thermal_images)}")
             st.text_area("Inspection Text Preview", inspection_text[:500] + "...")
             st.text_area("Thermal Text Preview", thermal_text[:500] + "...")
             
        with st.spinner("Analyzing with Gemini 1.5 Pro and generating structured DDR..."):
             try:
                 report_json = generate_ddr_report(
                     api_key=api_key,
                     inspection_text=inspection_text,
                     inspection_images=inspection_images,
                     thermal_text=thermal_text,
                     thermal_images=thermal_images
                 )
                 
                 # Save into session state to keep it rendered safely across interactions
                 st.session_state["report_json"] = report_json
                 st.session_state["all_images_map"] = all_images_map
                 st.success("Successfully generated the DDR!")
             except Exception as e:
                 st.error(f"Failed to generate report: {e}")
                 
    # Finally, render the report if it exists in state
    if "report_json" in st.session_state:
        render_report(st.session_state["report_json"], st.session_state.get("all_images_map", {}))

if __name__ == "__main__":
    main()
