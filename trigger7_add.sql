--The current time of your AuctionBase system can only advance forward in time, not backward in time.
drop trigger if exists must_later_time;
create trigger must_later_time
before update on CurrentTime
for each row
when new.Curr_Time<old.Curr_Time
begin
  select raise(rollback, 'The current time of your AuctionBase system can only advance forward in time, not backward in time.');
end;