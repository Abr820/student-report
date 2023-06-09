import gspread
import pandas as pd
import numpy as np
from gspread_dataframe import set_with_dataframe

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
		self.__create_sheet("Fundamental",["Mentors","Students","Subjects"])
		self.__create_sheet("Answers",["Qno","Answer","Tags"],index = "Qno")
		self.__create_sheet("Responses",["Student Name"],index = "Student Name")

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
			print("Dataframe to be saved : ")
			print(df.head())
			set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=include_index,include_column_header=True, resize=False)
			self._dfs[title] = None
			print(f"{title} is updated")

	def __add_elements(self,title,col,vals,unique = True, rearrange = True):
		df = self.__read_sheet(title)
		all_df = {}
		for c,dt in zip(df.columns,df.dtypes):
			value_list = [v for v in df[c].values.tolist() if v is not (None or np.nan) or not rearrange]
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
		l = [v for v in df[col_name].values.tolist() if v is not None and v != np.nan]
		print(l)
		return l

	def __add_row(self,title,data,replace = True):
		df = self.__read_sheet(title)
		indexx = self._indices[title]
		if not replace:
			idx = self.__find_row_index(df,indexx,data[0])
			data = df.loc[idx[0]].values.tolist() + data[1:]
		df = df.append(pd.Series(data, index=df.columns[:len(data)]), ignore_index=True)
		df = df.drop_duplicates(subset=[indexx],keep='last')
		self._dfs[title] = df

	def __add_value(self,title,row_name,col_name,value, index = None):
		df = self.__read_sheet(title)
		if index is None:
			index = self._indices[title]
		idx = self.__find_row_index(df,index,row_name)
		df.loc[idx,col_name] = value
		self._dfs[title] = df

	def __find_row_index(self,df,col_name,row_val):
		idx = df.index[df[col_name] == row_val].tolist()
		return idx[0]

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

	def write_all(self):
		for title in self.sheets:
			if self._dfs[title] is not None:
				self.__write_sheet(title,self._dfs[title])

	def add_answers(self, row_name , answers , tags):
		rows = [row_name+f"Q{i+1}" for i in range(len(answers))]
		for idx,ans,tag in zip(rows,answers,tags):
			self.__add_row("Answers",[idx,ans,tag],True)

	def add_student_response(self,sname,tname,answers):
		qnos = [tname+f"Q{i+1}" for i in range(len(answers))]
		for qno in qnos:
			self.__add_column("Responses",qno,[],'str')
		self.__add_elements("Responses","Student Name",[sname],unique = True)
		for qno,ans in zip(qnos,answers):
			self.__add_value("Responses",sname,qno,ans)
