import re


# ============================================================
# SKILL DICTIONARY
# ============================================================

SKILL_ALIASES = {

    "python": ["python", "python programming"],
    "java": ["java", "java programming"],
    "c": ["c programming"],
    "c++": ["c++"],

    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],

    "html": ["html", "html5"],
    "css": ["css", "css3"],

    "react": ["react", "react.js", "reactjs"],
    "node.js": ["node.js", "nodejs", "node"],
    "express.js": ["express.js", "express"],

    "rest api": [
        "rest api",
        "rest apis",
        "restful api",
        "restful apis"
    ],

    "sql": ["sql"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb", "mongo db"],
    "postgresql": ["postgresql", "postgres"],

    "git": ["git"],
    "github": ["github"],

    "docker": ["docker"],
    "aws": ["aws", "amazon web services"],
    "azure": ["azure"],

    "machine learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "deep learning": [
        "deep learning",
        "deep-learning",
        "dl"
    ],

    "artificial intelligence": [
        "artificial intelligence",
        "ai"
    ],

    "nlp": [
        "nlp",
        "natural language processing"
    ],

    "data science": [
        "data science",
        "data analytics"
    ],

    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],

    "tensorflow": ["tensorflow"],
    "pytorch": ["pytorch"],

    "streamlit": ["streamlit"],

    "dsa": [
        "dsa",
        "data structures",
        "data structures and algorithms",
        "algorithms"
    ],

    "oops": [
        "oops",
        "oop",
        "object oriented programming",
        "object-oriented programming"
    ],

    "dbms": [
        "dbms",
        "database management system"
    ],

    "operating systems": [
        "operating systems",
        "operating system",
        "os"
    ],

    "computer networks": [
        "computer networks",
        "computer network",
        "cn"
    ],

    "cloud": [
        "cloud computing",
        "cloud",
        "cloud deployment"
    ],
}


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text):
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#.\- ]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ============================================================
# SKILL EXTRACTION
# ============================================================

def extract_skills(text):

    text = normalize_text(text)

    found_skills = []

    for skill, aliases in SKILL_ALIASES.items():

        for alias in aliases:

            alias = normalize_text(alias)

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(alias)
                + r"(?![a-z0-9])"
            )

            if re.search(pattern, text):

                found_skills.append(skill)

                break

    return sorted(set(found_skills))


# ============================================================
# REQUIRED / PREFERRED SKILLS
# ============================================================

def extract_skill_categories(job_description):

    job_text = job_description.lower()

    required_skills = []
    preferred_skills = []

    required_match = re.search(
        r"(required skills?|must have|required qualifications?)"
        r"\s*:?(.*?)(?="
        r"preferred skills?|nice to have|good to have|"
        r"preferred qualifications?|responsibilities|"
        r"requirements|experience|education|$)",
        job_text,
        re.DOTALL
    )

    if required_match:

        required_text = required_match.group(2)

        required_skills = extract_skills(
            required_text
        )

    preferred_match = re.search(
        r"(preferred skills?|nice to have|good to have|"
        r"preferred qualifications?)"
        r"\s*:?(.*?)(?="
        r"required skills?|responsibilities|"
        r"requirements|experience|education|$)",
        job_text,
        re.DOTALL
    )

    if preferred_match:

        preferred_text = preferred_match.group(2)

        preferred_skills = extract_skills(
            preferred_text
        )

    all_job_skills = extract_skills(
        job_description
    )

    # If there are no explicit sections,
    # treat all detected skills as required.
    if not required_skills and not preferred_skills:

        required_skills = all_job_skills

    else:

        categorized = set(
            required_skills +
            preferred_skills
        )

        additional_skills = [
            skill
            for skill in all_job_skills
            if skill not in categorized
        ]

        required_skills.extend(
            additional_skills
        )

    return {
        "required": sorted(
            set(required_skills)
        ),
        "preferred": sorted(
            set(preferred_skills)
        ),
        "all": sorted(
            set(all_job_skills)
        )
    }


# ============================================================
# KEYWORD MATCHING
# ============================================================

def calculate_keyword_match(
    resume_text,
    job_description
):

    resume_skills = extract_skills(
        resume_text
    )

    categories = extract_skill_categories(
        job_description
    )

    job_skills = categories["all"]

    if not job_skills:

        return {
            "score": 0,
            "resume_skills": resume_skills,
            "job_skills": [],
            "required_skills": [],
            "preferred_skills": [],
            "matched": [],
            "missing": [],
            "matched_required": [],
            "missing_required": [],
            "matched_preferred": [],
            "missing_preferred": []
        }

    matched = [
        skill
        for skill in job_skills
        if skill in resume_skills
    ]

    missing = [
        skill
        for skill in job_skills
        if skill not in resume_skills
    ]

    matched_required = [
        skill
        for skill in categories["required"]
        if skill in resume_skills
    ]

    missing_required = [
        skill
        for skill in categories["required"]
        if skill not in resume_skills
    ]

    matched_preferred = [
        skill
        for skill in categories["preferred"]
        if skill in resume_skills
    ]

    missing_preferred = [
        skill
        for skill in categories["preferred"]
        if skill not in resume_skills
    ]

    score = (
        len(matched) /
        len(job_skills)
    ) * 100

    return {

        "score": round(score, 2),

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "required_skills":
            categories["required"],

        "preferred_skills":
            categories["preferred"],

        "matched": matched,

        "missing": missing,

        "matched_required":
            matched_required,

        "missing_required":
            missing_required,

        "matched_preferred":
            matched_preferred,

        "missing_preferred":
            missing_preferred
    }


