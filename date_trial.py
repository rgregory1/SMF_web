import datetime

def convert_timestamp(i):
	i = i[:-2]
	return datetime.datetime.strptime(i, "%Y%m%d%H%M%S")

new = convert_timestamp('2018042411413342')

print(new)
