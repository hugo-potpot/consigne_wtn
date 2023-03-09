from src.Starter import Starter


def users_to_insert():
    """
    Gets the users to insert.
    :return: The users to insert.
    """

    return [
        {
            "id": 218810179590815744,
            "name": "Potpot",
        }
    ]

def insertions(clear=False):
    """
    Inserts data into the database.
    :param clear: If True, clears the database before inserting.
    :return: None
    """
    starter = Starter()

    if clear:
        starter.database.clear()

    users = users_to_insert()
    for user in users:
        starter.database.add_user(user["id"], user["name"])

if __name__ == "__main__":
    insertions(clear=True)