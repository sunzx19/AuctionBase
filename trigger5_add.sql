--Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.
PRAGMA foreign_keys = ON;
drop trigger if exists must_higher_bid;
create trigger must_higher_bid
before insert on Bid
for each row
when exists (
        Select * 
        from Item i
        where i.ItemID=new.ItemID and (i.Currently>=new.Amount) 
    	)
begin
  select raise(rollback, 'Any new bid for a particular item must have a higher amount than any of the previous bids for that particular item.');
end;