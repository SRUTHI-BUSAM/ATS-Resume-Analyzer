import streamlit as st

from resume_parser import extract_text
from ats_analyzer import calculate_ats_score
from llm import generate_resume_suggestions


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="ATS Resume Analyzer",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, Helvetica, sans-serif;
}

.stApp {
    background-color: #f7f8fa;
    color: #111827;
}

/* Main content width */
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* General headings */
h1, h2, h3, h4 {
    color: #111827 !important;
    font-weight: 700 !important;
}

p, label, span, div {
    color: #374151;
}

/* Analysis result heading */
.analysis-title {
    color: #111827 !important;
    font-size: 30px;
    font-weight: 700;
    margin-bottom: 20px;
}

/* Main score card */
.score-card {
    background: #ffffff;
    border: 1px solid #dfe3e8;
    border-radius: 12px;
    padding: 28px 32px;
    margin-bottom: 35px;
}

.score-card-label {
    color: #4b5563 !important;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
}

.score-number {
    color: #111827 !important;
    font-size: 42px;
    font-weight: 700;
    line-height: 1.1;
}

.score-out-of {
    color: #6b7280 !important;
    font-size: 18px;
    margin-left: 5px;
}

.score-description {
    color: #374151 !important;
    font-size: 15px;
    line-height: 1.5;
    margin-top: 12px;
}

/* Section headings */
.section-title {
    color: #111827 !important;
    font-size: 24px;
    font-weight: 700;
    margin-top: 35px;
    margin-bottom: 18px;
}

.section-description {
    color: #6b7280 !important;
    font-size: 14px;
    margin-bottom: 20px;
}

/* Metric cards */
.metric-card {
    background: #ffffff;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    padding: 22px 18px;
    min-height: 105px;
}

.metric-title {
    color: #4b5563 !important;
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 10px;
}

.metric-value {
    color: #111827 !important;
    font-size: 27px;
    font-weight: 700;
}

/* Skill cards */
.skill-card {
    background: #ffffff;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    padding: 20px;
    min-height: 150px;
}

.skill-card-title {
    color: #111827 !important;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 15px;
}

/* Skill tags */
.skill-tag {
    display: inline-block;
    background: #f3f4f6;
    color: #374151 !important;
    border: 1px solid #d9dde3;
    border-radius: 5px;
    padding: 6px 10px;
    margin: 3px;
    font-size: 13px;
}

/* Missing skills */
.missing-skill {
    background: #fff7ed;
    color: #9a3412 !important;
    border: 1px solid #fed7aa;
    border-radius: 6px;
    padding: 9px 12px;
    margin: 5px 0;
    font-size: 13px;
}

/* No missing skills message */
.no-missing {
    color: #166534 !important;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 7px;
    padding: 12px 14px;
    font-size: 14px;
}

/* Resume structure */
.structure-card {
    background: #ffffff;
    border: 1px solid #dfe3e8;
    border-radius: 10px;
    padding: 20px;
}

.structure-score {
    color: #111827 !important;
    font-size: 28px;
    font-weight: 700;
}

.structure-message {
    color: #166534 !important;
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 7px;
    padding: 13px 15px;
    font-size: 14px;
}

/* Suggestions */
.suggestions-box {
    background: #ffffff;
    border: 1px solid #d9e0e8;
    border-radius: 8px;
    padding: 14px 16px;
    margin: 10px 0;
    color: #183b63;
    line-height: 1.6;
}

.suggestion-item {
    color: #374151 !important;
    padding: 10px 0;
    border-bottom: 1px solid #eeeeee;
    line-height: 1.5;
}

.suggestion-item:last-child {
    border-bottom: none;
}

/* Buttons */
.stButton > button {
    background-color: #2563eb;
    color: #ffffff !important;
    border: none;
    border-radius: 7px;
    padding: 9px 20px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #1d4ed8;
    color: #ffffff !important;
}

/* Horizontal separator */
hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 35px 0;
}

