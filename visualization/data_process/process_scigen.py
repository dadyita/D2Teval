import json

def generate_table_text(column, table_content, caption):
    table_text = "Table Content:<br>"
    table_text += " | ".join(column) + "<br>"
    for row in table_content:
        table_text += " | ".join(row) + "<br>"
    table_text += f"<br>Table Caption:<br>"
    table_text += caption
    return table_text


data = json.load(open("data/scigen/dev.json"))
output_data = {}

for example_id, example in data.items():
    table_text = generate_table_text(example["table_column_names"], example["table_content_values"], example["table_caption"])
    example["table_text"] = table_text
    example["text"] = example["text"].replace("[CONTINUE]", "")

    output_data[example_id] = example

json.dump(output_data, open("data/scigen/dev_processed.json", "w"), indent=4)

    

