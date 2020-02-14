CREATE TABLE Task_Group(
	Group_ID serial PRIMARY KEY NOT NULL,
	Group_Name VARCHAR(255) NOT NULL
);

CREATE TABLE Task(
	Task_Name VarChar(255) Primary Key NOT NULL,
	Group_ID integer NOT NULL,
	FOREIGN KEY (Group_ID) REFERENCES Task_Group(Group_ID)
	
);

CREATE TABLE event(
	Event_ID serial Primary Key NOT NULL,
	Task_Name VarChar(255) NOT NULL,
	Start_Time timestamp NOT NULL,
	End_Time timestamp NULL,
	Foreign Key (Task_Name) References Task(Task_Name)	
);

CREATE TABLE Cube (
	Cube_ID serial PRIMARY KEY NOT NULL
);

CREATE TABLE Side (
	Side_ID serial PRIMARY KEY NOT NULL,
	Cube_ID integer NOT NULL,
	Task_Name VARCHAR(255) NULL,
	FOREIGN KEY (Task_Name) REFERENCES Task(Task_Name),
	Foreign KEY (Cube_ID) REFERENCES Cube(Cube_ID)
);