/* Prevent Streamlit markdown from creating unwanted dark/code boxes */
code {
    background: transparent !important;
    color: #374151 !important;
}

pre {
    background: transparent !important;
    color: #374151 !important;
    white-space: pre-wrap !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #9ca3af !important;
    font-size: 12px;
    margin-top: 45px;
}

</style>
""", unsafe_allow_html=True)
# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="app-title">ATS Resume Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="app-subtitle">'
    'Compare your resume with a job description and identify areas to improve.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown(
    '<div class="section-title">Resume Analysis</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Upload your resume and provide the complete job description.'
    '</div>',
    unsafe_allow_html=True
)


col1, col2 = st.columns(2, gap="large")


with col1:

    st.markdown(
        '<div class="input-title">Resume</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="input-description">'
        'Upload your resume in PDF or DOCX format.'
        '</div>',
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"],
        label_visibility="collapsed"
    )


with col2:

    st.markdown(
        '<div class="input-title">Job Description</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="input-description">'
        'Paste the complete job description used for the application.'
        '</div>',
        unsafe_allow_html=True
    )

    job_description = st.text_area(
        "Job Description",
        height=230,
        placeholder=(
            "Paste the complete job description here.\n\n"
            "Example:\n"
            "We are looking for a Software Developer with "
            "experience in Python, Java, SQL and machine learning."
        ),
        label_visibility="collapsed"
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

button_col1, button_col2, button_col3 = st.columns([1, 1.5, 1])

with button_col2:

    analyze_button = st.button(
        "Analyze Resume",
        use_container_width=True
    )


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if uploaded_file is None:

        st.warning("Please upload your resume before starting the analysis.")

    elif not job_description.strip():

        st.warning("Please enter the job description before starting the analysis.")

    else:

        with st.spinner("Analyzing your resume..."):

            try:

                # ------------------------------------------------
                # Extract Resume Text
                # ------------------------------------------------

                resume_text = extract_text(uploaded_file)

                if not resume_text or not resume_text.strip():

                    st.error(
                        "Unable to extract text from the uploaded resume."
                    )

                    st.stop()


                # ------------------------------------------------
                # ATS Analysis
                # ------------------------------------------------

                result = calculate_ats_score(
                    resume_text,
                    job_description
                )


                # Store result in session state
                st.session_state["analysis_result"] = result
                st.session_state["resume_text"] = resume_text
                st.session_state["job_description"] = job_description


            except Exception as e:

                st.error(
                    f"An error occurred while analyzing the resume: {e}"
                )

                st.stop()


# ============================================================
# DISPLAY RESULTS
# ============================================================

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]


    # ========================================================
    # ANALYSIS RESULT
    # ========================================================

    st.markdown(
        '<div class="section-title">Analysis Result</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="result-card">',
        unsafe_allow_html=True
    )

    score = result.get("overall_score", 0)

    if score >= 80:
        description = "Strong alignment with the job requirements."
    elif score >= 60:
        description = "Good alignment with the job requirements."
    elif score >= 40:
        description = "Moderate alignment with the job requirements."
    else:
        description = "Your resume may need improvement for this job."


    score_col1, score_col2 = st.columns([1, 2])

    with score_col1:

        st.markdown(
            '<div class="score-label">ATS Compatibility</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <span class="score-number">{score:.1f}</span>
            <span class="score-out-of">/ 100</span>
            """,
            unsafe_allow_html=True
        )

    with score_col2:

        st.markdown(
            '<div class="score-label">Overall Assessment</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="score-description">{description}</div>',
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================
    st.markdown(
        '<div class="section-title">Score Breakdown</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("Keyword Match", result["keyword_score"]),
        ("Technical Skills", result["skills_score"]),
        ("Job Relevance", result["job_relevance_score"]),
        ("Project Relevance", result["project_score"])
    ]

    for col, (title, value) in zip(
        [col1, col2, col3, col4],
        metrics
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">{title}</div>
                    <div class="metric-value">{value:.1f}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    # ---------------------------------------------------------
    # SKILL MATCH
    # ---------------------------------------------------------

    st.markdown("---")
    st.subheader("Skill Match")

    st.caption(
        "Skills identified from the resume and compared with the job description."
    )

    # Create two columns FIRST
    skill_col1, skill_col2 = st.columns(2)

    # ---------------------------------------------------------
    # MATCHED SKILLS
    # ---------------------------------------------------------

    with skill_col1:

        st.markdown("### Matched Skills")

        if result["matched_skills"]:

            matched_html = ""

            for skill in result["matched_skills"]:
                matched_html += f"""
                <span class="skill-tag">{skill}</span>
                """

            st.markdown(
                f"""
                <div class="skill-box">
                    {matched_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.info("No matching skills were detected.")


    # ---------------------------------------------------------
    # MISSING SKILLS
    # ---------------------------------------------------------

    with skill_col2:

        st.markdown("### Missing Skills")

        if result["missing_skills"]:

            missing_html = ""

            for skill in result["missing_skills"]:
                missing_html += f"""
                <span class="skill-tag missing">{skill}</span>
                """

            st.markdown(
                f"""
                <div class="skill-box">
                    {missing_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.success("No missing skills were detected.")

    # ========================================================
    # RESUME STRUCTURE
    # ========================================================

    st.markdown(
        '<div class="section-title">Resume Structure</div>',
        unsafe_allow_html=True
    )

    structure_score = result.get("structure_score", 0)

    structure_col1, structure_col2 = st.columns([1, 3])

    with structure_col1:

        st.metric(
            "Structure Score",
            f"{structure_score:.1f}%"
        )

    with structure_col2:

        if structure_score >= 75:

            st.success(
                "Your resume contains the main sections expected in a standard resume."
            )

        elif structure_score >= 50:

            st.info(
                "Some standard resume sections could be added or improved."
            )

        else:

            st.warning(
                "Several standard resume sections appear to be missing."
            )

    # ---------------------------------------------------------
    # RESUME SUGGESTIONS
    # ---------------------------------------------------------

    st.markdown("---")

    st.subheader("Resume Suggestions")

    st.caption(
        "Suggestions are generated only when you choose to view them."
    )

    if st.button("View Resume Suggestions"):

        try:

            # Send ATS analysis results to the LLM
            suggestions = generate_resume_suggestions(result)

            # -------------------------------------------------
            # HANDLE DIFFERENT LLM RETURN FORMATS
            # -------------------------------------------------

            if suggestions is None:

                st.warning(
                    "No suggestions were generated."
                )

            elif isinstance(suggestions, str):

                # LLM returned normal text
                st.markdown(suggestions)

            elif isinstance(suggestions, list):

                # LLM returned a list
                for suggestion in suggestions:

                    if suggestion:
                        st.markdown(
                            f"""
                            <div class="suggestion-box">
                                {suggestion}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            elif isinstance(suggestions, dict):

                # LLM returned dictionary / JSON

                for key, value in suggestions.items():

                    # Format section title
                    section_title = str(key).replace(
                        "_", " "
                    ).title()

                    st.markdown(
                        f"### {section_title}"
                    )

                    if isinstance(value, list):

                        for item in value:

                            st.markdown(
                                f"""
                                <div class="suggestion-box">
                                    {item}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.markdown(
                            f"""
                            <div class="suggestion-box">
                                {value}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

            else:

                # Handle objects returned by some LLM libraries
                if hasattr(suggestions, "text"):

                    st.markdown(
                        suggestions.text
                    )

                else:

                    # Last fallback
                    st.markdown(
                        str(suggestions)
                    )

        except Exception as e:

            st.error(
                f"Unable to generate suggestions: {e}"
            )
# ============================================================
# FOOTER
# ============================================================

st.markdown(
    '<div class="footer">ATS Resume Analyzer</div>',
    unsafe_allow_html=True
)