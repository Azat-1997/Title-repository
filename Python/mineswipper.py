import sys
# two different modes: from regular file and standart input stream 
def get_field_conf(filename):
    mine = set()
    with open(filename) as file:
        nrow, ncol= map(int, file.readline().split())
        field = file.readlines()
        for row, line in enumerate(field):
            for col, cell in enumerate(line):
                if cell == "*":
                    mine.add((row, col))
                
    return {"ncol":ncol, "nrow":nrow, "mines_coords":mine}
 
def get_from_std():
    mine = set()
    nrow, ncol= map(int, sys.stdin.readline().split())
    field = sys.stdin.readlines()
    for row, line in enumerate(field):
        for col, cell in enumerate(line):
            if cell == "*":
                mine.add((row, col))

    return {"ncol":ncol, "nrow":nrow, "mines_coords":mine}


def get_neigbores(nrow, ncol, mine):
    neigbores = set()    
    for x in range(-1, 2):
        for y in range(-1, 2):
            if (x, y) == (0, 0) or (mine[0] + x < 0) or (mine[0] + x > nrow - 1) or (mine[1] + y < 0) or (mine[1] + y > ncol - 1):
                # skip mine itself and make correction for the borders
                continue
            else:
                neigbores.add((mine[0] + x, mine[1] + y)) 
        
    return neigbores
          
def fill_neigbores(field_conf):
    ncol = field_conf["ncol"]
    nrow = field_conf["nrow"]
    mines = field_conf["mines_coords"]
    neigbores = {}
    for m in  mines:
        ng = get_neigbores(nrow, ncol, m)
        for coord in ng:
            if coord in mines:
                continue
                
            if not coord in neigbores.keys():
                neigbores[coord] = 1
            else:
                neigbores[coord] += 1
                
    return neigbores
     
 
def print_solved_field(field_conf):
     ncol = field_conf["ncol"]
     nrow = field_conf["nrow"]
     mines = field_conf["mines_coords"]
     neigbores = fill_neigbores(field_conf)
     for x in range(nrow):
        for y in range(ncol):
            if (x, y) in mines:
                print("*", end ="")
            elif (x, y) in neigbores.keys():
                print(neigbores[(x, y)], end="")
            else:
                print(0, end = "")
        print()
         
         
if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("Solution: ")
        field_conf = get_field_conf(sys.argv[1])
        print_solved_field(field_conf)
    else:
        print("Solution: ")
        field_conf = get_from_std()
        print_solved_field(field_conf)



        
