from flask import Flask, request, render_template
import requests
import textstat

app = Flask(__name__)

def fetch_readme_contents(repo_url):
    readme_url = f"https://raw.githubusercontent.com/{repo_url}/main/README.md"
    response = requests.get(readme_url)
    if response.status_code != 200:
        return None
    return response.text

def evaluate_readme(readme_text):
    evaluation = {}

    essential_sections = ["Getting Started", "Installation", "Usage", "Contribution"]
    section_results = {}
    for section in essential_sections:
        if section in readme_text:
            section_results[section] = f"The section '{section}' is present. Good job!"
        else:
            section_results[section] = f"The section '{section}' is missing. Consider adding it to improve your README."

    evaluation["Essential Sections"] = section_results
    readability = textstat.flesch_reading_ease(readme_text)
    evaluation["Readability"] = f"The readability score is {readability}. Higher is better, aim for 60-70."

    length = len(readme_text.split())
    evaluation["Length"] = f"The README has {length} words. Make sure it's not too short or too verbose."

    return evaluation

@app.route("/", methods=["GET", "POST"])
def index():
    evaluation = {}
    if request.method == "POST":
        repo_url = request.form.get("repo_url")
        readme_text = fetch_readme_contents(repo_url)
        if readme_text:
            evaluation = evaluate_readme(readme_text)
        else:
            evaluation = {"error": "Could not fetch README. Ensure the repository and README exist."}
    return render_template("index.html", evaluation=evaluation)

if __name__ == "__main__":
    app.run(debug=True)
