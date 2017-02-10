--A user may not bid on an item he or she is also selling.
PRAGMA foreign_keys = ON;
drop trigger if exists no_bid_as_seller;
create trigger no_bid_as_seller
before insert on Bid
for each row
when exists (
        Select * 
        from Item i
        where i.ItemID=new.ItemID and i.SellerID= new.UserID 
        )
begin
  select raise(rollback, 'A user may not bid on an item he or she is also selling.');
end;