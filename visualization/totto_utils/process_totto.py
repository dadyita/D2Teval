# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Creates HTML for annotated examples for easy visualization."""
import json
import os


import table_to_text_html_utils
from preprocess_data_main import *
import six


def main():
  input_path = "data/totto/totto_dev_data.jsonl"
  pref_path = "data/totto/predictions.json"
  output_path = "data/totto/visualization.json"
  
  predictions = json.load(open(pref_path))
  outputs = {}
  with open(input_path, "r", encoding="utf-8") as input_file:
    index = 0
    for line in input_file:
      line = six.ensure_text(line, "utf-8")
      example = json.loads(line)
      html_str = table_to_text_html_utils.get_example_html(example)
      example["html_str"] = html_str.replace("\n", "")
      example_id = example["example_id"]

      pred_text = predictions[str(example_id)]
      example["text"] = pred_text
      
      table = example["table"]
      cell_indices = example["highlighted_cells"]

      table_page_title = example["table_page_title"]
      table_section_title = example["table_section_title"]

      subtable = (
          preprocess_utils.get_highlighted_subtable(
              table=table,
              cell_indices=cell_indices,
              with_heuristic_headers=True))
      subtable_metadata_str = (
          preprocess_utils.linearize_subtable(
              subtable=subtable,
              table_page_title=table_page_title,
              table_section_title=table_section_title))
      
      example["table_text"] = subtable_metadata_str

      outputs[index] = example

      index += 1
      if index > 100:
        break

  json.dump(outputs, open(output_path, "w"), indent=4)


if __name__ == "__main__":
  main()
