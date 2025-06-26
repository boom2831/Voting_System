import random
def voter_id_generate():
    voter_id=''
    for _ in range(6):
        random_digits = random.randint(0, 9)
        voter_id+=str(random_digits)
    voter_id = "UTC"+voter_id
    return voter_id

print(f"Voter ID: '{voter_id_generate()}'")