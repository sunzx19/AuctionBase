--Constraint 1
select * from User u1, User u2 where u1.UserID=u2.UserID and (u1.Rating <> u2.Rating);
--Constraint 2
select SellerID from Item where SellerID not in (select UserID from User);
select UserID as BIdderID from Bid where UserID not in (select UserID from User);
--Constraint 3
select * from Item i1, Item i2 where i1.ItemID=i2.ItemID and i1.Name <> i2.Name;
--Constraint 4
select ItemID from Bid where ItemID not in(select ItemID from Item);
--Constraint 5
select ItemID from Category where ItemID not in(select ItemID from Item);
--Constraint 6
select * from Category group by ItemID,Category having count(*)>1;
--Constraint 7
select * from Item where Ends<=Started;
--Constraint 8
select * from Item i where Currently <> (select Amount from Bid b where b.ItemID=i.ItemID and b.Time=(select max(Time) from Bid b1 where b1.ItemID=b.ItemID group by b1.ItemID));
--Constraint 9
select i.SellerID from Item i, Bid b where i.ItemID=b.ItemID and i.SellerID=b.UserID;
--Constraint 10
select * from Bid group by ItemID,Time having count(*)>1;
--Constraint 11
select i.ItemID from Item i, Bid b where i.ItemID=b.ItemID and (b.Time<i.Started or b.Time>i.Ends);
--Constraint 12
select * from Bid group by ItemID,UserID,Amount having count(*)>1;
--Constraint 13
select * from Item i, Bid b where i.ItemID=b.ItemID and i.Number_of_Bids <>(select count(*) from Bid where i.ItemID=ItemID);
--Constraint 14
select * from Bid b1, Bid b2 where b1.ItemID=b2.ItemID and b2.Time>b1.Time and b2.Amount<=b1.Amount;
--Constraint 15,16
--No need to check initial values