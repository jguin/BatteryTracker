import database


def read_cells(tun, sn_start, sn_end):
    data = database.repacker_range_query(tun, sn_start, sn_end)
    return data

