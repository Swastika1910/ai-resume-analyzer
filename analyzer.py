import nltk
from nltk.corpus import stopwords
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# Extra words to ignore (non-skill words)
extra_stopwords = {"looking", "candidate", "experience", "job", "role", "work", "skills"}

def clean_text(text):
    text = text.lower()

    # Keep important phrases together
    text = text.replace("machine learning", "machine_learning")
    text = text.replace("data analytics", "data_analytics")

    # Remove punctuation
    text = re.sub(r'[^\w\s]', ' ', text)

    words = text.split()
    cleaned_words = []

    for word in words:
        if word not in stop_words and word not in extra_stopwords:
            cleaned_words.append(word)

    return " ".join(cleaned_words)


def analyze_resume(resume_text, job_text):
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, job_text])

    # Better scoring (more intuitive)
    important_words = set(vectorizer.get_feature_names_out())

    resume_words = set(resume_text.split()) & important_words
    job_words = set(job_text.split()) & important_words

    matched_words = resume_words & job_words
    missing_words = job_words - resume_words

    # Skill-based score (much better than cosine)
    score = (len(matched_words) / len(job_words)) * 100 if job_words else 0

    return {
        "score": round(score, 2),
        "matched": matched_words,
        "missing": missing_words
    }


if __name__ == "__main__":
    resume = input("Enter resume:\n")
    job = input("\nEnter job description:\n")

    result = analyze_resume(resume, job)

    print("\n===== RESULT =====")
    print(f"Match Score: {result['score']}%")

    matched = [w.replace("_", " ") for w in result["matched"]]
    missing = [w.replace("_", " ") for w in result["missing"]]

    print("\nMatched Skills:")
    for m in matched:
        print(f"✔ {m}")

    print("\nMissing Skills:")
    for m in missing:
        print(f"❗ {m}")