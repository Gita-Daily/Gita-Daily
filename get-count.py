import json

def count_keys_in_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        
        # Ensure that the parsed data is a dictionary
        if not isinstance(data, dict):
            raise ValueError("The provided JSON file does not contain a dictionary at the top level.")
        
        return len(data.keys())

# Main execution
if __name__ == "__main__":
    try:
        num_keys = count_keys_in_file("data.json")
        print(f"Number of keys in the file: {num_keys}")
    except Exception as e:
        print(f"An error occurred: {e}")

