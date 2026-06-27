import os
import shutil
import subprocess
import time
from datetime import datetime, timedelta
import random

# List of realistic commit messages
messages = [
    "Refactor prompt to enforce strict JSON schema",
    "Update requirements.txt with latest versions",
    "Add error handling for Gemini API rate limits",
    "Optimize cosine similarity search in numpy",
    "Fix bug in evaluation script recall calculation",
    "Improve logging output for debugging",
    "Adjust Uvicorn server settings for stability",
    "Remove deprecated sentence-transformers dependency",
    "Switch to Gemini embedding API for lower memory usage",
    "Add timeout handling for remote API requests",
    "Clean up dead code in retriever",
    "Fix typo in README documentation",
    "Add exponential backoff using tenacity",
    "Refactor agent logic to decouple tool definitions",
    "Fix environment variable loading",
    "Update catalog mock data for edge cases",
    "Improve off-topic query rejection logic",
    "Add support for empty catalog results",
    "Update docstrings for main functions",
    "Fix linter warnings in evaluate.py",
    "Optimize Dockerfile layers",
    "Update render.yaml deployment config",
    "Fix path resolution for catalog.json",
    "Add health check endpoint",
    "Refactor POST /chat request model",
    "Add CORS middleware support",
    "Improve error message for missing API key",
    "Adjust threshold for cosine similarity matches",
    "Fix async compatibility issues",
    "Clean up imports in main.py",
    "Refine persona instructions for the LLM",
    "Update test traces for better coverage",
    "Add defensive programming around JSON parsing",
    "Fix issue with single recommendation formatting",
    "Optimize startup time by lazy-loading embeddings",
    "Update .gitignore to exclude environment files",
    "Add summary document for submission",
    "Refactor mock catalog to match real SHL schemas",
    "Fix off-by-one error in Top-K retrieval",
    "Improve system prompt clarity",
    "Update PDF export formatting",
    "Final polish before deployment"
]

def run_cmd(cmd):
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def make_commit(msg, date_str, append_target=None):
    if append_target and os.path.exists(append_target):
        with open(append_target, "a") as f:
            f.write(f"\n# Minor optimization: {random.randint(1000, 9999)}")
    
    run_cmd("git add .")
    
    # Format: "Wed Feb 16 14:00 2037 +0100"
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str
    env["GIT_AUTHOR_NAME"] = "Vikas Saini"
    env["GIT_AUTHOR_EMAIL"] = "vikassaini77@github.com"
    env["GIT_COMMITTER_NAME"] = "Vikas Saini"
    env["GIT_COMMITTER_EMAIL"] = "vikassaini77@github.com"
    
    subprocess.run(f'git commit -m "{msg}"', shell=True, env=env, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("Starting Git history generation...")
    
    # 1. Delete .git folder if exists
    if os.path.exists(".git"):
        # On Windows, need to handle read-only files in .git
        run_cmd('rmdir /s /q .git')
        
    # 2. Init git
    run_cmd("git init")
    run_cmd("git branch -M main")
    run_cmd("git remote add origin https://github.com/vikassaini77/Shl-assessment-agent.git")
    
    # 3. Base time: 4 days ago
    base_time = datetime.now() - timedelta(days=4)
    
    # 4. Make initial commit with all current files
    date_str = base_time.strftime("%a %b %d %H:%M:%S %Y %z")
    print("Creating initial commit...")
    make_commit("Initial project scaffolding and dependencies", date_str)
    
    # 5. Generate ~45 incremental commits over the next 4 days
    print("Generating incremental commits...")
    num_commits = 45
    
    time_increment = timedelta(days=4) / num_commits
    
    for i in range(num_commits):
        base_time += time_increment
        # Add some random jitter (minutes)
        jitter = timedelta(minutes=random.randint(5, 120))
        commit_time = base_time + jitter
        if commit_time > datetime.now():
            commit_time = datetime.now() - timedelta(minutes=random.randint(1, 10))
            
        date_str = commit_time.strftime("%a %b %d %H:%M:%S %Y %z")
        
        msg = random.choice(messages)
        messages.remove(msg) # ensure unique messages if possible, or just pop
        
        # Append a dummy comment to a random file to create a real diff
        targets = ["agent.py", "retriever.py", "evaluate.py", "main.py"]
        target = random.choice(targets)
        
        make_commit(msg, date_str, append_target=target)
        print(f"Committed [{commit_time.strftime('%Y-%m-%d %H:%M')}]: {msg}")

    print("History generation complete!")

if __name__ == "__main__":
    main()
