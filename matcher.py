from sklearn.metrics.pairwise import cosine_similarity
from gemini_api import get_embedding
from concurrent.futures import ThreadPoolExecutor
from logger import logger
import time

def rank_resumes(job_desc, resumes, names, file_bytes, filenames):
    logger.info("Starting job embedding")
    start = time.time()
    job_vec = get_embedding(job_desc)
    logger.info("Job embedding done in %.2fs", time.time() - start)

    logger.info("Embedding %d resumes...", len(resumes))
    start = time.time()
    
    with ThreadPoolExecutor() as executor:
        resume_vecs = list(executor.map(get_embedding, resumes))
    logger.info("Resume embeddings done in %.2fs", time.time() - start)

    logger.info("Calculating similarity...")
    scores = cosine_similarity([job_vec], resume_vecs)[0]
    sorted_indices = scores.argsort()[::-1][:10]

    results = []
    for i in sorted_indices:
        results.append({
            "name": names[i],
            "score": scores[i],
            "resume_text": resumes[i],
            "file_bytes": file_bytes[i],
            "file_name": filenames[i]
        })

    logger.info("Top 10 candidates processed (no summaries yet).")
    return results
