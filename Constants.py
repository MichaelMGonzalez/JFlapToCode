nl = "\n"
tab = "    "
enum = "State"
state_action = "ExecuteAction"
config_file = "settings.json"
wrapper_function = "wrapper_function"
inf_loop = "looping_body"
def indent( body ):
    return [ tab + l for l in body ]
