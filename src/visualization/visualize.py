# Load the new JSON file that was uploaded
new_json_file_path = '/Users/karan/Data_Science_Challenge_Es_Profiler/data/processed.json'

with open(new_json_file_path, 'r') as file:
    processed_data = json.load(file)

# Count the number of adversaries for each technique for the visualization
technique_adversary_count = {tech['technique']: len(tech['adversaries']) for tech in processed_data}

# Sort the techniques by popularity (number of adversaries using it)
sorted_technique_adversary_count = dict(sorted(technique_adversary_count.items(), key=lambda item: item[1], reverse=True))

# Take the top 20 most popular techniques
top_techniques = list(sorted_technique_adversary_count.keys())[:20]
top_counts = [sorted_technique_adversary_count[tech] for tech in top_techniques]

# Create the bar chart
plt.figure(figsize=(12, 9))
plt.barh(top_techniques, top_counts, color='skyblue')
plt.xlabel('Number of Adversaries Using the Technique')
plt.ylabel('Techniques')
plt.title('Top 20 Most Popular Techniques by Number of Adversaries')
plt.gca().invert_yaxis()  # To display the highest value at the top
plt.tight_layout()

# Save the figure
chart_file_path_technique_popularity = '/mnt/data/technique_popularity_chart.png'
plt.savefig(chart_file_path_technique_popularity)

plt.show()

chart_file_path_technique_popularity

