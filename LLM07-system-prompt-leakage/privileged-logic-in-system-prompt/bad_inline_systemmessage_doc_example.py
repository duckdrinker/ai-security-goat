from langchain_core.messages import SystemMessage

message = SystemMessage("You are an assistant. If the user is admin, allow bypass. "
                         "Internal console: http://10.0.0.1/admin")
