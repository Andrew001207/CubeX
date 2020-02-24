


CREATE TABLE Cube (
	Cube_ID serial PRIMARY KEY NOT NULL,
	username varchar(150) not null,
	foreign key username references auth_user(username)
);

CREATE TABLE Task(
    task_id serial primary key not null,
	Task_Name VarChar(255) NOT NULL,
	Group_name VarChar(255) NOT NULL,
	Cube_Id integer NULL,
	username Varchar(150) not null,
	Foreign Key(Cube_Id) REFERENCES Cube(Cube_ID),
	foreign key(username) references auth_user(username),
	unique (Task_Name,Group_name,username)
	
);

CREATE TABLE event(
	Event_ID serial Primary Key NOT NULL,
	task_id integer not null,
	Start_Time timestamp NOT NULL,
	End_Time timestamp NULL,
	Foreign Key (task_id) References Task(task_id)
);

CREATE TABLE Side (
	Side_ID integer PRIMARY KEY NOT NULL,
	task_id integer not null,
	FOREIGN KEY (task_id) REFERENCES Task(task_id)
);