# ============================================================
# REQUIRED SKILL SCORE
# ============================================================

def calculate_required_skill_score(result):

    required = result["required_skills"]

    matched = result["matched_required"]

    if not required:
        return 100

    return round(
        (len(matched) / len(required)) * 100,
        2
    )


# ============================================================
# TECHNICAL SKILL SCORE
# ============================================================

def calculate_skill_score(result):

    required = result["required_skills"]

    preferred = result["preferred_skills"]

    matched_required = result["matched_required"]

    matched_preferred = result["matched_preferred"]

    required_weight = 0.70
    preferred_weight = 0.30

    if required:

        required_score = (
            len(matched_required) /
            len(required)
        ) * 100

    else:

        required_score = 100

    if preferred:

        preferred_score = (
            len(matched_preferred) /
            len(preferred)
        ) * 100

    else:

        preferred_score = 100

    score = (
        required_score * required_weight +
        preferred_score * preferred_weight
    )

    return round(score, 2)


# ============================================================
# RESUME STRUCTURE
# ============================================================

def calculate_structure_score(resume_text):

    text = normalize_text(
        resume_text
    )

    sections = {

        "education": [
            "education"
        ],

        "skills": [
            "skills",
            "technical skills"
        ],

        "projects": [
            "projects",
            "project"
        ],

        "experience": [
            "experience",
            "work experience"
        ],
    }

    found = 0

    for keywords in sections.values():

        if any(
            keyword in text
            for keyword in keywords
        ):

            found += 1

    score = (
        found /
        len(sections)
    ) * 100

    return round(score, 2)


# ============================================================
# PROJECT RELEVANCE
# ============================================================

def calculate_project_relevance(
    resume_text,
    job_description
):

    normalized_resume = normalize_text(
        resume_text
    )

    job_result = calculate_keyword_match(
        normalized_resume,
        job_description
    )

    job_skills = job_result["job_skills"]

    if not job_skills:
        return 0

    project_words = [
        "project",
        "developed",
        "built",
        "implemented",
        "created",
        "designed"
    ]

    project_word_count = sum(
        1
        for word in project_words
        if word in normalized_resume
    )

    skill_match_ratio = (
        len(job_result["matched"]) /
        len(job_skills)
    )

    project_evidence = min(
        project_word_count / 3,
        1
    )

    score = (
        skill_match_ratio * 70 +
        project_evidence * 30
    )

    return round(score, 2)


# ============================================================
# FINAL ATS SCORE
# ============================================================

def calculate_ats_score(
    resume_text,
    job_description
):

    keyword_result = calculate_keyword_match(
        resume_text,
        job_description
    )

    keyword_score = (
        keyword_result["score"]
    )

    required_score = (
        calculate_required_skill_score(
            keyword_result
        )
    )

    skills_score = (
        calculate_skill_score(
            keyword_result
        )
    )

    project_score = (
        calculate_project_relevance(
            resume_text,
            job_description
        )
    )

    structure_score = (
        calculate_structure_score(
            resume_text
        )
    )

    job_relevance_score = required_score

    # --------------------------------------------------------
    # WEIGHTED SCORE
    #
    # Technical Skills     35%
    # Required Match       25%
    # Keyword Match        10%
    # Project Relevance    20%
    # Resume Structure     10%
    # --------------------------------------------------------

    overall_score = (

        skills_score * 0.35 +

        job_relevance_score * 0.25 +

        keyword_score * 0.10 +

        project_score * 0.20 +

        structure_score * 0.10

    )

    return {

        "overall_score":
            round(overall_score, 2),

        "keyword_score":
            keyword_score,

        "skills_score":
            skills_score,

        "job_relevance_score":
            job_relevance_score,

        "project_score":
            project_score,

        "structure_score":
            structure_score,

        "resume_skills":
            keyword_result["resume_skills"],

        "job_skills":
            keyword_result["job_skills"],

        "required_skills":
            keyword_result["required_skills"],

        "preferred_skills":
            keyword_result["preferred_skills"],

        "matched_skills":
            keyword_result["matched"],

        "missing_skills":
            keyword_result["missing"],

        "matched_required":
            keyword_result["matched_required"],

        "missing_required":
            keyword_result["missing_required"],

        "matched_preferred":
            keyword_result["matched_preferred"],

        "missing_preferred":
            keyword_result["missing_preferred"],
    }