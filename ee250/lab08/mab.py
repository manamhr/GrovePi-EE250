def move_index_left(array):
    for i in range(0, len(array) - 1):
        array[i] = array[i+1]

def average(array):
    sum = 0
    for i in range(0, len(array)):
        sum = sum + array[i]
    return sum/len(array)

def printlol(array):
    for i in range(0, len(array)):
        print(array[i])


def moving_avg_buffer(mab, array):
    move_index_left(mab)
    average_array = average(array)
    mab[len(mab) - 1] = average_array

def difference(diff_array, dist_array):
    move_index_left(diff_array)
    for i in range(0, len(dist_array)-1):
        diff_array[i] = dist_array[i+1] - dist_array[i]



test = [1,4,0,10,13]
diff = [0,0,0,0,0]
size_array = 5


difference(diff, test)
printlol(diff)