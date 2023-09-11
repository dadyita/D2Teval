import json
import datasets

def generate_table_text(title, column, table_content, question):
    table_text = "Title: " + title + "<br><br>"
    table_text += "Table Content:<br>"
    table_text += " | ".join(column) + "<br>"
    for row in table_content:
        table_text += " | ".join(row) + "<br>"
    table_text += "<br>"
    table_text += "Question: " + question + "<br><br>"
    return table_text


data = json.load(open("data/fetaqa/predictions.json"))
output_data = {}

examples = datasets.load_dataset("DongfuTingle/FeTaQA", split="test")
orig_data = {}
for example in examples:
    orig_data[example["feta_id"]] = example

for i, (example_id, pred_text) in enumerate(data.items()):
    example = {}

    orig_example = orig_data[int(example_id)]
    example["table_column_names"] = orig_example["table_array"][0]
    example["table_content_values"] = orig_example["table_array"][1:]
    example["query"] = orig_example["question"]
    example["title"] = f"{orig_example['table_page_title']} - {orig_example['table_section_title']}"

    table_text = generate_table_text(example["title"], example["table_column_names"], example["table_content_values"], example["query"])
    example["table_text"] = table_text
    example["text"] = pred_text

    output_data[i] = example

json.dump(output_data, open("data/fetaqa/visualization.json", "w"), indent=4)

    

