from acadomate import Acadomate
from utils import get_answers

if __name__ == '__main__':
	am = Acadomate()

	# am.add_mentors(["Abrar Hossain"])
	# am.add_students(["Pratyaya Mandal"])
	# am.add_students(["Pratyaya Mandal"])
	# am.add_mentors(["Santanu Das","Baby Ghosh"])
	# am.add_students(["Sujata Bhandari"])
	# am.add_subjects(["Maths","Language"])
	# am.add_subjects(["Mental Ability"])
	# am.add_topics("Mental Ability",["Mirror","Odd out"])
	# am.add_topics("Maths",["Number System","Divisibility"])


	rname , ans , tags = get_answers(am)
	am.add_answers(rname,ans,tags)




	am.write_all();