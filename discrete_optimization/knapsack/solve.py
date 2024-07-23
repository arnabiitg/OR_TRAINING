import sys
sys.setrecursionlimit(3000)

def greedy_knapsack(items, capacity):
    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x.value/x.weight, reverse=True)
    taken = [0 for _ in range(len(items))]
    total_value = 0
    total_weight = 0
    
    for item in items:
        if total_weight + item.weight <= capacity:
            total_value += item.value
            total_weight += item.weight
            taken[item.index] = 1
    
    return total_value, taken

def dynammic_approach(items,n,k,dp,taken):
    if n<=0 or k<=0:
        return 0
    if(dp[n-1][k-1] != 0):
        return dp[n-1][k-1]

    if(items[n-1].weight<=k):
        a = dynammic_approach(items,n-1,k-(items[n-1].weight),dp,taken)
        a = items[n-1].value + a
        b = dynammic_approach(items,n-1,k,dp,taken)
        if(a>b):
            if n == 1:
                taken[n-1][k-1] = 1
            else:
                taken[n-1][k-1] = taken[n-2][k-(items[n-1].weight)-1] + pow(2,n-1) 
            dp[n-1][k-1] = a
        else:
            taken[n-1][k-1] = taken[n-2][k-1]
            dp[n-1][k-1] = b
    else:
        dp[n-1][k-1]= dynammic_approach(items,n-1,k,dp,taken)
        if n == 1:
            taken[n-1][k-1] = 0
        else:
            taken[n-1][k-1] = taken[n-2][k-1]
    return dp[n-1][k-1]
