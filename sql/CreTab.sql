


CREATE TABLE Cube (
	Cube_ID serial PRIMARY KEY NOT NULL,
	username VARCHAR(150) not null,
	FOREIGN KEY(username) REFERENCES auth_user(username)
);

CREATE TABLE Task(
	Task_Id serial PRIMARY KEY NOT NULL,
	Task_Name VarChar(255) NOT NULL,
	Group_name VarChar(255) NOT NULL,
	Cube_Id integer NULL,
	username VarChar(150) NOT NULL,
	UNIQUE (Task_Name, Group_Name, username),
	Foreign Key(Cube_Id) REFERENCES Cube(Cube_ID),
	Foreign Key(username) REFERENCES auth_user(username)

);

CREATE TABLE event(
	Event_ID serial Primary Key NOT NULL,
	Task_Id INTEGER NOT NULL,
	Start_Time timestamp NOT NULL,
	End_Time timestamp NULL,
	Foreign Key (Task_Id) References Task(Task_Id)
);

CREATE TABLE Side (
	Side_ID integer NOT NULL,
	Cube_Id integer NOT NULL,
	Task_Id INTEGER not null,
	PRIMARY KEY (Side_ID,Cube_Id),
	FOREIGN KEY (Cube_Id) REFERENCES Cube(Cube_ID),
	FOREIGN KEY (Task_Id) REFERENCES Task(Task_Id)
);
