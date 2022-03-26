#!/bin/python3
#makeCSV.py
#read saldump database and create some limited csv files for use in data mining
#Daniel Gysi CIS-241 Data Mining September 15, 2020

#imports
import sqlite3 #for querying the database
import csv #for writing to csv files. (sign data has unicode characters i'm gonna kms)
import time as Time #for converting epoch time to something readable

#Queries
block_break_query = """
        SELECT co_block.time, co_user.user, co_material_map.material,
            co_world.world, co_block.x, co_block.y, co_block.z            
        FROM co_block INNER JOIN co_material_map
	ON co_block.type == co_material_map.id
        INNER JOIN co_user ON co_block.user == co_user.id
        INNER JOIN co_world ON co_block.wid == co_world.id
        WHERE uuid IS NOT NULL AND action == 0 LIMIT 1000000;"""   #we can't query everything so I'm taking the first million. It's indexed by time.
block_place_query = """
        SELECT co_block.time, co_user.user, co_material_map.material,
            co_world.world, co_block.x, co_block.y, co_block.z            
        FROM co_block INNER JOIN co_material_map
	ON co_block.type == co_material_map.id
        INNER JOIN co_user ON co_block.user == co_user.id
        INNER JOIN co_world ON co_block.wid == co_world.id
        WHERE uuid IS NOT NULL AND action == 1 LIMIT 1000000;""" #we can't query everything so I'm taking the first million. It's indexed by time. 
sign_query = """
        SELECT co_sign.time, co_user.user,
            co_sign.line_1, co_sign.line_2, co_sign.line_3, co_sign.line_4,
            co_world.world, co_sign.x, co_sign.y, co_sign.z            
        FROM co_sign INNER JOIN co_user
            ON co_sign.user == co_user.id
        INNER JOIN co_world
            ON co_sign.wid == co_world.id
        WHERE uuid IS NOT NULL AND
        NOT(co_sign.line_1 IS NULL AND
            co_sign.line_2 IS NULL AND
            co_sign.line_3 IS NULL AND
            co_sign.line_4 IS NULL);""" #remove blank signs
session_query = """
        SELECT co_session.time, co_user.user, co_session.action,
            co_world.world, co_session.x, co_session.y, co_session.z            
        FROM co_session INNER JOIN co_user
            ON co_session.user == co_user.id
        INNER JOIN co_world
            ON co_session.wid == co_world.id
        WHERE uuid IS NOT NULL;"""


#query the database
DB_URL = "F:\\salDump\\database.db"
OUTPUT_URL = "F:\\salDump\\CSV\\"
database = sqlite3.connect(DB_URL);
print("db connected");

cursor = database.cursor();

#block break
cursor.execute(block_break_query); #execute query
print("Block break query executed.");

block_break = cursor.fetchall();

with open(OUTPUT_URL + "block_break.csv", "w") as bb_file: #open output file
    print("\nWriting to block break csv.")
    linesWritten = 0;
    bb_writer = csv.writer(bb_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    bb_writer.writerow(["time", "user", "block", "world", "x", "y", "z"]) #write labels

    #write lines from query
    for line in block_break:
        time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(line[0]))
        user = line[1]
        block = line[2][10:]
        world = line[3]
        x = line[4]
        y = line[5]
        z = line[6]
        
        bb_writer.writerow([time, user, block, world, x, y, z])

        #progress update
        linesWritten += 1;
        if linesWritten % 1000 == 0:
            print(str(linesWritten) + " lines written so far.");

    print("Block break file written.")

    
#block place
cursor.execute(block_place_query); #execute query
print("\nBlock place query executed.");

block_place = cursor.fetchall();
with open(OUTPUT_URL + "block_place.csv", "w") as bp_file: #open output file
    print("\nWriting to block place csv.")
    linesWritten = 0;
    bp_writer = csv.writer(bp_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    bp_writer.writerow(["time", "user", "block", "world", "x", "y", "z"]) #write labels

    #write lines from query
    for line in block_place:
        time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(line[0]))
        user = line[1]
        block = line[2][10:]
        world = line[3]
        x = line[4]
        y = line[5]
        z = line[6]
        
        bp_writer.writerow([time, user, block, world, x, y, z])

        #progress update
        linesWritten += 1;
        if linesWritten % 1000 == 0:
            print(str(linesWritten) + " lines written so far.");
            
    print("Block place file written.");


#sign data
cursor.execute(sign_query); #execute query
print("\nSign query executed.");

sign_data = cursor.fetchall();
with open(OUTPUT_URL + "sign.csv", "w") as sg_file: #open output file
    print("\nWriting to sign csv.")
    linesWritten = 0;
    notWritten = 0;
    sg_writer = csv.writer(sg_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    sg_writer.writerow(["time", "user", "text", "world", "x", "y", "z"]) #write labels

    #write lines from query
    for line in sign_data:
        time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(line[0]))
        user = line[1]
        text = line[2] + " " + line[3] + " " + line[4] + " " + line[5] #combine all 4 lines into a single string
        world = line[6]
        x = line[7]
        y = line[8]
        z = line[9]

        #exception handled for non-standard characters.
        #I don't have the willpower to get within a thousand yards of unicode encoding atm.
        #Ask me again in 2 weeks. I've done it before but it was the biggest pain of my life
        #This is due in 12 hours. 
        try:
            sg_writer.writerow([time, user, text, world, x, y, z])
        except:
            notWritten += 1;

        #progress update
        linesWritten += 1;
        if linesWritten % 1000 == 0:
            print(str(linesWritten) + " lines written so far.");
            
    print("Sign file written.");
    print(str(notWritten) + " lines omitted due to unicode character usage.");


#session data
cursor.execute(session_query); #execute query
print("\nSession query executed.");

session_data = cursor.fetchall();
with open(OUTPUT_URL + "session.csv", "w") as ss_file: #open output file
    print("\nWriting to sesssion csv.")
    linesWritten = 0;
    ss_writer = csv.writer(ss_file, delimiter=',', quotechar='"', lineterminator='\n', quoting=csv.QUOTE_MINIMAL)
    ss_writer.writerow(["time", "user", "action", "world", "x", "y", "z"]) #write labels

    #write lines from query
    for line in session_data:
        time = Time.strftime('%Y-%m-%d %H:%M:%S', Time.localtime(line[0]))
        user = line[1]
        action = line[2]
        world = line[3]
        x = line[4]
        y = line[5]
        z = line[6]
        
        ss_writer.writerow([time, user, action, world, x, y, z])

        #progress update
        linesWritten += 1;
        if linesWritten % 1000 == 0:
            print(str(linesWritten) + " lines written so far.");
            
    print("Session file written.");

