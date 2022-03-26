Daniel Gysi
Dr. Hallenbeck
CIS-241 Data Mining
15 September 2020

Because the original database is so large, I chose not to
include it in my submission. You can access it with the
following link, or if you like I can bring you a hard drive
with the database on it.
https://salc1.com/downloads.html

Because of the size of the co_block table, I chose to only
take the first 1,000,000 places and breaks respectively
as a representative sample. Every other table I extracted
from was able to be taken in its entirety.

I did some data cleansing in R, but the vast majority was
done in SQL and Python. The makeCSV.py file contains the
script I used to read the data from the database and write
it to CSV files. Things to note about that script:
- many columns in the tables were ignored or replaced with 
  inner joins
- I ignored all block placements/breaks done by the server
  rather than by a player (uuid IS NOT NULL)
- I ignored all signs with unicode text. This was a hard
  decision and I might go back and fix it if I get the 
  time, but it was just too hard to deal with in python.
  That's 924 signs with text I don't have now though.
- For the time being I'm entirely ignoring entities and
  entity kills. If I get the time I might decide
  to add those back in. I'll message the plugin dev
  and see if he'll help me out with understanding the db.
