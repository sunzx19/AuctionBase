--All new bids must be placed at the time which matches the current time of your AuctionBase system.
PRAGMA foreign_keys = ON;
drop trigger if exists bidTime_equal_to_currentTime;
create trigger bidTime_equal_to_currentTime
before insert on Bid
for each row
when exists (
        Select * 
        from CurrentTime c
        where c.Curr_Time <> new.Time 
    	)
begin
  select raise(rollback, 'All new bids must be placed at the time which matches the current time of your AuctionBase system.');
end;