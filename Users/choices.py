from .models import UsersWaitingResponse

USERS = []
RESPONSE_CHOICES = [
    (1,'Accept'),
    (2, 'Reject'),
]

def getUsers():
    WaitingResponse = UsersWaitingResponse.objects.all()
    counter = 1
    USERS = []
    for i in WaitingResponse:
        USERS.append((i, i))
        counter+=1
    return USERS