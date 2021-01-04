from collections import defaultdict

min_user = 3
min_item = 10

# shared users between book domain and movie domain

nUser = 0
userIds = defaultdict(int)
rUserIds = defaultdict(str)

############BOOK##################

nItem = 0
itemIds = defaultdict(int)
rItemIds = defaultdict(str)
user_books = defaultdict(set)
book_users = defaultdict(set)
total = 0
with open('rat45_book_sharemovie.txt') as ifile:
    for line in ifile:
        if not line or line == '':
            continue
        line = line.split(' ')
        user = line[0]
        if user not in userIds:
            userIds[user] = nUser
            rUserIds[nUser] = user
            nUser += 1
        item = line[1]
        if item not in itemIds:
            itemIds[item] = nItem
            rItemIds[nItem] = item
            nItem += 1
        user_books[userIds[user]].add(itemIds[item])
        book_users[itemIds[item]].add(userIds[user])
        total += 1
print('#rats (book, before) = {}'.format(total))
with open('user_id_maps.bookmovie.txt', 'w', encoding='utf-8') as ofile:
    for user, uid in userIds.items():
        ofile.write(user + ' ' + str(uid))
with open('book_id_maps.txt', 'w', encoding='utf-8') as ofile:
    for item, iid in itemIds.items():
        ofile.write(item + ' ' + str(iid))

users_filter_book = set()
total = 0
for user, books in user_books.items():
    if len(books) < min_user:
        continue
    cands = []
    for book in books:
        if len(book_users[book]) < min_item:
            continue
        cands.append(book)
    if len(cands) == 0:
        continue
    total += len(cands)
    users_filter_book.add(user)
print('#rats (book, after) = {}'.format(total))
print('#users_filter = {}'.format(len(users_filter_book)))

##########MOVIE#################

nItem = 0
itemIds = defaultdict(int)
rItemIds = defaultdict(str)
user_movies = defaultdict(set)
movie_users = defaultdict(set)
total = 0
with open('rat45_movie_sharebook.txt') as ifile:
    for line in ifile:
        if not line or line == '':
            continue
        line = line.split(' ')
        user = line[0]
        item = line[1]
        if item not in itemIds:
            itemIds[item] = nItem
            rItemIds[nItem] = item
            nItem += 1
        user_movies[userIds[user]].add(itemIds[item])
        movie_users[itemIds[item]].add(userIds[user])
        total += 1
print('#rats (movie, before) = {}'.format(total))
with open('movie_id_maps.txt', 'w', encoding='utf-8') as ofile:
    for item, iid in itemIds.items():
        ofile.write(item + ' ' + str(iid))

total = 0
users_filter_movie = set()
for user, movies in user_movies.items():
    if len(movies) < min_user:
        continue
    cands = []
    for movie in movies:
        if len(movie_users[movie]) < min_item:
            continue
        cands.append(movie)
    if len(cands) == 0:
        continue
    total += len(cands)
    users_filter_movie.add(user)
print('#rats (movie, after) = {}'.format(total))
print('#users_filter = {}'.format(len(users_filter_movie)))

############shared##################

users_filter_shared = users_filter_movie.intersection(users_filter_book)
print('#users_filter_shared = {}'.format(len(users_filter_shared)))
users_filter_shared = [u for u in users_filter_shared]
users_filter_shared = sorted(users_filter_shared)

total = 0
with open('book_u'+str(min_user) + 'i'+str(min_item) + '.dat', 'w', encoding='utf-8') as ofile:
    for user in  users_filter_shared:
        books = user_books[user]
        if len(books) < min_user:
            continue
        cands = []
        for book in books:
            if len(book_users[book]) < min_item:
                continue
            cands.append(book)
        if len(cands) == 0:
            continue
        ofile.write(str(user) + ' ' + str(len(cands)) + ' ' + ' '.join([str(i) for i in cands]) + '\n')
        total += len(cands)
        users_filter_book.add(user)
print('#rats (book, shared) = {}'.format(total))
print('wrote book')

total = 0
with open('movie_u'+str(min_user) + 'i'+str(min_item) + '.dat', 'w', encoding='utf-8') as ofile:
    for user in users_filter_shared:
        movies = user_movies[user]
        if len(movies) < min_user:
            continue
        cands = []
        for movie in movies:
            if len(movie_users[movie]) < min_item:
                continue
            cands.append(movie)
        if len(cands) == 0:
            continue
        ofile.write(str(user) + ' ' + str(len(cands)) + ' ' + ' '.join([str(i) for i in cands]) + '\n')
        total += len(cands)
        users_filter_movie.add(user)
print('#rats (movie, shared) = {}'.format(total))
print('wrote movie')
