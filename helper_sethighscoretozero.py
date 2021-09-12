import pickle

with open('./Pacman/highscore.txt', 'wb') as file:
    pickle.dump(0, file)