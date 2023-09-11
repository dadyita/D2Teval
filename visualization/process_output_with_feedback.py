from process_output import *

def remove_number(feedbacks):
    return [feedback[3:] if feedback[1] == "." else feedback for feedback in feedbacks]

if __name__ == "__main__":
    gpt3_file_path =  'data/raw_jsons/r2d2_output_evaluation_GPT3.5.json'
    gpt4_file_path =  'data/raw_jsons/r2d2_output_evaluation_GPT4.json'

    gpt3_data = json.load(open(gpt3_file_path))
    gpt4_data = json.load(open(gpt4_file_path))

    output_data = {}
    example_id = 0
    for example_id, example in gpt3_data.items():
        if "feedback" not in example:
            continue
        output_data[example_id] = {}
        output_data[example_id]["csv_id"] = example["csv_id"]
        output_data[example_id]["sentences"] = example["sentences"]
        output_data[example_id]["title"] = example["title"]
        output_data[example_id]["labels"] = example["labels"]
        output_data[example_id]["table"] = example["table"]
        output_data[example_id]["table_text"] = example["table_text"]

        output_data[example_id]["gpt3_feedback"] = remove_number(example["feedback"])
        output_data[example_id]["gpt4_feedback"] = remove_number(gpt4_data[example_id]["feedback"])
        

    json.dump(output_data, open('data/r2d2_output_w_feedback.json', "w"), indent=4)