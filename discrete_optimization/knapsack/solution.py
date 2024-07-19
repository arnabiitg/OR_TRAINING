def branching(index, cap, items):
    if index>= len(items) or items[index].weight > cap:
        return [0 for _ in range(len(items))],0
    
    # not taking the current node
    taken1, val1 = branching(index+1,cap,items)

    # taking the current node
    cap = cap - items[index].weight
    taken2,val2 = branching(index+1,cap,items)
    val2 = val2 + items[index].value
    taken2[index] = 1

    if val1 > val2:
        return taken1, val1
    else:
        return taken2, val2