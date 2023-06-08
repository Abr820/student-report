import gspread
import pandas as pd
import numpy as np
from gspread_dataframe import set_with_dataframe

class Acadomate:
	def __init__(self, cred_file = "acadomate-report-7028d1340299.json",sheet_name = "Acadomate Report"):
		self.gc = gspread.service_account(filename= cred_file)
		try:
			self.sh = self.gc.open(sheet_name)
			print("Spreadsheet exists")
		except SpreadsheetNotFound:
			print("Spreadsheet doesn't exist")
		self.sheets = [ws.title for ws in self.sh.worksheets()]
		self.dfs = {}
		self.indices = {}
		for title in self.sheets:
			self.dfs[title] = None
			self.indices[title] = None
		self._create_sheet("Fundamental",["Mentors","Students","Subjects"])
		self._create_sheet("Answers",["Qno","Answer","Tags"],index = "Qno")

	def _create_sheet(self, title , columns , index = None):
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
			self._write_sheet(title,df)
			print(f"Column names {columns} added")

		if index is not None and index in values_list:
			self.indices[title] = index
			print(f"{index} is added as index of sheet {title}")
		print(self.indices)

	def _read_sheet(self,title):
		if title not in self.sheets:
			print("{title} sheet doesn't exist in the given spreadsheet")
			return None
		else:
			if self.dfs[title] is not None:
				return self.dfs[title]

			worksheet = self.sh.worksheet(title)
			columns = worksheet.row_values(1)
			df = pd.DataFrame(worksheet.get_all_records(),columns=columns)
			df = df.replace({'': None})

			# index = self.indices[title]
			# if index is not None and index in df.columns:
			# 	df = df.set_index(index)
			# 	print(f"{index} is set as index")

			print("Dataframe read : ")
			print(df.head())
			self.dfs[title] = df
			return df

	def _write_sheet(self,title,df, include_index = False):
		if title not in self.sheets:
			print("{title} sheet doesn't exist in the given spreadsheet")
		else:
			worksheet = self.sh.worksheet(title)
			worksheet.clear()
			df = df.fillna("")
			print("Dataframe to be saved : ")
			print(df.head())
			set_with_dataframe(worksheet=worksheet, dataframe=df, include_index=include_index,include_column_header=True, resize=False)
			self.dfs[title] = None
			print(f"{title} is updated")

	def _add_element(self,title,col,vals,unique = True, rearrange = True):
		df = self._read_sheet(title)
		all_df = {}
		for c,dt in zip(df.columns,df.dtypes):
			value_list = [v for v in df[c].values.tolist() if v is not (None or np.nan) or not rearrange]
			if c == col:
				for v in vals:
					if not unique or (unique and v not in value_list):
						value_list.append(v)
			all_df[c] = pd.Series(value_list,dtype=dt)
		print(all_df)
		df = pd.DataFrame(all_df,columns=df.columns)
		self.dfs[title] = df

	def _add_column(self,title,col_name,data, dtype):
		df = self._read_sheet(title)
		if col_name not in df.columns:
			add_df = pd.DataFrame(pd.Series(data,dtype=dtype),columns=[col_name])
			df = pd.concat([df,add_df],axis=1)
			self.dfs[title] = df
		else:
			self._add_element(title,col_name,data,unique=True)

	def _get_column(self,title,col_name):
		df = self._read_sheet(title)
		return [v for v in df[col_name].values.tolist() if v is not None and v != np.nan]

	def _add_row(self,title,data):
		df = self._read_sheet(title)
		index = self.indices[title]
		df = df.append(pd.Series(data, index=df.columns[:len(data)]), ignore_index=True)
		df = df.drop_duplicates(subset=[index],keep='last')
		self.dfs[title] = df


	def add_mentors(self,names):
		self._add_element("Fundamental","Mentors",names,unique=True)

	def add_students(self,names):
		self._add_element("Fundamental","Students",names,unique=True)

	def add_subjects(self,names):
		self._add_element("Fundamental","Subjects",names,unique=True)
		for name in names:
			self._add_column("Fundamental",name+" Topics",[],'str')

	def get_subjects(self):
		return self._get_column("Fundamental","Subjects")

	def add_topics(self,sub_name,topic_names):
		self._add_element("Fundamental",sub_name+" Topics",topic_names,unique=True,rearrange = True)

	def get_topics(self,sub):
		return self._get_column("Fundamental",sub+" Topics")

	def write_all(self):
		for title in self.sheets:
			if self.dfs[title] is not None:
				self._write_sheet(title,self.dfs[title])

	def add_answers(self, row_name , answers , tags):
		rows = [row_name+f"Q{i+1}" for i in range(len(answers))]
		for idx,ans,tag in zip(rows,answers,tags):
			self._add_row("Answers",[idx,ans,tag])
