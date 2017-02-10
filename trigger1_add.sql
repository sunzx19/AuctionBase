--The Current Price of an item must always match the Amount of the most recent bid for that item.
PRAGMA foreign_keys = ON;
drop trigger if exists update_currently;
create trigger update_currently
after insert on Bid
for each row
begin
  update Item set Currently = new.Amount 
  where ItemID = new.ItemID;
end;