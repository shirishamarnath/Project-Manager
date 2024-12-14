import unittest

def simulate_llm_prompt_response(prompt):

    if "project plan" in prompt.lower():
        return "Mock Project Plan Response"
    elif "class diagram" in prompt.lower():
        return "Mock Class Diagram Code"
    else:
        return "Unknown Prompt"

class TestLLMPrompts(unittest.TestCase):
    def test_project_plan_prompt(self):
        # Simulating a prompt for generating a project plan
        prompt = "Generate a complete project plan for the following SRS document."
        response = simulate_llm_prompt_response(prompt)
        self.assertEqual(response, "Mock Project Plan Response")
        print("Test Case Success: Project Plan Prompt")

    def test_class_diagram_prompt(self):
        # Simulating a prompt for generating class diagram code
        prompt = "Generate Python code that creates a class diagram."
        response = simulate_llm_prompt_response(prompt)
        self.assertEqual(response, "Mock Class Diagram Code")
        print("Test Case Success: Class Diagram Prompt")

    def test_invalid_prompt(self):
        # Simulating an invalid or unknown prompt
        prompt = "This is an invalid prompt."
        response = simulate_llm_prompt_response(prompt)
        self.assertEqual(response, "Unknown Prompt")
        print("Test Case Success: Invalid Prompt")

if __name__ == "__main__":
    unittest.main()
