
import streamlit as st
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="ForgeSight AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 ForgeSight AI")
st.subheader("Manufacturing Quality Inspection")
st.write(
    "Upload a product image to explore the inspection workflow."
)

st.info(
    "Prototype mode: results are simulated. "
    "This version does not use AI to detect real defects."
)

with st.sidebar:
    st.header("Inspection Settings")
    part_id = st.text_input(
        "Part ID",
        value="PART-001"
    )
    inspector = st.text_input(
        "Inspector",
        value="Inspector"
    )

st.header("1. Upload a product image")

uploaded_file = st.file_uploader(
    "Choose a JPG, JPEG, or PNG image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    st.image(
        image,
        caption="Uploaded product image",
        use_container_width=True
    )

    st.header("2. Demo inspection")

    if st.button("Run demo inspection", type="primary"):
        st.session_state["inspection_done"] = True
        st.session_state["part_id"] = part_id
        st.session_state["inspector"] = inspector
        st.session_state["inspection_time"] = (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

    if st.session_state.get("inspection_done", False):
        st.warning(
            "Demo only: no defect detection was performed. "
            "A qualified person must inspect the actual part."
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Inspection status", "Review required")

        with col2:
            st.metric("AI defect score", "Not available")

        st.header("3. Human review")

        reviewed = st.checkbox(
            "I have reviewed the uploaded image."
        )

        if reviewed:
            review_note = st.text_area(
                "Review notes",
                placeholder="Enter observations from your own inspection."
            )

            st.success(
                "Review recorded in this session. "
                "This prototype does not save it to a database."
            )
        else:
            review_note = ""

        report = f"""
FORGESIGHT AI — DEMO INSPECTION REPORT

Part ID: {st.session_state.get("part_id", part_id)}
Inspector: {st.session_state.get("inspector", inspector)}
Date and time: {st.session_state.get("inspection_time", "Not recorded")}

Status: HUMAN REVIEW REQUIRED

Important:
This is a software demonstration.
No AI defect detection or automated quality assessment
has been performed.

Human review completed in this session: {"Yes" if reviewed else "No"}

Review notes:
{review_note if reviewed else "No review notes entered."}

Final manufacturing quality decisions must be made
using appropriate inspection procedures.
"""

        st.download_button(
            "Download inspection report",
            data=report,
            file_name="forgesight_inspection_report.txt",
            mime="text/plain"
        )

else:
    st.caption(
        "Your uploaded image and inspection controls will appear here."
    )

st.divider()
st.caption("ForgeSight AI | Manufacturing inspection prototype")
