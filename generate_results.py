from random import randint

for user in range(1, 6):
    for assessment in range(1, 17):
        print(f'({user}, {assessment}, {randint(0,4)}),')
