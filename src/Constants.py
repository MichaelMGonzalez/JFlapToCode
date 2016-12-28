import os

slash = "\\" if os.name == "NT" else "/"
f_path = slash.join( [os.path.dirname(__file__), ".." ])
templates_dir = slash.join([f_path, "templates"])
nl = "\n"
tab = "    "
enum = "State"
state_action = "ExecuteAction"
config_file = slash.join([f_path, "Config", "settings.json"])
wrapper_function = "wrapper_function"
inf_loop = "looping_body"
hlsm = "fa"
mdp  = "mealy"
on_trans = "on_transition"
on_trans_type = "on_transition_type"
def indent( body ):
    return [ tab + l for l in body ]
