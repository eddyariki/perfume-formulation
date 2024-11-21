import csv
from collections import defaultdict
import matplotlib.pyplot as plt

def calculate_ingredients(csv_file, total_weight, perfume_concentration, output_file):
    perfume_weight = total_weight * perfume_concentration

    diluent_contribution = 0
    category_weights = defaultdict(float)
    ingredient_weights = defaultdict(list)
    total_concentration = 0

    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)

        for row in reader:
            ingredient = row['ingredient']
            category = row['category']
            pre_dilution = float(row['pre-dilution'])
            concentration = float(row['concentration'])

            total_concentration += concentration
            perfume_contribution = 0

            if pre_dilution == 1:
                weight_to_add = concentration * perfume_weight
                perfume_contribution = concentration * perfume_weight
            else:
                weight_to_add = concentration * perfume_weight * (1.0 / pre_dilution)
                diluent_contribution += weight_to_add - concentration * perfume_weight * (1.0 - pre_dilution)
                perfume_contribution = concentration * perfume_weight

            ingredient_weights[category].append((ingredient, pre_dilution, weight_to_add))
            category_weights[category] += perfume_contribution

    ethanol_weight = total_weight - perfume_weight - diluent_contribution

    markdown_output = "# Perfume Ingredients Breakdown\n"
    markdown_output += f"**Perfume weight**: {perfume_weight:.4f} g\n"
    markdown_output += f"**Total diluent contribution**: {diluent_contribution:.4f} g\n"
    markdown_output += f"**Ethanol weight**: {ethanol_weight:.4f} g\n"
    markdown_output += f"**Total Concentration**: {total_concentration*100:.2f}%\n\n"

    markdown_output += "## Ingredients by Category\n"

    categories = list(category_weights.keys())
    percentages = [(category_weights[cat] / perfume_weight) * 100 for cat in categories]

    plt.figure(figsize=(10, 6))
    plt.bar(categories, percentages, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Percentage of Perfume Weight (%)')
    plt.title('Category Contributions to Perfume Weight')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    chart_filename = output_file.replace('.md', '.png')
    plt.savefig(chart_filename)
    plt.close()

    for category, ingredients in ingredient_weights.items():
        markdown_output += f"### {category}\n"
        markdown_output += "| **Ingredient** | **Pre-dilution (%)** | **Weight to Add (g)** |\n"
        markdown_output += "|----------------|----------------------|-----------------------|\n"
        for ingredient, pre_dilution, weight_to_add in ingredients:
            markdown_output += f"| {ingredient} | {pre_dilution*100:.2f} | {weight_to_add:.4f} |\n"
        category_percentage = (category_weights[category] / perfume_weight) * 100
        markdown_output += f"**Category Total**: {category_weights[category]:.4f} g ({category_percentage:.2f}%)\n\n"

    markdown_output += f"## Category Contributions Chart\n"
    markdown_output += f"![Category Contributions]({chart_filename})\n"

    with open(output_file, 'w') as file:
        file.write(markdown_output)

    print(f"\nMarkdown output saved to {output_file}")
    print(f"Chart saved to {chart_filename}")

if __name__ == "__main__":
    total_weight = float(input("Enter total weight (g): "))
    perfume_concentration = float(input("Enter perfume concentration (0-1): "))
    output_file = input("Enter the output filename (e.g., output.md): ")
    csv_file = input("Enter the CSV file name (e.g., ingredients.csv): ")
    calculate_ingredients(csv_file, total_weight, perfume_concentration, output_file)
