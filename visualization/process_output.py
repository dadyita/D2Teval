import json

def read_csv_table(file_path):
    table = []
    with open(file_path, "r") as f:
        for line in f:
            table.append(line.strip().split("#"))
    
    table_text = ""
    for row in table:
        table_text += " | ".join(row) + "<br>"
    return table, table_text

def get_title(file_path):
    titles = {}
    data = json.load(open(file_path))
    for csv_id in data:
        titles[csv_id] = data[csv_id][0][2]

    return titles


if __name__ == "__main__":
    file_path = "r2d2_output.json"

    data = json.load(open(file_path))
    output_data = {}
    titles = get_title("test_lm.json")
    example_id = 0
    for csv_id, sents in data.items():
        output_data[example_id] = {}
        output_data[example_id]["csv_id"] = csv_id
        output_data[example_id]["sentences"] = sents
        output_data[example_id]["title"] = titles[csv_id]

        csv_path = f"data/all_csv/{csv_id}"
        output_data[example_id]["table"], output_data[example_id]["table_text"], = read_csv_table(csv_path)
        example_id += 1

    json.dump(output_data, open("r2d2_output_processed.json", "w"), indent=4)
