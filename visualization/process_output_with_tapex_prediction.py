from process_output import *

if __name__ == "__main__":
    file_path =  'data/raw_jsons/r2d2_output_evaluation_result.json'

    data = json.load(open(file_path))
    output_data = {}
    titles = get_title("data/logicnlg/test_lm.json")
    example_id = 0
    for csv_id, example in data.items():
        output_data[example_id] = {}
        output_data[example_id]["csv_id"] = csv_id
        output_data[example_id]["sentences"] = example["sent"]
        output_data[example_id]["title"] = titles[csv_id]
        output_data[example_id]["labels"] = example["label"]

        csv_path = f"data/all_csv/{csv_id}"
        output_data[example_id]["table"], output_data[example_id]["table_text"], = read_csv_table(csv_path)

        prefix_table_text = f"Table Title: {output_data[example_id]['title']}<br><br>"
        prefix_table_text += f"Table Content:<br>"
        output_data[example_id]["table_text"] = prefix_table_text + output_data[example_id]["table_text"]
        example_id += 1

    json.dump(output_data, open('data/r2d2_output_evaluation_result_visualization.json', "w"), indent=4)