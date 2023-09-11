import asyncio
import api_utils
import argparse
import time
import re
import os

synonym_perturbation_prompt = "Replace some entities with synonyms. Return three different candidates in numbered list."

abbreviation_perturbation_prompt = "Replace two or three of entities with abbreviation. Return three different candidates in numbered list."

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_qa_path", type=str, default="data/wtq/wtq_orig_qa.json")
    parser.add_argument("--input_table_path", type=str, default="data/wtq/wtq_orig_table.json")
    parser.add_argument("--output_dir", type=str, default="data/wtq/header_level")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo")
    parser.add_argument("--perturbation_type", type=str, default="synonym")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--max_tokens", type=int, default=256)
    parser.add_argument("--top_p", type=float, default=1.0)
    parser.add_argument("--api_key", type=str, default="")
    parser.add_argument("--max_num", type=int, default=-1)
    args = parser.parse_args()
    requests_per_minute = 100 if args.model == "gpt-4" else 300

    os.makedirs(args.output_dir, exist_ok=True)
    output_table_path = os.path.join(args.output_dir, f"{args.perturbation_type}_perturbed_table.json")
    output_qa_path = os.path.join(args.output_dir, f"{args.perturbation_type}_perturbed_qa.json")


    table_data = read_data(args.input_table_path)
    if args.max_num > 0:
        table_data = dict(list(table_data.items())[:args.max_num])


    question_data = read_data(args.input_qa_path)

    prompt = synonym_perturbation_prompt if args.perturbation_type == "synonym" else abbreviation_perturbation_prompt
    
    questions = [" | ".join(table["header"]) for i, table in table_data.items()]
    messages = [perturbation_prompt(question, prompt) for question in questions]


    responses = asyncio.run(generate_from_openai_chat_completion(
        api_key=args.api_key,
        messages=messages,
        engine_name=args.model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        top_p=args.top_p,
        requests_per_minute=requests_per_minute,
    ))

    output_table_data = {}
    table_id_map = {}
    for i, (table_id, example) in enumerate(table_data.items()):
        table_id_map[table_id] = []
        header = example["header"]

        response = responses[i]
        perturbed_header = [i.strip()[2:].strip() for i in response.split("\n") if re.match(r"\d\.", i) and i.strip()]

        if len(perturbed_header) != 3:
            print("incorrect format: ", response)

        for j, perturbed_header in enumerate(perturbed_header):
            new_header = [i.strip() for i in perturbed_header.split(" | ") if i.strip()]
            if len(new_header) != len(header):
                continue

            output_example = example.copy()
            output_example["header"] = new_header
            output_example["original_header"] = header
            new_table_id = f"{table_id}/{args.perturbation_type}_{j}"
            
            output_table_data[new_table_id] = output_example
            table_id_map[table_id].append(new_table_id)

    output_qa_data = []
    for example in question_data:
        table_id = example["table_id"]
        if table_id not in table_id_map:
            continue
        for i, new_table_id in enumerate(table_id_map[table_id]):
            output_example = example.copy()
            output_example["original_id"] = example["id"]
            output_example["id"] = f"{example['id']}/{args.perturbation_type}-{i}"
            output_example["original_table_id"] = table_id
            output_example["table_id"] = new_table_id
            output_qa_data.append(output_example)
    
    json.dump(output_table_data, open(output_table_path, "w"), indent=4)
    print(f"Saved processed wtq data to {output_table_path}, with {len(output_table_data)} table examples.")
    json.dump(output_qa_data, open(output_qa_path, "w"), indent=4)
    print(f"Saved processed wtq data to {output_qa_path}, with {len(output_qa_data)} QA examples.")
        


        