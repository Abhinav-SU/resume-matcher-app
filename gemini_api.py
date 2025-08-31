import os
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np
from logger import logger
import time

# Load environment variables with explicit path
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(env_path)

# Get API key and configure Gemini if available
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
else:
    logger.error("GEMINI_API_KEY not found. Some features will be disabled.")


class MissingAPIKeyError(Exception):
    """Raised when GEMINI_API_KEY is not configured."""


def _ensure_api_key():
    if not API_KEY:
        raise MissingAPIKeyError("GEMINI_API_KEY not configured")

def get_embedding(text):
    """Generate embeddings using Gemini API."""
    try:
        _ensure_api_key()
        start = time.time()
        # Clean and prepare text
        text = text.strip()
        if not text:
            logger.warning("Empty text provided for embedding")
            return np.zeros(768)  # Default embedding size

        # Generate embedding
        result = genai.embed_content(
            model='models/embedding-001',
            content=text,
            task_type='retrieval_document'
        )

        # Handle different response formats
        if isinstance(result, dict) and 'embedding' in result:
            embedding = result['embedding']
        elif hasattr(result, 'embedding'):
            embedding = result.embedding
        else:
            logger.error("Unexpected embedding format: %s", type(result))
            return np.zeros(768)

        logger.info("Gemini embedding success (%.2fs, %d chars)", time.time() - start, len(text))
        return embedding

    except MissingAPIKeyError:
        logger.error("Embedding skipped: GEMINI_API_KEY not configured")
        return np.zeros(768)
    except Exception as e:
        logger.error("Embedding error: %s", str(e))
        return np.zeros(768)

def generate_fit_summary(job_desc, resume_text):
    """Generate a summary of how well a resume matches a job description."""
    prompt = f"""
You are helping match resumes to job descriptions.

Job Description:
{job_desc}

Resume:
{resume_text}

Explain briefly why this candidate is a good match for this job.
"""

    try:
        _ensure_api_key()
        start = time.time()
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        response = model.generate_content(prompt)
        summary = response.text.strip()
        logger.info("Gemini summary success (%.2fs)", time.time() - start)
        return summary
    except MissingAPIKeyError:
        logger.error("Summary generation skipped: GEMINI_API_KEY not configured")
        raise
    except Exception as e:
        logger.error("Summary generation failed: %s", str(e))
        return "_Could not generate summary._"
