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
            "token": "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..4FuJDiYk6YVY56ir.iFjpUma4Ry4QJUEOOZTCzBLFTn-cRHcUtQZaBsgbd97pjo_HpgZdK8AEMK9lv1VMH8SGbay8Iu4BKBkWMSqy8O0k1vJCAko4D9Y0x8vXb2k1dgSZ8UmkRdKYaoSYkV-d_W7_sK0ax237AYRMIRpyHORGkE8oXHX_6zikOnr4mQGrwx6z98Hl5f_tcwJq9IcotVK3NZ2UVHD0YCykym77zr4I00BueCW_juXt7TNFoucw57JwMQN1wVH0EkwXtSoqpBrxo8FMRexLJqpJdKcrYWj-AxZaQTzoniVSukX9kKZn_hSsfFQaY68bYbHnzNmEmwM83q7xskw216dFSmdlkReceEph5P_hTZ_A_z6eplS31OeQAewNbDJYILSsxdamDw6ux3qinFAgKtwFvvLMBpNSqC2Yqz2FIzLnHRgqCMXaX85RSUvWTCjNFb9DMpAgiH1ZwKr3aGJOap7x-yr-GomqTgvWFhgBPSc7yz_rD3jBfjywob-sSvam83FOQODaYy5_DThi4nEGc2ibJaUJLJJH58_Diwn_28ipjbcswwG3cIHQ9Vd6Lse31SSanKYNpRvlcDwVX3yONKjzSuuWaMzCZdSkPnS0qZ26HzH29r-BVvxrRRCpxdswRPiVONqf9OoRDebuFKkuJ6XBPxbia_3F7FWbP0qkjbatwSo2HoQ_eKcHju5fYcTsHwkEzlQGOJQd5ZaU39qtbVS_FFyNJF4LWnRUIlzZaKqQuMFgla66gHxhvXIqoc5hALlukW5Zsr4tEMgUtc9J5mP3w5Yjqx99MA.og4Qd3IEVVRvtTr0FXeyVw"
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
        starter.database.add_token(user["id"], user["token"])

if __name__ == "__main__":
    insertions(clear=True)