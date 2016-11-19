import time
begin = int(round(time.time() * 1000))
for i in range(100000):
	print(i)
final = int(round(time.time() * 1000))
print(final - begin)