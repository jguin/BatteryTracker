import database


def read_cells(tun, sn_start, sn_end):
    data = database.repacker_range_query(tun, sn_start, sn_end)
    return data


def sort_cells(cell_data):
    cell_data.sort(key=lambda x: x[1])
    return cell_data


def build_pack(num_cells, sorted_cell_data):
    packs = []
    for x in range(num_cells):
        packs.append('')
    print(packs)
    cells_to_remove = len(sorted_cell_data) % num_cells
    stripped_sorted_cell_data = sorted_cell_data[:-cells_to_remove]
    while stripped_sorted_cell_data:
        for x in range(num_cells):
            if not packs[x]:
                packs[x] = stripped_sorted_cell_data.pop()
            else:
                packs[x].append(stripped_sorted_cell_data.pop())
    for x in packs:
        print(x)
