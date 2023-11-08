import json

# Load the JSON data from the file
file_path = '/Users/karan/Data_Science_Challenge_Es_Profiler/data/raw/enterprise-attack-14.0.json'
with open(file_path, 'r') as file:
    data = json.load(file)


# Step 1: Identify all techniques
techniques = [obj for obj in data['objects'] if obj['type'] == 'attack-pattern']

# Step 2: Map each technique to its details (we will use the 'id' to map relationships later)
technique_details = {tech['id']: tech for tech in techniques}

# Step 3: Identify all adversaries (intrusion-sets)
adversaries = [obj for obj in data['objects'] if obj['type'] == 'intrusion-set']

# Step 4: Map each adversary to its details
adversary_details = {adv['id']: adv for adv in adversaries}

# Step 5: Compile techniques with adversaries using them
# Initialize a dictionary to hold the mapping of techniques to the adversaries that use them
techniques_to_adversaries = {tech['id']: {'technique': tech, 'adversaries': []} for tech in techniques}

# Iterate through the relationship objects to fill the mapping
for relationship in relationship_objects:
    if relationship['relationship_type'] == 'uses' and relationship['target_ref'] in technique_details:
        # Append the adversary details to the technique's list of adversaries
        source_id = relationship['source_ref']
        target_id = relationship['target_ref']
        if source_id in adversary_details:
            techniques_to_adversaries[target_id]['adversaries'].append(adversary_details[source_id])

# Now we have a dictionary of techniques to adversaries, but we want a list of techniques each with a sub-list of adversaries
final_data_structure = list(techniques_to_adversaries.values())

# For the purposes of this example, we will display only one entry to ensure it looks correct
final_data_structure[0] if final_data_structure else "No Data Found"
