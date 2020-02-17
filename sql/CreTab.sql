
CREATE TABLE Task(
	Task_Name VarChar(255) NOT NULL,
	Group_name VarChar(255) NOT NULL,
	Cube_Id integer NOT NULL
	Primary KEY (Group_name, Task_Name, Cube_ID)
	
);

CREATE TABLE Cube (
	Cube_ID serial PRIMARY KEY NOT NULL
);

CREATE TABLE event(
	Event_ID serial Primary Key NOT NULL,
	Task_Name VarChar(255) NOT NULL,
	Group_Name VarChar (255) NOT NULL,
    Cube_ID integer Not NULL,
	Start_Time timestamp NOT NULL,
	End_Time timestamp NULL,
	Foreign Key (Task_Name, Group_Name, Cube_ID) References Task(Task_Name, Group_Name, Cube_ID),
	FOREIGN KEY (Cube_ID) REFERENCES Cube(Cube_ID)
);

CREATE TABLE Side (
	Side_ID integer PRIMARY KEY NOT NULL,
	Cube_ID integer NOT NULL,
	Task_Name VARCHAR(255) NULL,
	Group_Name varchar(255) NOT Null,
	FOREIGN KEY (Task_Name, Group_Name, Cube_ID) REFERENCES Task(Task_Name, Group_Name, Cube_ID),
	Foreign KEY (Cube_ID) REFERENCES Cube(Cube_ID)
);
