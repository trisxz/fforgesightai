
import streamlit as st
from PIL import Image
from transformers import pipeline
from datetime import datetime
import pandas as pd

st.set_page_config(
    page_title="ForgeSight AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 ForgeSight AI")
st.subheader("Manufacturing Quality Inspection")

st.write(
    "Analyze product images, record inspector observations, "
    "and generate inspection reports."
)

st.warning(
    "AI descriptions are not validated defect detection. "
    "Human inspection is required for all quality decisions."
)


@st.cache_resource
def load_model():
    return pipeline(
        "image-to-text",
        model="nlpconnect/vit-gpt2-image-captioning",
        device=-1
    )


if "history" not in st.session_state:
    st.session_state.history = []

if "caption" not in st.session_state:
    st.session_state.caption = None

if "image_key" not in st.session_state:
    st.session_state.image_key = None


with st.sidebar:
    st.header("Inspection Details")

    part_id = st.text_input("Part ID", "PART-001")
    inspector = st.text_input("Inspector name", "Inspector")
    line_name = st.text_input("Production line", "Line 1")


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

    image_key = (
        uploaded_file.name,
        uploaded_file.size
    )

    if st.session_state.image_key != image_key:
        st.session_state.image_key = image_key
        st.session_state.caption = None

    st.header("2. AI image description")

    if st.button("Analyze image with AI", type="primary"):
        try:
            with st.spinner("Analyzing image..."):
                model = load_model()
                result = model(image, max_new_tokens=40)

            st.session_state.caption = (
                result[0]["generated_text"].strip()
            )

        except Exception as error:
            st.error("Image analysis failed.")
            st.code(str(error)[:1000])

    if st.session_state.caption:
        st.success("AI description generated")
        st.write(st.session_state.caption)

        st.caption(
            "This is a general image description, not a "
            "confirmed assessment of product quality."
        )

        st.header("3. Inspector observations")

        defect_types = [
            "Scratch",
            "Crack",
            "Dent",
            "Discoloration",
            "Deformation",
            "Missing component",
            "Surface contamination",
            "Other",
            "No visible issue observed"
        ]

        observations = st.multiselect(
            "Select observations from your visual inspection",
            defect_types
        )

        severity = st.selectbox(
            "Observed severity",
            ["Not assessed", "Low", "Medium", "High"]
        )

        review_notes = st.text_area(
            "Inspector notes",
            placeholder=(
                "Describe the location, appearance, or "
                "measurements of any suspected defect."
            )
        )

        review_status = st.selectbox(
            "Inspection review status",
            [
                "Pending review",
                "Reviewed — further testing needed",
                "Reviewed — no issue observed"
            ]
        )

        st.caption(
            "Select 'No visible issue observed' only when appropriate. "
            "It does not prove the part is defect-free."
        )

        if st.button("Save inspection record"):
            if not part_id.strip():
                st.error("Please enter a Part ID.")
            else:
                record = {
                    "Date": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "Part ID": part_id.strip(),
                    "Inspector": inspector.strip(),
                    "Production line": line_name.strip(),
                    "AI description": st.session_state.caption,
                    "Observations": ", ".join(observations)
                    if observations else "None recorded",
                    "Severity": severity,
                    "Review status": review_status,
                    "Notes": review_notes
                }

                st.session_state.history.append(record)
                st.session_state.last_record = record

                st.success("Inspection record saved for this session.")

        if "last_record" in st.session_state:
            record = st.session_state.last_record

            report = f"""
FORGESIGHT AI — INSPECTION REPORT

Date: {record['Date']}
Part ID: {record['Part ID']}
Inspector: {record['Inspector']}
Production line: {record['Production line']}

AI-GENERATED IMAGE DESCRIPTION:
{record['AI description']}

HUMAN-RECORDED OBSERVATIONS:
{record['Observations']}

Observed severity: {record['Severity']}
Review status: {record['Review status']}

Inspector notes:
{record['Notes']}

LIMITATIONS:
The AI generated a general image description.
It did not confirm the presence or absence of defects.
No automated pass/fail decision was made.
Follow applicable manufacturing inspection procedures.
"""

            st.download_button(
                "Download inspection report",
                data=report,
                file_name=f"{record['Part ID']}_inspection.txt",
                mime="text/plain"
            )

else:
    st.info("Upload a product image to begin.")

st.divider()
st.header("4. Inspection history")

history = st.session_state.history

if history:
    df = pd.DataFrame(history)

    col1, col2, col3 = st.columns(3)

    col1.metric("Records this session", len(df))

    col2.metric(
        "Pending review",
        int((df["Review status"] == "Pending review").sum())
    )

    col3.metric(
        "Records with observations",
        int(
            (
                (df["Observations"] != "None recorded")
                & (
                    df["Observations"]
                    != "No visible issue observed"
                )
            ).sum()
        )
    )

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "Export inspection history as CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="forgesight_inspection_history.csv",
        mime="text/csv"
    )

else:
    st.write("No inspection records saved in this session yet.")

st.caption(
    "ForgeSight AI | AI-assisted inspection prototype"
)




   
       
            
