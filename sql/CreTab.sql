CREATE TABLE Task(
	Task_Name VarChar(255) Primary Key NOT NULL,
	Task_Group VarChar(255) NOT NULL
);

CREATE TABLE event(
	EventID serial Primary Key NOT NULL,
	Task_Name VarChar(255) NOT NULL,
	Start_Time timestamp NOT NULL,
	End_Time timestamp NOT NULL,
	Foreign Key (Task_Name) References Task(Task_Name)	
);