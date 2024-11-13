id_map = {}

name_id_map = {}

objects = []

# blocks
objects.extend([
    "coal_block", "diamond_block", "iron_block", "border"
])

# items
objects.extend([
    "raw_coal", "refined_coal", "raw_diamond", "refined_diamond", "raw_iron", "refined_iron"
])

# machine types
objects.extend([
    "conveyor", "split_conveyor_left", "split_conveyor_right", "furnace", "miner", "seller"
])

for object_ in objects:
    id_map[object_] = len(id_map)+1

for k, v in id_map.items():
    name_id_map[v] = k
