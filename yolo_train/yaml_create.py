import yaml

data = {
    "train" : '/box_data_6/train/',
        "val" : '/box_data_6/valid/',
        "test" : '/box_data_6/test/', 
        "names" : {0 : 'red_line'}}

with open('./box_data_6.yaml', 'w') as f :
    yaml.dump(data, f)

# check written file
with open('./box_data_6.yaml', 'r') as f :
    lines = yaml.safe_load(f)
    print(lines)
    