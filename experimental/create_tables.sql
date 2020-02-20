CREATE TABLE User(
    User_ID VarChar(255) PRIMARY KEY NOT NULL,
    User_Name VarChar(255) NOT NULL
);

CREATE TABLE Cube(
	Cube_ID serial PRIMARY KEY NOT NULL,
    Side_Count Integer NOT NULL,
    User_ID Integer NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Task(
    Task_ID serial PRIMARY KEY NOT NULL,
	Task_Name VarChar(255) NOT NULL,
	User_ID Integer NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Group(
    Group_ID serial PRIMARY KEY NOT NULL,
    Group_Name VarChar(255) NOT NULL,
    User_ID Integer NOT NULL,
    FOREIGN KEY (User_ID) REFERENCES User(User_ID)
);

CREATE TABLE Side(
	Side_Number Integer NOT NULL,
	Cube_ID Integer NOT NULL,
	Task_ID Integer NULL,
	Group_ID Integer NULL,
    PRIMARY KEY (Side_Number, Cube_ID),
	FOREIGN KEY (Cube_ID) REFERENCES Cube(Cube_ID),
    FOREIGN KEY (Task_ID) REFERENCES Task(Task_ID),
    FOREIGN KEY (Group_ID) REFERENCES Group(Group_ID)
);

CREATE TABLE Event(
	Event_ID serial PRIMARY KEY NOT NULL,
    Cube_ID Integer NOT NULL,
	Task_ID Integer NOT NULL,
	Group_ID Integer NOT NULL,
	Start_Time Timestamp NOT NULL,
	End_Time Timestamp NULL,
	FOREIGN KEY (Cube_ID) REFERENCES Cube(Cube_ID),
    FOREIGN KEY (Task_ID) REFERENCES Task(Task_ID),
    FOREIGN KEY (Group_ID) REFERENCES Group(Group_ID)
);