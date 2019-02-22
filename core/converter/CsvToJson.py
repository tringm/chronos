import json

import pandas as pd

from config import root_path

folder_path = root_path() / "examples" / "io"
var_type = ["string", "integer", "number", "boolean", "decimal"]
aito_var_type = ["String", "Int", "Decimal", "Boolean", "Decimal"]

all_tables = {}
all_tables_schema = {}
all_tables_data = {}

for file_name in folder_path.glob('**/*.csv'):
    all_tables[file_name.stem] = pd.read_csv(file_name)

# print(all_tables.keys())

for key in all_tables.keys():
    table_df = all_tables[key]
    all_tables_schema[key] = pd.io.json.build_table_schema(table_df, index=False)['fields']
    all_tables_data[key] = table_df.to_json(orient="records")

schema = ""
schema += "{\"tables\":["

keys = list(all_tables.keys())
for i in range(len(keys)):
    key = keys[i]
    # print(key)
    table_schema = all_tables_schema[key]

    # fixed table schema to fit aito schema (name -> column, type is capitalized)
    # !!! Currently not support null (?)

    # table_schema_fixed = []
    # for i in range(len(table_schema)):
    #   column_schema = {}
    #   column_schema['column'] = table_schema[i]['name']
    #   column_schema['type'] = aito_var_type[var_type.index(table_schema[i]['type'])]
    #   table_schema_fixed.append(column_schema)
    # print(table_schema_fixed)
    table_schema_json_string = "["
    for j in range(len(table_schema)):
        table_schema_json_string += "{ \"column\":" + "\"" + table_schema[j]['name'] + "\"" + ","
        table_schema_json_string += "\"type\": " + "\"" + aito_var_type[
            var_type.index(table_schema[j]['type'])] + "\"" + "}"
        if j != len(table_schema) - 1:
            table_schema_json_string += ","
    table_schema_json_string += "]"
    # print(table_schema_json_string)

    # add table
    # add table name
    schema += "{ \"table\": " + "\"" + key + "\"" + ","
    # add columns schema
    schema += "\"columns\": "
    schema += table_schema_json_string
    schema += "}"
    if i != (len(keys) - 1):
        schema += ","
    # print(schema)
schema += "]}"

output_folder_path = root_path() / "examples" / "io"
# output_folder_path = "../generate_data/test_data/json/"
with (output_folder_path / 'schema.json').open(mode='w') as outfile:
    parsed = json.loads(schema)
    print(json.dumps(parsed, indent=4))
    json.dump(parsed, outfile)

for key in all_tables.keys():
    name = key + '.json'
    with (output_folder_path / name).open(mode='w') as outfile:
        parsed = json.loads(all_tables_data[key])
        json.dump(parsed, outfile)