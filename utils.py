from formatting import *

def get_test_number():
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

	return t

def get_choice(arr):
	if not arr:
		print("!!! ARRAY is empty !!!")
		return -1

	choice = 0
	while(choice < 1 or choice > len(arr)):
		print("Choose among the following : ")
		for i in range(len(arr)):
			print(f"{i+1} . {arr[i]}")
		inp = input("Enter your choice : ")
		if not inp.isnumeric():
			print("!!!! INVALID INPUT !!!!")
		else:
			choice = int(inp)
			if choice < 1 or choice > len(arr):
				print("!!!! INVALID CHOICE !!!!")
	return choice

def get_multi_choices(arr):
	choices = []
	valids = [i+1 for i in range(len(arr))]
	while(len(choices)<=0 or not set(choices).issubset(set(valids))):
		print("Choose multiple choice among the followings : ")
		for j in range(len(arr)):
			print(f"{j+1}. {arr[j]}")
		inps = (input(f"Enter choices separated by space (e.g., 1 3 7) : ")).split(" ")
		print("inputs:  ",inps)
		if not all(x.isnumeric() for x in inps):
			print("!!!! INVALID INPUT !!!!")
		else:
			choices = [int(x) for x in inps]
			if not set(choices).issubset(set(valids)):
				print("!!!! INVALID CHOICE !!!!")
	choices = sorted(choices)
	print("Choices picked up : ",choices)
	return choices

def get_subject_name(subjects):
	choice = get_choice(subjects)

	sub = subjects[choice-1]
	print(f"{sub} chosen.")

	subject_abbr = [''.join(i[0].upper() for i in s.split() if len(i) > 3) for s in subjects]
	print("Subject Abbreaviations : ",subject_abbr)

	return sub , subject_abbr[choice-1]

def get_number_of_questions():
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

	return n

def get_response(valids,n):
	ans = ''
	while ans not in valids:
		ans = input(f"Enter answer for question number {n} ({'/'.join(v.upper() for v in valids)}) : ").upper()
		if ans not in valids:
			print("!!!! INVALID INPUT !!!!!")
	return ans

def get_answers(am):
	t = get_test_number()

	subjects = am.get_subjects()
	sub , sub_abbr = get_subject_name(subjects)

	row_name = f"T{t}{sub_abbr}"

	topics = am.get_topics(sub)
	print(f"{sub} topics are : {topics}")

	n = get_number_of_questions()

	answers = []
	tag_list = []
	for i in range(n):
		ans = get_response(['A','B','C','D'],i+1)
		answers.append(ans)

		tags_nos = get_multi_choices(topics)
		tag_list.append([topics[x-1] for x in tags_nos])
		
	print("Answers : ",answers)
	print("Tags : ",tag_list)

	return t , row_name, answers , tag_list


def get_student_answer(am):
	students = am.get_students()
	choice = get_choice(students)
	name = students[choice-1]
	print(f"{name} chosen")

	t = get_test_number()

	subjects = am.get_subjects()
	sub , sub_abbr = get_subject_name(subjects)

	row_name = f"T{t}{sub_abbr}"

	n = get_number_of_questions()

	answers = []
	for i in range(n):
		ans = get_response(['A','B','C','D','NA'],i+1)
		answers.append(ans)

	print("Student Name : ",name)	
	print("Answers : ",answers)

	return t , name , row_name , answers

def update_fundamentals(am):
	print("-"*30 + "\nFundamental Informations\n"+"-"*30)
	ops = ["Add Mentor","Add Student","Add Subject","Add Topics","Delete Mentor","Delete Student","Delete Subject" , "Exit"]

	choice = 0
	while choice != len(ops):
		choice = get_choice(ops)

		if choice == 1:
			name = input("Enter the mentor name : ")
			am.add_mentors([name])
		elif choice == 2:
			name = input("Enter the student name : ")
			am.add_students([name])
		elif choice == 3:
			name = input("Enter the subject name : ")
			am.add_subjects([name])
		elif choice == 4:
			subjects = am.get_subjects()
			sub , _ = get_subject_name(subjects)
			name = input("Enter comma separated topic names for subject {sub} (e.g., Number System , Divisibility): ")
			name = name.replace(" , ",",").replace(", ",",").replace(" ,",",")
			topics = [topic for topic in name.split(",") if topic]
			am.add_topics(sub,topics)

def update_reports(am):
	print("-"*30 + "\nAnswers , Responses and Reports\n"+"-"*30)
	ops = ["Add Test Answer" , "Add Student Response" , "Make Report"  , "Make Result", "Write ALL into Spreadsheet", "Update Test Answer" , "Update Student Response", "Exit"]

	choice = 0
	while choice != len(ops):
		choice = get_choice(ops)

		if choice == 1:
			test_num ,rname , ans , tags = get_answers(am)
			am.add_answers(test_num , rname,ans,tags)
		elif choice == 2:
			test_num , sname , qname , answers = get_student_answer(am)
			am.add_student_response(test_num , sname,qname,answers)
		elif choice == 3:
			col_types = ['topic','subject','test','all']
			ch = get_choice(col_types)
			if ch != len(col_types):
				am.add_report(col_types[ch-1])
			else:
				for col_type in col_types[:-1]:
					am.add_report(col_type)
		elif choice == 4:
			tests = am.get_tests()
			tests_str = ["Test - "+str(t) for t in tests] + ["All"]
			ch = get_choice(tests_str)
			if ch != len(tests_str):
				am.make_test_result(tests[ch-1])
			else:
				for test in tests:
					am.make_test_result(test)
		elif choice == 5:
			am.write_all()

def update_acadomate(am):
	print("-"*30 + "\nWELCOME to Acadomate\n"+"-"*30)
	ops = ["Update Fundamentals" , "Update Reports", "Exit"]

	choice = 0
	while choice != len(ops):
		choice = get_choice(ops)

		if choice == 1:
			update_fundamentals(am)
		elif choice == 2:
			update_reports(am)

		am.write_all()

	reports = ['topic','subject','test']
	for rep in reports:
		format_report(am,rep)
	
	tests = am.get_tests()
	for t in tests:
		format_result(am,t)
	