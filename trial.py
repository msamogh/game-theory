for i in range(60):
		a = range(i)
		x = [a[x:x+4] for x in range(0, len(a), 4)]
		y = [a[x:x+5] for x in range(0, len(a), 5)]
		print(str(len(x)) + ' ' + str(len(y)))