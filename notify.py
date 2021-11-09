from notifypy import Notify

notification = Notify()
notification.title = "Title"
notification.message = "this is a message"

notification.send()
