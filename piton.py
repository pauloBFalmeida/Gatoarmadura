def algo(a, **kwargs):
	# b = kwargs.get('b')
    # c = kwargs.get('c')
	print(a)
	for k in kwargs.items():
		if k[0] == 'b':
			print('finalmente'+str(k[1]))
		print(k)
	# for key, value in kwargs.items():
	# 	print("The value of {} is {}".format(key, value))

algo(10)
algo(10, b=5)
algo(10, c=12)
algo(10, b=2,c=3)
