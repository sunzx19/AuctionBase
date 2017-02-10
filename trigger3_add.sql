--No auction may have a bid before its start time or after its end time.
PRAGMA foreign_keys = ON;
drop trigger if exists no_bid_out_time_range;
create trigger no_bid_out_time_range
before insert on Bid
for each row
when exists (
        Select * 
        from Item i
        where i.ItemID=new.ItemID and (i.Started>new.Time or i.Ends<new.Time) 
    	)
begin
  select raise(rollback, 'No auction may have a bid before its start time or after its end time.');
end;