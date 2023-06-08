def get_answers(am):
	t = -1
	while(t<=0):
		inp = input("Enter test number : ")
		if not inp.isnumeric():
			print("!!!! INVALID INPUT !!!!")
		else:
			t = int(inp)
			if t <= 0:
				print("!!!! INVALID CHOICE !!!!")
	print(f"Test number : {t}")

	subjects = am.get_subjects()
	choice = 0
	while(choice < 1 or choice > 3):
		print("Choose which subject among the following : ")
		for i in range(len(subjects)):
			print(f"{i+1} . {subjects[i]}")
		inp = input("Enter your choice : ")
		if not inp.isnumeric():
			print("!!!! INVALID INPUT !!!!")
		else:
			choice = int(inp)
			if choice < 1 or choice > len(subjects):
				print("!!!! INVALID CHOICE !!!!")

	sub = subjects[choice-1]
	print(f"{sub} chosen.")

	subject_abbr = [''.join(i[0].upper() for i in s.split() if len(i) > 3) for s in subjects]
	print("Subject Abbreaviations : ",subject_abbr)

	row_name = f"T{t}{subject_abbr[choice-1]}"

	topics = am.get_topics(sub)
	print(f"{sub} topics are : {topics}")

	n = 0
	while(n<=0):
		inp = input("Number of questions : ")
		if not inp.isnumeric():
			print("!!!! INVALID INPUT !!!!")
		else:
			n = int(inp)
			if n <= 0:
				print("!!!! INVALID CHOICE !!!!")
	print(f"{n} questions")

	answers = []
	tag_list = []
	for i in range(n):
		ans = 'NA'
		valids = ['A','B','C','D']
		while ans not in valids:
			ans = input(f"Enter answer for question number {i+1} : ").upper()
			if ans not in valids:
				print("!!!! INVALID INPUT !!!!!")
		answers.append(ans)

		tags_nos = []
		valids = [i+1 for i in range(len(topics))]
		while(len(tags_nos)<=0 or not set(tags_nos).issubset(set(valids))):
			print("Choose topics among the followings : ")
			for j in range(len(topics)):
				print(f"{j+1}. {topics[j]}")
			inps = (input(f"Enter topic choices for question {i+1} separated by space (e.g., 1 3 7) : ")).split(" ")
			print("inputs:  ",inps)
			if not all(x.isnumeric() for x in inps):
				print("!!!! INVALID INPUT !!!!")
			else:
				tags_nos = [int(x) for x in inps]
				if not set(tags_nos).issubset(set(valids)):
					print("!!!! INVALID CHOICE !!!!")
		print("Tag Numbers : ",tags_nos)
		tag_list.append([topics[x-1] for x in tags_nos])
		
	print("Answers : ",answers)
	print("Tags : ",tag_list)

	return row_name, answers , tag_list