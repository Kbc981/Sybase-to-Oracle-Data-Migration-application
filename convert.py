import google.generativeai as genai
import json
import os

# Configure the API key - it's best to set this as an environment variable
# For example: export GOOGLE_API_KEY="your_api_key"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# --- Configuration ---
# In a real app, get these from a config file or arguments
SYBASE_DDL_FILE = "C:\\Users\\thisi\\OneDrive\\Desktop\\Sybase to oracle\\sybase sample procedure.sql"
CONVERSION_RULES_FILE = "C:\\Users\\thisi\\OneDrive\\Desktop\\Sybase to oracle\\sybase_to_oracle_data.json"
MODEL_NAME = "gemini-1.5-flash-latest" # Use a powerful and cost-effective model

def load_file_content(filepath):
    """Loads content from a file."""
    with open(filepath, 'r',encoding='utf-8') as f:
        return f.read()

def generate_conversion_prompt(sybase_ddl, conversion_rules_json, object_type="PROCEDURE"):
    """Constructs a detailed prompt for the Gemini model."""
    
    prompt = f"""
    You are an expert database migration assistant specializing in converting Sybase T-SQL to Oracle PL/SQL.
    Your task is to convert the following Sybase {object_type} DDL into the equivalent Oracle PL/SQL DDL.

    **CRITICAL CONVERSION RULES:**
    You must adhere to the following conversion rules, data type mappings, and function replacements provided in this JSON format:
    ```json
    {conversion_rules_json}
    ```

    **INPUT SYBASE DDL:**
    ```sql
    {sybase_ddl}
    ```

    **INSTRUCTIONS:**
    1.  Carefully analyze the input Sybase DDL.
    2.  Apply the rules from the JSON to perform the conversion.
    3.  Pay close attention to data types, identity columns, constraints, built-in functions (like GETDATE()), and syntax for triggers or stored procedures.
    4.  Provide ONLY the fully converted, valid Oracle PL/SQL code as the output. Do not add any explanations or apologies.
    
    **OUTPUT ORACLE PL/SQL DDL:**
    """
    return prompt

def main():
    """Main function to run the conversion."""
    try:
        # 1. Load data
        sybase_code = load_file_content(SYBASE_DDL_FILE)
        conversion_rules = load_file_content(CONVERSION_RULES_FILE)

        # 2. Construct the prompt
        # You can make object_type dynamic (e.g., 'PROCEDURE', 'TRIGGER')
        prompt = generate_conversion_prompt(sybase_code, conversion_rules, object_type="PROCEDURE")
        
        # 3. Call the Gemini API
        print("Sending request to Gemini API...")
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        
        # 4. Print the result
        print("\n--- Converted Oracle DDL ---")
        print(response.text)

    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
