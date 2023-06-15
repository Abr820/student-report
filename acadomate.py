import gspread
import pandas as pd
import numpy as np
import re
import gspread_dataframe as gpd

class Acadomate:
	def __init__(self, cred_file = "acadomate-report-7028d1340299.json",sheet_name = "Acadomate Report"):
		self._gc = gspread.service_account(filename= cred_file)
		try:
			self.sh = self._gc.open(sheet_name)
			print("Spreadsheet exists")
		except SpreadsheetNotFound:
			print("Spreadsheet doesn't exist")
		self.sheets = [ws.title for ws in self.sh.worksheets()]
		self._dfs = {}
		self._indices = {}
		for title in self.sheets:
			self._dfs[title] = None
			self._indices[title] = None
		self.__create_sheet("Fundamental",["Tests","Mentors","Students","Subjects"])
		self.__create_sheet("Answers",["Qno","Answer","Tags"],index = "Qno")
		self.__create_sheet("Responses",["Student Name"],index = "Student Name")
		self.__create_sheet("Reports",["Student Name"],"Student Name")

	def __create_sheet(self, title , columns , index = None):
		ws = None
		if title not in self.sheets:
			ws = self.sh.add_worksheet(title=title,rows=100, cols=20)
			self.sheets = [ws.title for ws in self.sh.worksheets()]
			print(f"{title} sheet added in the given spreadsheet")
		else:
			ws = self.sh.worksheet(title)
			print(f"{title} sheet alread exist in the given spreadsheet")

		values_list = ws.row_values(1)
		if len(values_list) < len(columns):
			d = {}
			for col in columns:
				d[col] = pd.Series()
			df = pd.DataFrame(d)
			self.__write_sheet(title,df)
			print(f"Column names {columns} added")

		if index is not None and index in values_list:
			self._indices[title] = index
			print(f"{index} is added as index of sheet {title}")
		print(self._indices)

	def __read_sheet(self,title):
		if title not in self.sheets:
			print("{title} sheet doesn't exist in the given spreadsheet")
			return None
		else:
			if self._dfs[title] is not None:
				return self._dfs[title]

			worksheet = self.sh.worksheet(title)
			columns = worksheet.row_values(1)
			df = pd.DataFrame(worksheet.get_all_records(),columns=columns)
			df = df.replace({'': None,np.nan:None})

			# index = self._indices[title]
			# if index is not None and index in df.columns:
			# 	df = df.set_index(index)
			# 	print(f"{index} is set as index")

			print("Dataframe read : ")
			print(df.head())
			self._dfs[title] = df
			return df

	def __write_sheet(self,title,df, include_index = False):
		if title not in self.sheets:
			print("{title} sheet doesn't exist in the given spreadsheet")
		else:
			worksheet = self.sh.worksheet(title)
			worksheet.clear()
			df = df.fillna("")
			df = df.replace({None:'',np.nan:''})
			print("Dataframe to be saved : ")
			print(df.head())
			gpd.set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=include_index,include_column_header=True, resize=False)
			self._dfs[title] = None
			print(f"{title} is updated")

	def __add_elements(self,title,col,vals,unique = True, rearrange = True):
		df = self.__read_sheet(title)
		all_df = {}
		for c,dt in zip(df.columns,df.dtypes):
			value_list = [v for v in df[c].values.tolist() if not rearrange or (v is not None and not pd.isnull(v))]
			if c == col:
				for v in vals:
					if not unique or (unique and v not in value_list):
						value_list.append(v)
			all_df[c] = pd.Series(value_list,dtype=dt)
		df = pd.DataFrame(all_df,columns=df.columns)
		self._dfs[title] = df

	def __add_column(self,title,col_name,data, dtype):
		df = self.__read_sheet(title)
		if col_name not in df.columns:
			add_df = pd.DataFrame(pd.Series(data,dtype=dtype),columns=[col_name])
			df = pd.concat([df,add_df],axis=1)
			self._dfs[title] = df
		else:
			self.__add_elements(title,col_name,data,unique=True)

	def __get_column(self,title,col_name):
		df = self.__read_sheet(title)
		l = [v for v in df[col_name].values.tolist() if v is not None and not pd.isnull(v)]
		print(l)
		return l

	def __add_row(self,title,data,replace = True):
		df = self.__read_sheet(title)
		indexx = self._indices[title]
		if not replace:
			idx = self.__find_row_index(df,indexx,data[0])
			if idx is not None:
				data = df.loc[idx[0]].values.tolist() + data[1:]

		df = df.append(pd.Series(data, index=df.columns[:len(data)]), ignore_index=True)
		df = df.drop_duplicates(subset=[indexx],keep='last')
		self._dfs[title] = df

	def __add_value(self,title,row_name,col_name,value, index = None):
		df = self.__read_sheet(title)
		if index is None:
			index = self._indices[title]
		idx = self.__find_row_index(df,index,row_name)
		if idx is not None:
			df.loc[idx,col_name] = value
			self._dfs[title] = df

	def __find_row_index(self,df,col_name,row_val):
		idx = df.index[df[col_name] == row_val].tolist()
		if idx:
			return idx[0]
		return None

	def add_mentors(self,names):
		self.__add_elements("Fundamental","Mentors",names,unique=True)

	def add_students(self,names):
		self.__add_elements("Fundamental","Students",names,unique=True)

	def get_students(self):
		return self.__get_column("Fundamental","Students")

	def add_subjects(self,names):
		self.__add_elements("Fundamental","Subjects",names,unique=True)
		for name in names:
			self.__add_column("Fundamental",name+" Topics",[],'str')

	def get_subjects(self):
		return self.__get_column("Fundamental","Subjects")

	def add_topics(self,sub_name,topic_names):
		self.__add_elements("Fundamental",sub_name+" Topics",topic_names,unique=True,rearrange = True)

	def get_topics(self,sub):
		return self.__get_column("Fundamental",sub+" Topics")

	def get_tests(self):
		tests = [int(t) for t in self.__get_column("Fundamental","Tests")]
		return tests

	def write_all(self):
		for title in self.sheets:
			if self._dfs[title] is not None:
				self.__write_sheet(title,self._dfs[title])

	def add_answers(self, test_num , row_name , answers , tags):
		rows = [row_name+f"Q{i+1}" for i in range(len(answers))]
		for idx,ans,tag in zip(rows,answers,tags):
			self.__add_row("Answers",[idx,ans,tag],True)
		df = self.__read_sheet("Answers")
		self._dfs["Answers"] = df.sort_values("Qno")
		self.__add_elements("Fundamental","Tests",[test_num],unique=True)

	def add_student_response(self,test_num , sname,tname,answers):
		qnos = [tname+f"Q{i+1}" for i in range(len(answers))]
		for qno in qnos:
			self.__add_column("Responses",qno,[],'str')
		self.__add_elements("Responses","Student Name",[sname],unique = True)
		for qno,ans in zip(qnos,answers):
			self.__add_value("Responses",sname,qno,ans)
		df = self.__read_sheet("Responses")
		cols = ["Student Name"] + sorted(df.columns[1:])
		df = df.loc[:,cols]
		self._dfs["Responses"] = df.sort_values("Student Name")
		self.__add_elements("Fundamental","Tests",[test_num],unique=True)

	def __filter_answers(self,test_num = None , subject = None, topic = None):
		df_ans = self.__read_sheet("Answers")
		ans_d = df_ans.to_dict("index")
		ans = {vals["Qno"] : vals["Answer"] for vals in ans_d.values()}
		tags = {vals["Qno"] : list((vals["Tags"][1:-1]).replace("'","").replace(" , ",",").replace(" ,",",").replace(", ",",").split(",")) for vals in ans_d.values()}

		if test_num is not None:
			test_name = "T"+str(test_num)
			ans = {k:v for k,v in ans.items() if re.search(f"\A{test_name}",k) is not None}
			tags = {k:v for k,v in tags.items() if re.search(f"\A{test_name}",k) is not None}

		if subject is not None:
			sub_name = ''.join(i[0].upper() for i in subject.split() if len(i) > 3)
			ans = {k:v for k,v in ans.items() if re.search(f"{sub_name}Q\B",k) is not None}
			tags = {k:v for k,v in tags.items() if re.search(f"{sub_name}Q\B",k) is not None}
		
		if topic is not None:
			tags = {k:v for k,v in tags.items() if topic in v}
			ans = {k:v for k,v in ans.items() if k in tags.keys()}

		return ans,tags

	def __filter_responses(self,name,test_num = None , subject = None, topic = None):
		df = self.__read_sheet("Responses")
		idx = self.__find_row_index(df,"Student Name",name)
		if idx is not None:
			res = df.loc[idx,df.columns[1:]].to_dict()
		else:
			return dict()

		res = {k:v for k,v in res.items() if v is not None}

		if test_num is not None:
			test_name = "T"+str(test_num)
			res = {k:v for k,v in res.items() if re.search(f"\A{test_name}",k) is not None}

		if subject is not None:
			sub_name = ''.join(i[0].upper() for i in subject.split() if len(i) > 3)
			res = {k:v for k,v in res.items() if re.search(f"{sub_name}Q\B",k) is not None}

		if topic is not None:
			ques,_ = self.__filter_answers(topic=topic)
			res = {k:v for k,v in res.items() if k in ques.keys()}

		return res

	def __filter_report(self,prefix,test_num = None , subject = None, topic = None , scale = None):
		d = {}
		students = self.get_students()
		for sname in students:
			col_names = [" Correct" , " Wrong", " NotAttempted"]
			col_names = [prefix + col for col in col_names]
			for col_name in col_names:
				if col_name not in d.keys():
					d[col_name] = []
			col_vals = [ 0 , 0 , 0 ]
			res = self.__filter_responses(sname,test_num = test_num , subject = subject, topic = topic)
			ans , _ = self.__filter_answers(test_num = test_num , subject = subject, topic = topic)
			for k,v in res.items():
				if k in ans.keys():
					if v == ans[k]:
						col_vals[0] += 1
					elif v == "NA":
						col_vals[2] += 1
					else:
						col_vals[1] += 1

			for col_name , val in zip(col_names,col_vals):
				d[col_name].append(scale*val/(sum(col_vals) if sum(col_vals)>0 else 1e-6) if scale is not None else val)
		
		return d

	def compute_report(self,col_type = "topic" , test_num = None , subject = None, topic = None, scale = None):
		d = {}
		students = self.get_students()
		d["Student Name"] = students
		subjects = self.get_subjects()
		if col_type == "topic":
			for sub in subjects:
				topics = self.get_topics(sub)
				for topic in topics:
					d_new = self.__filter_report(topic,test_num=test_num,subject=sub,topic=topic,scale=scale)
					d.update(d_new)
		
		elif col_type == "subject":
			for sub in subjects:
				d_new = self.__filter_report(sub,test_num=test_num,subject=sub,topic=topic, scale=scale)
				d.update(d_new)
		
		elif col_type == "test":
			for i in self.get_tests():
				d_new = self.__filter_report("Test-"+str(i),test_num=i,subject=subject,topic=topic,scale=scale)
				d.update(d_new)
		else:
			d_new = self.__filter_report("Total",test_num=test_num,subject=subject,topic=topic,scale=scale)
			d.update(d_new)

		df = pd.DataFrame(d)
		cols = sorted(df.columns)
		if "Student Name" in cols:
			cols.remove("Student Name")
		cols.insert(0,"Student Name")
		df = df.loc[:,cols]
		return df
	
	def add_report(self,col_type = 'all'):
		worksheet_name = "Report"
		if col_type == 'topic':
			worksheet_name += "-Topic"
		elif col_type == 'subject':
			worksheet_name += "-Subject"
		elif col_type == 'test':
			worksheet_name += "-Test"
		else:
			worksheet_name += "-Average"
		
		scale = 100 if col_type != 'topic' else None
		self.__create_sheet(worksheet_name,["Student Name"],"Student Name")
		df = self.compute_report(col_type=col_type,scale=scale)
		self._dfs[worksheet_name] = df

	def make_test_result(self, test_number):
		worksheet_name = f"Result-Test{test_number}"

		df_abs = self.compute_report(col_type='subject',test_num=test_number,scale=None)
		df_100 = self.compute_report(col_type='subject',test_num=test_number,scale=100)
		df = pd.concat([df_abs,df_100.iloc[:,1:]],axis=1)
		cols = [c for c in df.columns if re.search("Correct",c) is None]
		df = df.drop(cols,axis=1)

		self.__create_sheet(worksheet_name,["Student Name"],"Student Name")
		self._dfs[worksheet_name] = df

