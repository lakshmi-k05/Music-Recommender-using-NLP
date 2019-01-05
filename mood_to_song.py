from score_songs import score

def choose_song(mood):
    lib_score = score()
    ind = 0
    min = 5
    for song in lib_score:
        song_score = lib_score[song]        #stores ordered pair of moods
        happy_diff = mood[0] - song_score[0]
        excite_diff = mood[1] - song_score[1]
        happy_diff = abs(happy_diff)
        excite_diff = abs(excite_diff)
        avg_diff = (happy_diff + excite_diff)/2

        if avg_diff < min:
            min = avg_diff
            ans = song
        ind = ind + 1
    print ('Listening to', ans,'......')
    exit(0)


