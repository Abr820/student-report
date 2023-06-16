from acadomate import Acadomate
from utils import get_answers , get_student_answer,update_fundamentals , update_reports

if __name__ == '__main__':
	am = Acadomate()

	update_fundamentals(am)
	am.write_all()

	update_reports(am)
	am.write_all()
