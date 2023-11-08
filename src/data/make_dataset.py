import numpy as np
import pandas as pd

import json
import matplotlib.pyplot as plt
import seaborn as sns
from PyDictionary import PyDictionary


# Load the JSON data from the file
file_path = '/Users/karan/Data_Science_Challenge_Es_Profiler/data/raw/enterprise-attack-14.0.json'
with open(file_path, 'r') as file:
    data = json.load(file)

# Display the type and top-level keys of the JSON data
data_type = type(data)
top_level_keys = data.keys() if isinstance(data, dict) else 'Not a dict'

data_type, top_level_keys, len(data) if isinstance(data, list) else 'N/A'

# Inspect the first few elements in the 'objects' array to understand their structure
objects_preview = data['objects'][:5]  # Taking a slice of the first 5 objects

# Checking the structure of the objects
object_types = [obj.get('type', 'No type key') for obj in objects_preview]
objects_preview, object_types

# Let's look at the types of all objects to identify those that represent adversaries and relationships
object_types = set(obj.get('type', 'No type key') for obj in data['objects'])

# Display all unique types
object_types

# Extract and inspect some 'relationship' objects to understand their structure
relationship_objects = [obj for obj in data['objects'] if obj['type'] == 'relationship'][:5]  # Get the first 5 for inspection

relationship_objects


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

# Step 5 (revised): Compile techniques with adversaries using them for all relationships
# Reset the mapping to empty adversaries for a fresh start
techniques_to_adversaries = {tech['id']: {'technique': tech, 'adversaries': []} for tech in techniques}

# Iterate through all relationship objects to fill the mapping
for relationship in data['objects']:
    if relationship['type'] == 'relationship' and relationship['relationship_type'] == 'uses':
        source_id = relationship['source_ref']
        target_id = relationship['target_ref']
        # Check if the source is an adversary and the target is a technique
        if source_id in adversary_details and target_id in technique_details:
            techniques_to_adversaries[target_id]['adversaries'].append(adversary_details[source_id])

# Convert the final mapping to a list structure as required
final_data_structure = [{
    'technique': tech['technique']['name'],
    'technique_id': tech_id,
    'adversaries': [{'name': adv['name'], 'id': adv['id']} for adv in tech['adversaries']]
} for tech_id, tech in techniques_to_adversaries.items() if tech['adversaries']]  # Include only techniques with adversaries

# Save the transformed data to a new JSON file
transformed_file_path = '/Users/karan/Data_Science_Challenge_Es_Profiler/data/processed.json'
with open(transformed_file_path, 'w') as outfile:
    json.dump(final_data_structure, outfile, indent=2)

transformed_file_path, len(final_data_structure)

# Load the new JSON file that was uploaded
new_json_file_path = '/Users/karan/Data_Science_Challenge_Es_Profiler/data/processed.json'

with open(new_json_file_path, 'r') as file:
    processed_data = json.load(file)

# Count the number of adversaries for each technique for the visualization
technique_adversary_count = {tech['technique']['id']: len(tech['adversaries']) for tech in processed_data}

# Sort the techniques by popularity (number of adversaries using it)
sorted_technique_adversary_count = dict(sorted(technique_adversary_count.items(), key=lambda item: item[1], reverse=True))

# Take the top 20 most popular techniques
top_techniques = list(sorted_technique_adversary_count.keys())[:20]
top_counts = [sorted_technique_adversary_count[tech] for tech in top_techniques]

# Create a list of techniques with the count of adversaries using each technique
technique_popularity = [(tech['name'], len(tech['adversaries'])) for tech in final_techniques_list]

# Sort the list by the count of adversaries in descending order to show the most popular techniques first
technique_popularity_sorted = sorted(technique_popularity, key=lambda x: x[1], reverse=True)

# Select the top N techniques to display for clarity
top_techniques = technique_popularity_sorted[:20]

# Unzip the list of tuples into two lists for plotting
technique_names, adversary_counts = zip(*top_techniques)

# Create a bar chart
plt.figure(figsize=(15, 10))
plt.barh(technique_names, adversary_counts, color='skyblue')
plt.xlabel('Number of Adversaries Using the Technique')
plt.title('Top 20 Most Popular Techniques by Number of Adversaries')
plt.gca().invert_yaxis()  # Invert the y-axis to show the highest value at the top
plt.tight_layout()  # Adjust the plot to ensure everything fits without overlapping

