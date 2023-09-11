import json, os
import pandas as pd
import argparse

def get_box_abbreviation_map(box_map_txt_path):
    data = open(box_map_txt_path).readlines()
    box_score_abbrev_map = {}
    for line in data:
        line = line.strip()
        abbrev = line.split(" - ")[0].strip()
        full_name = line.split(" - ")[1].split("(row_number")[0].strip()
        box_score_abbrev_map[abbrev] = full_name
    return box_score_abbrev_map

def get_line_abbreviation_map(line_map_txt_path):   
    data = open(line_map_txt_path).readlines()
    line_score_abbrev_map = {}
    for line in data:
        line = line.strip()
        abbrev = line.split(" - ")[0].strip()
        full_name = line.split(" - ")[1].split("(")[0].strip()
        line_score_abbrev_map[abbrev] = full_name
    return line_score_abbrev_map

def create_box_score_table(box_score_line, box_score_abbrev_map):
    playname_map = box_score_line["PLAYER_NAME"]
    box_score_dict = {} # dict[player] = [attributes...]
    for id in playname_map:
        box_score_dict[playname_map[id]] = []
    for attribute_name in box_score_abbrev_map.keys():
        for id in box_score_line[attribute_name]:
            value = box_score_line[attribute_name][id]
            box_score_dict[playname_map[id]].append(value)

    box_score_columns = [box_score_abbrev_map[abbrev_name] for abbrev_name in box_score_abbrev_map.keys()]
    return pd.DataFrame.from_dict(box_score_dict,orient='index', columns= box_score_columns)


def create_line_score_table(home_line, vis_line, line_score_abbrev_map):
    # ret_dict[team_name] = []
    line_score_dict = {}
    for line in [home_line, vis_line]:
        team_name = line["TEAM-NAME"]
        line_score_dict[team_name] = []
        for abbrev in line_score_abbrev_map.keys():
            line_score_dict[team_name].append(line[abbrev])

    line_score_columns = [line_score_abbrev_map[abbrev_name] for abbrev_name in line_score_abbrev_map.keys()]
    return pd.DataFrame.from_dict(line_score_dict, orient='index', columns= line_score_columns)

def convert_df_to_text(df):
    # also include header
    text = ""
    for column in df.columns:
        text += column + " | "
    text += "\n"
    for row in df.values:
        for v in row:
            text += str(v) + " | "
        text += "\n"
    return text

def convert_df_to_list(df):
    # also include header
    table = [[]]
    for column in df.columns:
        table[0].append(column)
    for row in df.values:
        table.append(list(row))
    return table


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--pred_path", type=str, default="data/rotowire/predictions/macro.txt")
    parser.add_argument("--gold_path", type=str, default="data/rotowire/raw_data/test.json")
    parser.add_argument("--box_map_txt_path", type=str, default="data/rotowire/raw_data/box_score_map.txt")
    parser.add_argument("--line_map_txt_path", type=str, default="data/rotowire/raw_data/line_score_map.txt")
    parser.add_argument("--output_path", type=str, default="data/rotowire/visualization.json")
    args = parser.parse_args()

    box_score_abbrev_map = get_box_abbreviation_map(args.box_map_txt_path)
    line_score_abbrev_map = get_line_abbreviation_map(args.line_map_txt_path)

    raw_data = json.load(open(args.gold_path))
    pred_data = open(args.pred_path).readlines()
    output_example = {}

    assert len(raw_data) == len(pred_data)
    for i, (raw_line, pred) in enumerate(zip(raw_data, pred_data)):
        box_score_table_df = create_box_score_table(raw_line["box_score"], box_score_abbrev_map) 
        line_score_table_df = create_line_score_table(raw_line["home_line"], raw_line["vis_line"], line_score_abbrev_map)

        pred_text = pred.strip()
        gold_text = " ".join(raw_line["summary"])

        line_score_table_str, box_score_table_str = convert_df_to_text(line_score_table_df), convert_df_to_text(box_score_table_df)

        copy_str = f"Box Score Table:\n{box_score_table_str}\nLine Score Table:\n{line_score_table_str}\n"

        example = {
            "table1": convert_df_to_list(box_score_table_df),
            "table2": convert_df_to_list(line_score_table_df),
            "table1_str": box_score_table_str,
            "table2_str": line_score_table_str,
            "pred": pred_text,
            "gold": gold_text,
            "copy_str": copy_str.replace("\n", "<br>")
        }

        output_example[str(i)] = example

    json.dump(output_example, open(args.output_path, "w"), indent=4)