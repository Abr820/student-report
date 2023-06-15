from acadomate import Acadomate
from utils import get_answers , get_student_answer,update_fundamentals

if __name__ == '__main__':
	am = Acadomate()

	update_fundamentals(am)
	
	am.write_all()


	# test_num ,rname , ans , tags = get_answers(am)
	# am.add_answers(test_num , rname,ans,tags)
	# am.write_all()

	# test_num , sname , qname , answers = get_student_answer(am)
	# am.add_student_response(test_num , sname,qname,answers)
	# am.write_all()

	# am.add_report()
	# am.add_report('topic')
	# am.add_report('subject')
	# am.add_report('test')
	# am.write_all()

	am.make_test_result(1)
	am.make_test_result(2)
	am.write_all()