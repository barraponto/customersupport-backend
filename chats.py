import uuid


def get_thread():
    id = str(uuid.uuid4())
    return {"thread_id": id}


def get_configuration(thread_id: str | None = None):
    thread = {"thread_id": thread_id} if thread_id else get_thread()

    return {"configurable": thread}
