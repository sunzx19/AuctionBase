drop table if exists Item;
drop table if exists User;
drop table if exists Bid;
drop table if exists Category;

create table User(
	UserID text,
	Rating float,
	Location text,
	Country text,
	PRIMARY KEY(UserID)
);
create table Item(
	ItemID int,
	Name text,
	Currently float,
	Buy_Price float,
	First_Bid float,
	Number_of_Bids int,
	Started NUMERIC,
	Ends NUMERIC check(Ends>Started),
	SellerID text,
	Description text,
	PRIMARY KEY(ItemID),
	FOREIGN KEY(SellerID) references User
);
create table Bid(
	ItemID int,
	UserID text,
	Time NUMERIC,
	Amount float,
	UNIQUE(ItemID, Time),
	UNIQUE(ItemID, UserID, Amount),
	FOREIGN KEY(ItemID) references Item,
	FOREIGN KEY(UserID) references User
);
create table Category(
	ItemID int,
	Category text,
	PRIMARY KEY(ItemID,Category),
	FOREIGN KEY(ItemID) references Item
);

DROP TABLE if exists CurrentTime ;
CREATE TABLE CurrentTime (Curr_Time NUMERIC primary key) ;
INSERT into CurrentTime values ('2001-12-20 00:00:01') ;
SELECT * from CurrentTime ;