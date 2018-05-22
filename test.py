import sqlite3, csv
import random

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()
# artist_map = {}
# GENRE_CHOICES = (
# 	(1, 'Rock'),
# 	(2, 'Hip-hop'),
# 	(3, 'Pop'),
# 	(4, 'Metal'),
# 	(5, 'Jazz'),
# )
choices = [1, 2, 3, 4 ,5]

cursor.execute("SELECT * FROM music_song WHERE id > 48 order by id")
select = cursor.fetchall()
# print '---------------------------------------------------------------------------'
# print select
for song in select:
	genre = random.choice(choices)
	cursor.execute("UPDATE music_song SET genre=%s where id = %s" % (genre, song[0]))
	conn.commit()



# with open('music.csv') as csvfile:
# 	reader = csv.DictReader(csvfile)

	# INSERT ARTISTS
	# for row in reader:

	# 	to_db=(row['artist.id'], row['artist.name'])
	# 	cursor.executemany("insert into music_artist(source_id, name) values(?,?)", [to_db])
	# 	conn.commit()

		


	#mapping




	# for artist in select:
	# 	artist_map[artist[1]] = artist[0]
	# artist = 0;
	# for row in reader:
	# 	for key, value in artist_map.iteritems():
	# 		if row['artist.id'] == key:
	# 			artist = value
	# 			
	# 			to_db = (artist, genre, row['title'], row['tempo'])
	# 			cursor.executemany("insert into music_song(artist_id, genre, song_title, tempo, creator_id) values(?, ?, ? ,?, 1);", [to_db])
	# 			conn.commit()
	# 		else:
	# 			continue
			
