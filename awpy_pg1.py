deaths = [1,3,4,6,10,11,17,18,20,21]

for i in range(0,21):
    if i+1 in deaths:
        print(f'player died on round {i+1}')
    else:
        print(f'player did not die on round {i+1}')
