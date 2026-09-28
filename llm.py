import os

from dotenv import load_dotenv
from google import genai


# Load .env
load_dotenv()


def generate_resume_suggestions(
    resume_text,
    job_description,
    results
):
    """
    Uses Gemini to generate personalized
    resume improvement suggestions.

    The ATS score is calculated separately using
    deterministic Python logic.
    """

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        return (
            "⚠️ Gemini API key was not found.\n\n"
            "Please add GEMINI_API_KEY to your .env file."
        )

    try:

        client = genai.Client(
            api_key=api_key
        )

        matched = ", ".join(
            results.get(
                "matched_skills",
                []
            )
        )

        missing = ", ".join(
            results.get(
                "missing_skills",
                []
            )
        )

        prompt = f"""
You are an AI resume improvement assistant.

Analyze the candidate's resume against the
provided job description.

IMPORTANT RULES:

1. Do not invent skills, experience, achievements,
   metrics, companies, certifications or projects.

2. Only recommend improvements that are supported
   by the resume or job description.

3. Clearly distinguish between:
   - skills already present
   - skills missing from the resume
   - wording improvements

4. Do not claim that the candidate will get selected.

5. Give practical suggestions suitable for a student
   or entry-level software developer.

ATS INFORMATION:

Overall Score:
{results.get("overall_score", 0)}/100

Keyword Match:
{results.get("keyword_score", 0)}%

Technical Skills:
{results.get("skills_score", 0)}%

Job Relevance:
{results.get("job_relevance_score", 0)}%

Project Relevance:
{results.get("project_score", 0)}%

Resume Structure:
{results.get("structure_score", 0)}%

Matched Skills:
{matched}

Missing Skills:
{missing}


JOB DESCRIPTION:

{job_description}


RESUME:

{resume_text}


Provide the response using exactly these sections:

## SUMMARY

Give a short 2-3 sentence assessment.

## STRENGTHS

Give 3-5 specific strengths based on the resume.

## MISSING OR WEAK AREAS

Mention important missing or weak areas.

## IMPROVEMENT SUGGESTIONS

Give 4-6 practical suggestions.

## BULLET IMPROVEMENTS

Give up to 3 examples of how existing resume
bullets could be rewritten.

For every rewritten bullet:
- Do not invent metrics.
- Do not invent technologies.
- Preserve the original meaning.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:

            return response.text

        return (
            "The AI did not return any suggestions."
        )

    except Exception as e:

        return (
            "⚠️ Unable to generate AI suggestions.\n\n"
            f"Error: {str(e)}"
        )