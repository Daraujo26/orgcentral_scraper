import json

# Load JSON data from majors.json
input_file = 'majors.json'
output_file = 'majors.txt'

try:
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Extract titles and save to majors.txt
    with open(output_file, 'w') as file:
        for item in data:
            file.write(item["title"] + '\n')

    print(f"Titles successfully saved to {output_file}")

except FileNotFoundError:
    print(f"Error: {input_file} not found.")
except json.JSONDecodeError:
    print("Error: Failed to decode JSON. Please check the file format.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
