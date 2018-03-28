def move_index_left(array, size):
	for i in range(size - 1):
		array[i] = array[i+1]

	"""
	for i in range(size):
		print(array[i])
	"""

def average(array, size):
	sum = 0
	for i in range(size):
		sum = sum + array[i]
	return sum/size

def printlol(array,size):
	for i in range(size):
		print(array[i])


def moving_avg_buffer(mab, array, size):
	move_index_left(mab, size)
	average_array = average(array, size)
	mab[size-1] = average_array

def difference(diff_array, dist_array, size):
	move_index_left(diff_array, size)
	for i in range(size-1):
		diff_array[i] = dist_array[i+1] - dist_array[i]



test = [1,4,0,10,13]
diff = [0,0,0,0,0]
size_array = 5

difference(diff, test, size_array)
printlol(diff, size_array)
