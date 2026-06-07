import os
import subprocess
from typing import Any
from google import genai
from google.genai import types
from dotenv import load_dotenv

# 1. Load credentials from your .env file
load_dotenv()

# Check that critical keys are present before starting
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY is missing from your environment configuration.")
if not os.getenv("GITHUB_TOKEN"):
    raise ValueError("GITHUB_TOKEN is missing from your environment configuration.")

# ==========================================
# TOOL 1: Execute Local Workspace Shell Setup
# ==========================================
def setup_local_workspace_and_git(project_id: str) -> str:
    """Scaffolds the dbt, dataproc, and bigquery directory structure locally, 
    creates a secure .gitignore file, and initializes a local Git repo.
    
    Args:
        project_id: The active GCP Project ID (e.g., 'waybackhome-8nw4qqaw543g6sm9h5')
    """
    try:
        print(f"\n[Tool Executing]: Scaffolding folders for project {project_id}...")
        
        # Navigate to home workspace to create the framework root cleanly
        os.chdir(os.path.expanduser("~"))
        workspace_dir = os.path.expanduser("~/waybackhome-platform")
        
        # Create directories
        dirs = [
            "dbt_project/models", "dbt_project/macros", "dbt_project/seeds",
            "dataproc/jobs", "dataproc/scripts",
            "bigquery/schemas", "bigquery/procedures"
        ]
        for d in dirs:
            os.makedirs(os.path.join(workspace_dir, d), exist_ok=True)
            
        # Create .gitignore in the root workspace
        gitignore_content = "*.json\ncredentials/\n.dbt/profiles.yml\n__pycache__/\n*.pyc\n.venv/\n/target/\n/logs/\n"
        with open(os.path.join(workspace_dir, ".gitignore"), "w") as f:
            f.write(gitignore_content)
            
        # Create descriptive README
        with open(os.path.join(workspace_dir, "README.md"), "w") as f:
            f.write(f"# Data Platform Workspace\nManaged GCP pipeline files for project: {project_id}\n")

        # Initialize Git repository inside the target folder
        os.chdir(workspace_dir)
        subprocess.run(["git", "init", "-b", "main"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "config", "user.email", "automation-agent@google.com"], check=False)
        subprocess.run(["git", "config", "user.name", "ADK Automation Agent"], check=False)
        subprocess.run(["git", "commit", "-m", "feat: scaffold workspace pipelines via automation agent"], check=True)
        
        return "SUCCESS: Directories scaffolded and local main branch committed successfully at ~/waybackhome-platform."
    except Exception as e:
        return f"ERROR in setup_local_workspace_and_git: {str(e)}"

# ==========================================
# TOOL 2: Configure Remotes & Sync Branches
# ==========================================
def sync_pipeline_branches_to_github(repo_url: str) -> str:
    """Links the local repository to GitHub using your authenticated token, 
    creates development, release, and main branches, and pushes them upstream.
    
    Args:
        repo_url: The standard GitHub repository URL.
    """
    try:
        github_token = os.getenv("GITHUB_TOKEN")
        print(f"\n[Tool Executing]: Connecting to repository {repo_url}...")
        
        # Format URL with security token for automatic HTTPS pushes
        authenticated_url = repo_url.replace("https://", f"https://{github_token}@")
        
        # Switch to the target repository directory
        workspace_dir = os.path.expanduser("~/waybackhome-platform")
        os.chdir(workspace_dir)
        
        # Configure or update Git remote URL
        remote_check = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True)
        if remote_check.returncode == 0:
            subprocess.run(["git", "remote", "set-url", "origin", authenticated_url], check=True)
        else:
            subprocess.run(["git", "remote", "add", "origin", authenticated_url], check=True)
            
        # Force-push Main branch upstream
        print("-> Pushing 'main' branch...")
        subprocess.run(["git", "push", "-u", "origin", "main", "--force"], check=True)
        
        # Create and push Release branch upstream
        print("-> Creating and pushing 'release' branch...")
        subprocess.run(["git", "checkout", "-b", "release"], check=False)
        subprocess.run(["git", "push", "-u", "origin", "release", "--force"], check=True)
        
        # Create and push Development branch upstream
        print("-> Creating and pushing 'development' branch...")
        subprocess.run(["git", "checkout", "-b", "development"], check=False)
        subprocess.run(["git", "push", "-u", "origin", "development", "--force"], check=True)
        
        return "SUCCESS: main, release, and development branches have been pushed to GitHub."
    except Exception as e:
        return f"ERROR in sync_pipeline_branches_to_github: {str(e)}"

# ==========================================
# EXECUTION LIFECYCLE INTERFACE
# ==========================================
if __name__ == "__main__":
    print("Initializing Gemini Orchestration Engine...")
    
    # Initialize the official Google GenAI Client
    client = genai.Client()
    
    user_prompt = (
        "Please scaffold my workspace folders for GCP project 'waybackhome-8nw4qqaw543g6sm9h5', "
        "initialize my git configuration, and sync my main, release, and development branches "
        "to my repo: https://github.com/jakkampudiram-del/janaki_repo."
    )
    
    # Bundle our python tools together so Gemini can read their docstrings and execute them
    available_tools = {
        "setup_local_workspace_and_git": setup_local_workspace_and_git,
        "sync_pipeline_branches_to_github": sync_pipeline_branches_to_github
    }
    
    print("Sending automation instructions to agent...")
    
    # Call the model with tool execution permissions enabled
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction="You are a platform engineering agent. Use your tools sequentially to complete the user's workspace setup.",
            tools=[setup_local_workspace_and_git, sync_pipeline_branches_to_github],
            temperature=0.0
        )
    )
    
    # Check if the model decided to execute our functions
    if response.function_calls:
        for function_call in response.function_calls:
            name = function_call.name
            args = function_call.args
            
            if name in available_tools:
                # Dynamically execute our helper functions using parameters chosen by Gemini
                tool_result = available_tools[name](**args)
                print(tool_result)
            else:
                print(f"Unknown function execution requested: {name}")
                
        # Follow up with Gemini to close the loop on completion status
        print("\nFinalizing repository status feedback...")
        final_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part.from_text(text=user_prompt)]),
                response.candidates[0].content,
                types.Content(role="user", parts=[
                    types.Part.from_function_response(
                        name=name,
                        response={"result": tool_result}
                    )
                ])
            ]
        )
        print("\n[Agent Final Output]:")
        print(final_response.text)
    else:
        print("\n[Agent Output]:")
        print(response.text)