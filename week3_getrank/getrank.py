import sys
from pymongo import MongoClient


def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    contests_items = contests.find()

    contests_dict = {}
    for item in contests_items:
        list_temp = []

        score = item['score']
        submit_time = item['submit_time']
        if contests_dict.get(item['user_id']):
            score = score + int(contests_dict[item['user_id']][1])
            submit_time = submit_time + int(contests_dict[item['user_id']][2])
        list_temp.append(1)
        list_temp.append(score)
        list_temp.append(submit_time)
        contests_dict[item['user_id']] = list_temp

    for key, value in contests_dict.items():
        for key1, value1 in contests_dict.items():
            if key == key1:
                continue
            if value[1] < value1[1]:
                value[0] += 1
            elif value[1] == value1[1]:
                if value[2] < value1[2]:
                    value[0] += 1

    rank, score, submit_time = (x for x in contests_dict[user_id])
    return rank, score, submit_time


if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError
        if not sys.argv[1].isdigit():
            raise ValueError

    except ValueError:
        print("Parameter Error")
        sys.exit(1)

    user_id = int(sys.argv[1])
    userdata = get_rank(user_id)

    print("({}, {}, {})".format(userdata[0], userdata[1], userdata[2]))
