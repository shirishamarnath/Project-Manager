import requests
import os
from dotenv import load_dotenv
from markdown2 import markdown
import subprocess
from flask import url_for  # Import url_for to generate relative paths


# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("API_KEY")

# Set the API endpoint for Gemini
API_ENDPOINT = f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}'

# Initialize headers including Content-Type
headers = {
    'Content-Type': 'application/json',
}

def process_text_with_gemini(extracted_text):
    # Define the prompts
    project_plan_prompt = "Generate a complete project plan for the following SRS document, let the plan include different modules, technology stack for each module, time to spend in each module, total time, total number of employees in each module, etc. Don't give anything in table format."
    class_diagram_prompt = "Generate Python code(Don't give comments or explanations) that creates a class diagram based on the following SRS document. The code should use graphviz. The code should generate a png image and save(WRITE CODE FOR THIS) it under the following path /Users/s.sanjithsuryasrinivasan/Desktop/CAPSTONE_mybranch/AI-PROJECT-MANAGER/backend/static/class_diagram.png. Don't create the folder. Just put the png image in that location. SAVE THE IMAGE AS class_diagram.png like dot.render('/Users/s.sanjithsuryasrinivasan/Desktop/CAPSTONE_mybranch/AI-PROJECT-MANAGER/backend/static/class_diagram', format='png'). Make the code do all these. DIRECTLY GIVE THE CODE. DONT GIVE ANY OTHER STATEMENTS."
    sprint_wise_prompt = "Generate multiple sprints, and tell in detail what to be done in each sprints, and tell the exact number of people required for each sprints and cost(approximate cost) for each sprint, from the given SRS document. Focus only on sprints and nothing else. Also give the risks at each sprints and how to avoid them."

    # Step 1: Generate the project plan
    project_plan_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": extracted_text + "\n" + project_plan_prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=project_plan_data)
    
    if response.status_code == 200:
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            formatted_content = markdown(content)
        else:
            formatted_content = "No content generated for project plan."
    else:
        print(f"Failed to get response for project plan, status code: {response.status_code}")
        print(response.text)
        return None

    # Step 2: Generate the Python code for class diagram
    class_diagram_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": extracted_text + "\n" + class_diagram_prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=class_diagram_data)

    if response.status_code == 200:
        result = response.json()

        if 'candidates' in result and result['candidates']:
            class_diagram_code = result['candidates'][0]['content']['parts'][0]['text']
            class_diagram_code = class_diagram_code[9:len(class_diagram_code) - 4]

            print(class_diagram_code)
            # Execute the generated class diagram code
            execute_class_diagram_code(class_diagram_code)

            # Append HTML to display the class diagram image if generated
            # Use url_for to reference the static file location
            formatted_content += f'<h2>System Architecture Diagram</h2><div><img src="{url_for("static", filename="class_diagram.png")}" alt="Class Diagram" style = "max-width:100%; height:auto;"></div>'
        else:
            formatted_content += "<p>No content generated for class diagram code.</p>"
    else:
        print(f"Failed to get response for class diagram, status code: {response.status_code}")
        print(response.text)
        return None

    project_plan_data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": extracted_text + "\n" + sprint_wise_prompt
                    }
                ]
            }
        ]
    }

    response = requests.post(API_ENDPOINT, headers=headers, json=project_plan_data)
    
    if response.status_code == 200:
        result = response.json()
        
        if 'candidates' in result and result['candidates']:
            content = result['candidates'][0]['content']['parts'][0]['text']
            formatted_content += markdown(content)
        else:
            formatted_content = "No content generated for project plan."
    else:
        print(f"Failed to get response for project plan, status code: {response.status_code}")
        
        return None

    return formatted_content

def execute_class_diagram_code(code):
    # Write the generated Python code to a file
    with open("class_diagram.py", "w") as file:
        file.write(code)

    # Execute the Python script to generate the class diagram image
    result = subprocess.run(["python", "class_diagram.py"], capture_output=True, text=True)
    print("Execution result:", result.stdout)
    print("Execution errors:", result.stderr)

    # Check if the output image exists in the static folder
    output_path = "/Users/s.sanjithsuryasrinivasan/Desktop/CAPSTONE_mybranch/AI-PROJECT-MANAGER/backend/static/class_diagram.png"
    if os.path.exists(output_path):
        print("Class diagram image created successfully.")
        return True
    else:
        print("Failed to create class diagram image.")
        return False
