from db.firestore import FirebaseFirestore
from models.user import User

firestore = FirebaseFirestore()


def get_user(id: str) -> User:
    query = firestore.instance.collection("user").where(
        "id",
        "==",
        id,
    )
    users = query.stream()
    for user in users:
        if user:
            break
    u = user.to_dict()
    user = User(
        id=u["id"],
        user_name=u["user_name"],
        current_streak=u["current_streak"],
        display_picture=u["display_picture"],
        total_coins=u["total_coins"],
        # joined_on = u["joined_on"],
    )

    return user
