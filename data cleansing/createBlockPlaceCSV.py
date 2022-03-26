#Move serailized entities from database into binary files to be deserialized by Java


import sqlite3
database = "F:\\salDump\\database.db" #database location
output = "F:\\salDump\\" #output location for binary files

#pull entites from database
query = ("""SELECT x, z FROM co_block
            INNER JOIN co_user ON
            co_block.user = co_user.id
            WHERE action == 1
            AND wid == 1
            AND uuid IS NOT NULL
            LIMIT 1000;""");

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
