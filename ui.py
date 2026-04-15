import gradio as gr
from analyzer import analyze_resume

def run_analysis(resume, job):
    result = analyze_resume(resume, job)

    matched = [w.replace("_", " ") for w in result["matched"]]
    missing = [w.replace("_", " ") for w in result["missing"]]

    output = f"Match Score: {result['score']}%\n\n"

    output += "Matched Skills:\n"
    for m in matched:
        output += f"✔ {m}\n"

    output += "\nMissing Skills:\n"
    for m in missing:
        output += f"❗ {m}\n"

    return output


app = gr.Interface(
    fn=run_analysis,
    inputs=[
        gr.Textbox(lines=6, label="Paste Resume"),
        gr.Textbox(lines=6, label="Paste Job Description")
    ],
    outputs="text",
    title="AI Resume Analyzer",
    description="Check how well your resume matches a job description"
)

app.launch()