# Dhvanii Chheda - OIM3641

This repository is where I'll be posting all of my projects, exercises, and assignments for **OIM3641** throughout the semester. As the class progresses, I'll keep adding new folders and files here, so think of this as a running portfolio of everything I build and learn along the way.

## About Me

Hi! I'm Dhvanii, a senior at **Babson College** majoring in **Business Analytics**. I'm passionate about using data to solve real business problems, and I'm always looking for ways to combine analytical thinking with hands-on technical skills. OIM3641 is actually my first real exposure to working with AI tools, large language models, and retrieval-based applications like the ones in this repo — so this class has been a great introduction to a space I'm excited to keep exploring.

## Skills & Tools

**Languages**

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=for-the-badge&logo=postgresql&logoColor=white)

**Libraries & Frameworks**

![LlamaIndex](https://img.shields.io/badge/LlamaIndex-000000?style=for-the-badge)
![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

**Tools**

![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white)

## Directory Structure

As the semester goes on, I'll organize new assignments into their own folders by class module/topic. Right now the repo looks like this:

```
oim3641/
├── 01-llm-call.py                        # Basic script for making an LLM API call
├── 02-python_concepts.ipynb              # Notebook covering core Python concepts
├── 03-demo_create_llamaindex.py          # Script to build a LlamaIndex from source docs
├── 03-demo_llama_retrieval.py            # Script demoing retrieval with LlamaIndex
├── 03-demo_llama_gemini_retrieval.py     # Retrieval demo using Google Gemini as the LLM
├── .gitignore                            # Excludes .env, venv, caches, checkpoints, etc.
├── .env                                  # Local API keys (not tracked in git)
└── README.md
```

Going forward, each new project/assignment will get its own numbered folder (e.g. `04-project-name/`) containing its code, any data it needs, and a short note on what it does.

## Install Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/dhvaniichheda/oim3641.git
   cd oim3641
   ```

2. **Set up a virtual environment** (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install python-dotenv google-genai llama-index llama-cloud-services
   ```

4. **Add your API keys**
   Create a `.env` file in the root directory with your own keys, for example:
   ```
   GEMINI_API_KEY=your_key_here
   LLAMA_CLOUD_API_KEY=your_key_here
   ORGANIZATION_ID=your_org_id_here
   ```

5. **Run a script**
   ```bash
   python 01-llm-call.py
   ```
   Or open the notebook:
   ```bash
   jupyter notebook 02-python_concepts.ipynb
   ```

## Contact / Connect

- **LinkedIn:** [linkedin.com/in/dhvanii-chheda005](https://www.linkedin.com/in/dhvanii-chheda005)

Feel free to reach out if you'd like to connect or chat about any of the projects here!