# Show the plot
plt.show()


# Create a dataframe from the processed data for the heatmap
techniques = list({tech['technique']['id'] for tech in processed_data})
adversaries = list({adv['name'] for tech in processed_data for adv in tech['adversaries']})
heatmap_data = pd.DataFrame(0, index=adversaries, columns=techniques)

# Populate the dataframe with frequency of techniques used by each adversary
for tech in processed_data:
    for adv in tech['adversaries']:
        heatmap_data.at[adv['name'], tech['technique']['id']] += 1

# Since the dataset might be large, we'll create a heatmap for the top 20 adversaries only
top_adversaries_heatmap = heatmap_data.loc[top_adversaries_reloaded]

# Create the heatmap
plt.figure(figsize=(20, 15))
sns.heatmap(top_adversaries_heatmap, cmap='viridis', linewidths=.5, annot=True, fmt='d')
plt.title('Heatmap of Techniques vs. Top 20 Adversaries', fontsize=20)
plt.xlabel('Techniques', fontsize=16)
plt.ylabel('Adversaries', fontsize=16)

# Rotate the x labels for better visibility
plt.xticks(rotation=45, ha='right')

# Save the heatmap
heatmap_file_path = '/mnt/data/heatmap_techniques_adversaries.png'
plt.savefig(heatmap_file_path, bbox_inches='tight')

plt.show()

heatmap_file_path


# Since the number of techniques is large, we'll focus on the top N for the pie chart for clarity
top_n_for_pie_chart = 10
top_techniques_for_pie = top_popularity[:top_n_for_pie_chart]

# Extracting the technique names and the number of adversaries for the top N techniques
technique_names_for_pie, adversary_counts_for_pie = zip(*top_techniques_for_pie)

# Create a pie chart
plt.figure(figsize=(10, 10))
plt.pie(adversary_counts_for_pie, labels=technique_names_for_pie, autopct='%1.1f%%', startangle=140)
plt.title('Distribution of the Top {} Most Popular Techniques'.format(top_n_for_pie_chart))

# Save the figure to a file
pie_chart_filename = '/mnt/data/technique_popularity_pie_chart.png'
plt.savefig(pie_chart_filename)

# Show the plot
plt.show()

# Return the path to the saved pie chart image
pie_chart_filename


# Correcting the network graph generation

# Create a new graph
G_corrected = nx.Graph()

# Add nodes for top techniques and all adversaries associated with these techniques
for tech in top_techniques_for_network:
    technique_name = tech[0]
    # Add technique node with the count of adversaries as the size attribute
    G_corrected.add_node(technique_name, type='technique', size=tech[1])

    # Get the adversaries for each technique from our final_techniques_list
    adversaries_for_tech = [adv['adversaries'] for adv in final_techniques_list if adv['name'] == technique_name][0]
    for adversary in adversaries_for_tech:
        # Add adversary node if it's not already present
        if adversary not in G_corrected:
            G_corrected.add_node(adversary, type='adversary')
        # Add an edge between the adversary and the technique
        G_corrected.add_edge(adversary, technique_name)

# Define node colors based on type
colors = ['red' if G_corrected.nodes[node]['type'] == 'technique' else 'blue' for node in G_corrected]
# Define node sizes based on count of adversaries for techniques, fixed size for adversaries
sizes = [G_corrected.nodes[node]['size']*50 if 'size' in G_corrected.nodes[node] else 100 for node in G_corrected]

# Generate positions for each node using the spring layout
pos = nx.spring_layout(G_corrected, k=0.1, iterations=20)

# Draw the network graph
plt.figure(figsize=(14, 10))
nx.draw(G_corrected, pos, with_labels=True, node_color=colors, node_size=sizes, font_size=8, edge_color='gray', linewidths=0.5)
plt.title('Network Graph of Adversaries and Techniques')

# Save the figure to a file
network_graph_filename_corrected = '/mnt/data/technique_adversary_network_graph_corrected.png'
plt.savefig(network_graph_filename_corrected, format='PNG', dpi=300)

# Show the plot
plt.show()

# Return the path to the saved network graph image
network_graph_filename_corrected
