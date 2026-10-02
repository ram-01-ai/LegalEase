import streamlit as st
import requests
from docx import Document
from fpdf import FPDF
from io import BytesIO


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Header */
    .main-header {
        text-align: center;
        padding: 10px 0 25px 0;
    }

    .main-header h1 {
        font-size: 44px;
        margin-bottom: 5px;
    }

    .main-header p {
        font-size: 18px;
        color: #666666;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    /* Cards */
    .feature-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 15px;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 25px 0 10px 0;
        color: #777777;
        font-size: 13px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## ⚖️ LegalEase")

    st.caption("AI-Powered Legal Document Generator")

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "📄 Create Document",
            "📚 Document Types",
            "ℹ️ About"
        ]
    )

    st.markdown("---")

    st.caption("LegalEase v1.0")


# =========================================================
# HOME
# =========================================================

if page == "🏠 Home":

    st.markdown(
        """
        <div class="main-header">
            <h1>⚖️ LegalEase</h1>
            <p>AI-Powered Legal Document Generator</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "Create professional legal document drafts using "
        "AI. Enter your requirements, generate the document, "
        "edit it and download it."
    )

    st.markdown("### 🚀 What can LegalEase do?")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
            <div class="feature-card">

            ### 📄 Generate

            Create legal document drafts from your
            requirements using AI.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
            <div class="feature-card">

            ### ✏️ Edit

            Review and modify the generated document
            before downloading.

            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
            <div class="feature-card">

            ### ⬇️ Download

            Download your document as TXT, DOCX
            or PDF.

            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.markdown("### 📋 Supported Documents")

    st.write(
        """
        • Employment Contract

        • Non-Disclosure Agreement (NDA)

        • Lease Agreement

        • Other Agreements
        """
    )

    st.markdown("---")

    st.warning(
        "LegalEase generates draft documents for review. "
        "The generated content is not a substitute for "
        "advice from a qualified lawyer."
    )


# =========================================================
# CREATE DOCUMENT
# =========================================================

elif page == "📄 Create Document":

    st.markdown(
        """
        <div class="main-header">
            <h1>📄 Create Legal Document</h1>
            <p>Enter your document requirements below</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-title">📋 Document Details</div>',
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # INPUTS
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        document_type = st.selectbox(
            "📄 Document Type",
            [
                "Employment Contract",
                "Non-Disclosure Agreement (NDA)",
                "Lease Agreement",
                "Other Agreement"
            ]
        )

        effective_date = st.date_input(
            "📅 Effective Date"
        )

    with col2:

        parties = st.text_area(
            "👥 Parties Involved",
            placeholder="Example: ABC Company and Ravi Kumar",
            height=120
        )

    terms = st.text_area(
        "📝 Terms / Conditions",
        placeholder="Enter the important terms and conditions...",
        height=180
    )

    st.markdown("### 🚀 Generate")

    generate_button = st.button(
        "⚖️ Generate Legal Document",
        use_container_width=True,
        type="primary"
    )

    # =====================================================
    # GENERATE
    # =====================================================

    if generate_button:

        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not parties.strip():

            st.warning(
                "⚠️ Please enter the Parties Involved."
            )

            st.stop()

        if not terms.strip():

            st.warning(
                "⚠️ Please enter the Terms / Conditions."
            )

            st.stop()

        # -------------------------------------------------
        # DATA
        # -------------------------------------------------

        data = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "effective_date": str(effective_date)
        }

        # -------------------------------------------------
        # FASTAPI REQUEST
        # -------------------------------------------------

        try:

            with st.spinner(
                "⏳ Generating your legal document..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8000/generate-document",
                    json=data,
                    timeout=120
                )

            # =================================================
            # SUCCESS
            # =================================================

            if response.status_code == 200:

                result = response.json()

                st.success(
                    "✅ Document generated successfully!"
                )

                st.markdown(
                    '<div class="section-title">📄 Generated Document</div>',
                    unsafe_allow_html=True
                )

                document = result["document"]

                # -------------------------------------------------
                # EDITABLE PREVIEW
                # -------------------------------------------------

                edited_document = st.text_area(
                    "✏️ Review and Edit Your Document",
                    value=document,
                    height=600
                )

                # =================================================
                # DOWNLOADS
                # =================================================

                st.markdown(
                    '<div class="section-title">⬇️ Download</div>',
                    unsafe_allow_html=True
                )

                download_col1, download_col2 = st.columns(2)

                # -------------------------------------------------
                # TXT
                # -------------------------------------------------

                with download_col1:

                    st.download_button(
                        label="📄 Download TXT",
                        data=edited_document,
                        file_name="legal_document.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

                # -------------------------------------------------
                # DOCX
                # -------------------------------------------------

                doc = Document()

                for line in edited_document.split("\n"):

                    doc.add_paragraph(line)

                docx_file = BytesIO()

                doc.save(docx_file)

                docx_file.seek(0)

                with download_col2:

                    st.download_button(
                        label="📝 Download DOCX",
                        data=docx_file,
                        file_name="legal_document.docx",
                        mime=(
                            "application/vnd.openxmlformats-"
                            "officedocument.wordprocessingml.document"
                        ),
                        use_container_width=True
                    )

                # -------------------------------------------------
                # PDF
                # -------------------------------------------------

                st.markdown("### 📕 PDF")

                try:

                    pdf = FPDF()

                    pdf.set_auto_page_break(
                        auto=True,
                        margin=15
                    )

                    pdf.add_page()

                    pdf.set_font(
                        "Helvetica",
                        size=11
                    )

                    pdf_text = edited_document

                    pdf_text = (
                        pdf_text
                        .encode(
                            "latin-1",
                            "replace"
                        )
                        .decode("latin-1")
                    )

                    for line in pdf_text.split("\n"):

                        if line.strip() == "":

                            pdf.ln(5)

                        else:

                            pdf.multi_cell(
                                0,
                                7,
                                line,
                                wrapmode="CHAR"
                            )

                    pdf_bytes = bytes(
                        pdf.output()
                    )

                    st.download_button(
                        label="📕 Download PDF",
                        data=pdf_bytes,
                        file_name="legal_document.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )

                except Exception:

                    st.warning(
                        "PDF download is currently unavailable."
                    )

            # =================================================
            # FASTAPI ERROR
            # =================================================

            else:

                st.error(
                    "❌ FastAPI returned an error."
                )

                st.code(
                    response.text
                )

        # =====================================================
        # CONNECTION ERROR
        # =====================================================

        except requests.exceptions.ConnectionError:

            st.error(
                "❌ Could not connect to FastAPI."
            )

            st.info(
                "Start FastAPI using:"
            )

            st.code(
                "uvicorn legalEaseAPI.main:app --reload"
            )

        # =====================================================
        # TIMEOUT
        # =====================================================

        except requests.exceptions.Timeout:

            st.error(
                "⏳ Request timed out. "
                "Please try again."
            )

        # =====================================================
        # OTHER ERROR
        # =====================================================

        except Exception as error:

            st.error(
                "❌ Unexpected error occurred."
            )

            st.code(
                str(error)
            )


# =========================================================
# DOCUMENT TYPES
# =========================================================

elif page == "📚 Document Types":

    st.markdown(
        """
        <div class="main-header">
            <h1>📚 Document Types</h1>
            <p>Available legal document categories</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### 💼 Employment Contract

        An agreement between an employer and an employee
        covering employment terms and conditions.

        ---

        ### 🔐 Non-Disclosure Agreement (NDA)

        A document intended to establish confidentiality
        obligations between parties.

        ---

        ### 🏠 Lease Agreement

        A draft agreement covering the terms between
        a lessor and lessee.

        ---

        ### 📑 Other Agreement

        Use this option for other types of legal agreements.
        """
    )


# =========================================================
# ABOUT
# =========================================================

elif page == "ℹ️ About":

    st.markdown(
        """
        <div class="main-header">
            <h1>ℹ️ About LegalEase</h1>
            <p>AI-Powered Legal Document Generator</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        ### 🎯 Project Objective

        LegalEase is designed to help users create draft
        legal documents from structured information.

        ### ⚙️ Technology

        **Frontend**

        Streamlit

        **Backend**

        FastAPI

        **AI**

        Google Gemini

        **Document Generation**

        Python

        **File Formats**

        TXT • DOCX • PDF

        ### 🔄 Application Flow

        User Input

        ↓

        Streamlit Frontend

        ↓

        FastAPI Backend

        ↓

        Gemini AI

        ↓

        Generated Legal Document

        ↓

        Editable Preview

        ↓

        Download
        """
    )

    st.warning(
        "LegalEase is an academic/project application. "
        "Generated documents should be reviewed by a "
        "qualified legal professional before actual use."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="footer">

    ⚖️ <b>LegalEase</b> — AI-Powered Legal Document Generator

    <br><br>

    Generated documents are drafts for review and are not
    a substitute for advice from a qualified lawyer.

    </div>
    """,
    unsafe_allow_html=True
)