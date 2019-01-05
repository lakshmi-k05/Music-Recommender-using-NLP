import init_music

def initialise(sentence):
    sentence = sentence.lower()
    song_dict = init_music.init_music()
    #print (song_dict)
    check_song_name(sentence, song_dict)

def check_song_name(sentence, song_dict):
    sentence = sentence.split()
    name = sentence[1:]
    n = len(name)
    flag = True
    for song_det in song_dict:
        input_name = ""
        for i in range(0, n):
            if i == 0:
                input_name = input_name + str(name[i])
            else:
                input_name = input_name + " " + str(name[i])
            if input_name in song_det:
                flag = False
                break
        if not flag:
            break

    if not flag:
        play_song(input_name, song_det[input_name], song_dict)

def play_song(name, type, song_dict):
    if type == 'name':
        print('Playing song', name, "......")
        exit(0)
    else:
        print ('Choose song.....\n')
        for song in song_dict:
            if name in song:
                print (song)
        exit(0)