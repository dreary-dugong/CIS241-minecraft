#Move serailized entities from database into binary files to be deserialized by Java


import sqlite3
database = "F:\\salDump\\database.db" #database location
output = "E:\\Documents\\College\\2020 Fall Semester\\CIS 241 - Intro to Data Mining\\minecraft project\\entities" #output location for binary files

#pull entites from database
query = ("""SELECT data FROM co_entity
            LIMIT 500;""");

connection = sqlite3.connect(database)
cursor = connection.cursor()
cursor.execute(query)

rawEntities = [entityTuple[0] for entityTuple in cursor.fetchall()]

cursor.close()
connection.close()


#put entites in files
for i in range(len(rawEntities)):
    with open(output + "\\" + str(i), "wb") as file:
        file.write(rawEntities[i])

print("Wrote files.");
