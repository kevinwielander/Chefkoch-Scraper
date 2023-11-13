from german_lemmatizer import lemmatize

senetence= lemmatize(
    ['guter'],
    working_dir='*',
    chunk_size=10000,
    n_jobs=-1,
    escape=False,
    remove_stop=False)

for x in senetence:
    print(x)