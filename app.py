
import streamlit as st
from PIL import Image
from transformers import pipeline
from datetime import datetime

st.set_page_config(
    page_title="ForgeSight AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 ForgeSight AI")
st.subheader("AI-Assisted Manufacturing Inspection")

st.write(
    "Upload a manufactured part image to receive an AI-generated "
    "description and prepare a human-review report."
)

st.warning(
    "Prototype limitation: image descriptions are not reliable "
    "manufacturing defect detection. Do not use them to approve "
    "or reject real products."
)

@st.cache_resource(show_spinner="Loading the AI model...")
def load_model():
    return pipeline(
        "image-to-text",
        model="nlpconnect/vit-gpt2-image-captioning",
        device=-1
    )

with st.sidebar:
    st.header("Inspection Details")
    part_id = st.text_input("Part ID", "PART-001")
    inspector = st.text_input("Inspector name", "Inspector")

st.header("1. Upload a product image")

uploaded_file = st.file_uploader(
    "Choose a JPG, JPEG, or PNG image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded product image",
        use_container_width=True
    )

    st.header("2. AI image analysis")

    if st.button("Analyze image with AI", type="primary"):
        try:
            with st.spinner(
                "Loading the model and analyzing your image. "
                "The first run may take several minutes..."
            ):
                model = load_model()
                result = model(image, max_new_tokens=40)
                caption = result[0]["generated_text"].strip()

            st.session_state["caption"] = caption
            st.session_state["analyzed_part"] = part_id
            st.session_state["analysis_time"] = (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )

        except Exception as error:
            st.error(
                "The model could not run. The free hosting environment "
                "may have limited memory, or model setup may have failed."
            )
            st.caption(
                "Check the Streamlit app logs for the technical error."
            )
            st.code(str(error)[:1000])

    if "caption" in st.session_state:
        st.success("AI image description generated")

        st.markdown("### What the AI sees")
        st.write(st.session_state["caption"])

        st.info(
            "This is a general image description. It does not confirm "
            "that the part is defective or defect-free."
        )

        st.header("3. Human review")

        reviewed = st.checkbox(
            "I have personally reviewed the uploaded image."
        )

        notes = st.text_area(
            "Inspection notes",
            placeholder=(
                "Record observations from your own inspection."
            )
        )

        if reviewed:
            st.success("Human review marked as complete for this session.")

        report = f"""
FORGESIGHT AI — IMAGE ANALYSIS REPORT

Part ID: {st.session_state.get("analyzed_part", part_id)}
Inspector: {inspector}
Analysis time: {st.session_state.get("analysis_time", "Unknown")}

AI-generated image description:
{st.session_state["caption"]}

Human review completed: {"Yes" if reviewed else "No"}

Inspector notes:
{notes if reviewed else "Review not confirmed."}

IMPORTANT:
The AI generated a general image description.
It did not perform validated manufacturing defect detection.
No automated pass/fail decision has been made.
"""

        st.download_button(
            "Download analysis report",
            data=report,
            file_name="forgesight_analysis_report.txt",
            mime="text/plain"
        )

else:
    st.caption("Upload an image to begin.")

st.divider()
st.caption("ForgeSight AI | AI image analysis prototype")


   
       
            
