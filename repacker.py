import database

packs_capacity = []


def read_cells(tun, sn_start, sn_end):
    data = database.repacker_range_query(tun, sn_start, sn_end)
    return data


def sort_cells(cell_data):
    cell_data.sort(key=lambda x: x[1], reverse=True)
    return cell_data


def build_pack(num_cells, sorted_cell_data):
    packs = []
    packs_capacity.clear()
    for x in range(num_cells):
        packs.append([x])
    cells_to_remove = len(sorted_cell_data) % num_cells
    if cells_to_remove != 0:
        stripped_sorted_cell_data = sorted_cell_data[:-cells_to_remove]
    else:
        stripped_sorted_cell_data = sorted_cell_data
    for x in range(num_cells):
        packs_capacity.append(0)
    while stripped_sorted_cell_data:
        for x in range(num_cells):
            lowest_pack = lowest_capacity()
            current_cell = stripped_sorted_cell_data.pop(0)
            add_cell(lowest_pack, current_cell[1])
            packs[lowest_pack].append(current_cell)
    return packs


def add_cell(pack_num, capacity):
    packs_capacity[pack_num] += capacity


def get_capacity(pack_num):
    return packs_capacity[pack_num]


def lowest_capacity():
    min_capacity = min(packs_capacity)
    min_index = packs_capacity.index(min_capacity)
    return min_index
