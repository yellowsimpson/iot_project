import yaml

data = {
    "train" : '/box_data/train/',
        "val" : '/box_data/valid/',
        "test" : '/box_data/test/', 
        "names" : {0 : 'blue_box', 1 : 'red_box', 2 : 'green_box', 3 : 'yellow_box'}}

with open('./box_data.yaml', 'w') as f :
    yaml.dump(data, f)

# check written file
with open('./box_data.yaml', 'r') as f :
    lines = yaml.safe_load(f)
    print(lines)
    