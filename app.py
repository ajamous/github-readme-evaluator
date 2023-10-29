# Import necessary modules
from flask import Flask, request, render_template
import requests
import textstat
import openai
import os

# Initialize Flask app
app = Flask(__name__)

# Initialize OpenAI API key from environment variables
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Function to fetch README content from a GitHub repository
def fetch_readme_contents(repo_url):
    # Construct the URL for the README file
    readme_url = f"https://raw.githubusercontent.com/{repo_url}/main/README.md"
    # Fetch the README file
    response = requests.get(readme_url)
    # Check if the request was successful
    if response.status_code != 200:
        return None
    return response.text

# Function to evaluate a README text
def evaluate_readme(readme_text):
    evaluation = {}
    # Define essential sections for README
    essential_sections = ["Getting Started", "Installation", "Usage", "Contribution"]
    section_results = {}
    # Check if essential sections are present
    for section in essential_sections:
        if section in readme_text:
            section_results[section] = f"The section '{section}' is present. Good job! ✅"
        else:
            section_results[section] = f"The section '{section}' is missing. Consider adding it to improve your README. ❌"
    evaluation["Essential Sections"] = section_results

    # Evaluate readability
    readability = textstat.flesch_reading_ease(readme_text)
    evaluation["Readability"] = f"The readability score is {readability}. Higher is better, aim for 60-70."

    # Evaluate length
    length = len(readme_text.split())
    evaluation["Length"] = f"The README has {length} words. Make sure it's not too short or too verbose."

    return evaluation

# Function to evaluate README text quality using NLP
def nlp_text_quality(readme_text):
    # Use OpenAI API to evaluate text quality
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Evaluate the quality of the following README text:\n{readme_text[:5000]}",
        max_tokens=1000
    )
    return response.choices[0].text.strip()

# Function to summarize README text
def text_summarization(readme_text):
    # Use OpenAI API to summarize text
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following README text:\n{readme_text[:5000]}",
        max_tokens=1000
    )
    return response.choices[0].text.strip()

# Function for topic modeling on README text
def topic_modeling(readme_text):
    # Use OpenAI API to identify main topics
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"What are the main topics covered in the following README text?\n{readme_text[:5000]}",
        max_tokens=1000
    )
    return response.choices[0].text.strip()

# Function to provide recommendations to improve README
def recommendation_engine(readme_text):
    # Use OpenAI API for improvement recommendations
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"How can the following README text be improved?\n{readme_text[:5000]}",
        max_tokens=1000
    )
    return response.choices[0].text.strip()

# Main route
@app.route("/", methods=["GET", "POST"])
def index():
    evaluation = {}
    # If the request method is POST
    if request.method == "POST":
        # Get the repository URL from the form
        repo_url = request.form.get("repo_url")
        # Fetch README content
        readme_text = fetch_readme_contents(repo_url)
        if readme_text:
            # Evaluate README
            evaluation = evaluate_readme(readme_text)
            evaluation["NLP Text Quality"] = nlp_text_quality(readme_text)
            evaluation["Text Summarization"] = text_summarization(readme_text)
            evaluation["Topic Modeling"] = topic_modeling(readme_text)
            evaluation["Recommendation Engine"] = recommendation_engine(readme_text)
        else:
            # If fetching README fails
            evaluation = {"error": "Could not fetch README. Ensure the repository and README exist."}

    return render_template("index.html", evaluation=evaluation)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
