
#python , #regex

This script:

1. Defines a parse_scenario function that extracts all required fields from each scenario using regular expressions.

2. Defines a create_markdown_table function that:

- Creates the markdown table header

- Formats each scenario's data into a table row

- Handles multiline content by replacing newlines with <br>

- Escapes pipe characters

- Removes bullet points and extra whitespace

1. The main function:

- Reads the input file

- Splits the content into individual scenarios

- Parses each scenario

- Creates the markdown table

- Writes the output to a new file

To use the script:

1. Save your input text in a file named k8s-500-prod-issues

2. Run the script

3. The output will be saved in k8s-500-prod-issues.md

The script handles:

- Multiline content

- Bullet points

- Special characters

- Proper markdown table formatting

- Consistent spacing and formatting



```
import re

def parse_scenario(text):
    # Extract title
    title_match = re.search(r'Scenario #\d+: (.*?)\n', text)
    title = title_match.group(1) if title_match else ""

    # Extract category
    category_match = re.search(r'Category: (.*?)\n', text)
    category = category_match.group(1) if category_match else ""

    # Extract environment
    env_match = re.search(r'Environment: (.*?)\n', text)
    environment = env_match.group(1) if env_match else ""

    # Extract what happened
    what_happened_match = re.search(r'What Happened: (.*?)(?=Diagnosis Steps:|$)', text, re.DOTALL)
    what_happened = what_happened_match.group(1).strip() if what_happened_match else ""

    # Extract diagnosis steps
    diagnosis_match = re.search(r'Diagnosis Steps:(.*?)(?=Root Cause:|$)', text, re.DOTALL)
    diagnosis = diagnosis_match.group(1).strip() if diagnosis_match else ""

    # Extract root cause
    root_cause_match = re.search(r'Root Cause: (.*?)(?=Fix/Workaround:|$)', text, re.DOTALL)
    root_cause = root_cause_match.group(1).strip() if root_cause_match else ""

    # Extract fix/workaround
    fix_match = re.search(r'Fix/Workaround:(.*?)(?=Lessons Learned:|$)', text, re.DOTALL)
    fix = fix_match.group(1).strip() if fix_match else ""

    # Extract lessons learned
    lessons_match = re.search(r'Lessons Learned: (.*?)(?=How to Avoid:|$)', text, re.DOTALL)
    lessons = lessons_match.group(1).strip() if lessons_match else ""

    # Extract how to avoid
    avoid_match = re.search(r'How to Avoid:(.*?)(?=📘|$)', text, re.DOTALL)
    how_to_avoid = avoid_match.group(1).strip() if avoid_match else ""

    return {
        'Title': title,
        'Category': category,
        'Environment': environment,
        'What Happened': what_happened,
        'Diagnosis Steps': diagnosis,
        'Root Cause': root_cause,
        'Fix/Workaround': fix,
        'Lessons Learned': lessons,
        'How to Avoid': how_to_avoid
    }

def create_markdown_table(scenarios):
    # Create header
    headers = ['Title', 'Category', 'Environment', 'What Happened', 'Diagnosis Steps', 
               'Root Cause', 'Fix/Workaround', 'Lessons Learned', 'How to Avoid']
    
    # Create markdown table header
    table = "| " + " | ".join(headers) + " |\n"
    table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    
    # Add rows
    for scenario in scenarios:
        row = []
        for header in headers:
            # Replace newlines with <br> and escape pipe characters
            value = scenario[header].replace('\n', '<br>').replace('|', '\\|')
            # Remove bullet points and extra whitespace
            value = re.sub(r'^\s*[•-]\s*', '', value, flags=re.MULTILINE)
            value = re.sub(r'\s+', ' ', value).strip()
            row.append(value)
        table += "| " + " | ".join(row) + " |\n"
    
    return table

def main():
    # Read the input file
    with open('k8s_issues.txt', 'r') as file:
        content = file.read()
    
    # Split content into scenarios
    scenarios_text = content.split('📘')
    scenarios_text = [s for s in scenarios_text if s.strip()]  # Remove empty strings
    
    # Parse each scenario
    scenarios = []
    for scenario_text in scenarios_text:
        scenario = parse_scenario(scenario_text)
        scenarios.append(scenario)
    
    # Create markdown table
    markdown_table = create_markdown_table(scenarios)
    
    # Write to output file
    with open('k8s-500-prod-issues.md', 'w') as file:
        file.write(markdown_table)

if __name__ == "__main__":
    main()
```