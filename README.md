# AuctionBase
An auction system.

Website: http://web.stanford.edu/~zhenxuan/cgi-bin/auctionbase.py/currtime

Constraints for Users
1. No two users can share the same User ID.
2. All sellers and bidders must already exist as users.
Constraints for Items
3. No two items can share the same Item ID.
4. Every bid must correspond to an actual item.
5. The items for a given category must all exist.
6. An item cannot belong to a particular category more than once.
7. The end time for an auction must always be after its start time.
8. The Current Price of an item must always match the Amount of the most recent bid for that item.
Constraints for Bidding
9. A user may not bid on an item he or she is also selling.
10. No auction may have two bids at the exact same time.
11. No auction may have a bid before its start time or after its end time.
12. No user can make a bid of the same amount to the same item more than once.
13. In every auction, the Number of Bids attribute corresponds to the actual number of bids for that particular
item.
14. Any new bid for a particular item must have a higher amount than any of the previous bids for that particular
item.
Constraints for Time
15. All new bids must be placed at the time which matches the current time of your AuctionBase system.
16. The current time of your AuctionBase system can only advance forward in time, not backward in time.
