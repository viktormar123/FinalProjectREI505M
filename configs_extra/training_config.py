import sys
args = [x.lower() for x in sys.argv]

def initialize_variables(args):
    print(f"Usage: python training.py [train] [eval] [printq] epi=<num_episodes> eps=<epsilon> epd=<epsilon_decay> mine=<min_epsilon> qtn=<q_table_name>")
    train = True if "train" in args else False
    eval = True if "eval" in args else False
    print_q = True if "printq" in args else False
    num_episodes, epsilon, epsilon_decay, min_epsilon, q_table_name = None, None, None, None, None
    for arg in args:
        if "=" not in arg:
            continue
        key, value = arg.split("=")
        match key:
            case "epi":
                num_episodes = int(value)
            case "eps":
                epsilon = float(value)
            case "epd":
                epsilon_decay = float(value)
            case "mine":
                min_epsilon = float(value)
            case "qtn":
                q_table_name = value
            
    #Initialize the variables if they are not set
    def set_default(obj, default):
        if not obj:
            obj = default
        return obj

    try:
        epsilon = set_default(epsilon, 1.0)
        epsilon_decay = set_default(epsilon_decay, 0.99999)
        min_epsilon = set_default(min_epsilon, 0.05)
        q_table_name = set_default(q_table_name, "q_table.pkl")
        num_episodes = set_default(num_episodes, 500)
    except NameError:
        print("Error: missing arguments")
        print("Usage: python training.py [train] [eval] [printq] epi=<num_episodes> eps=<epsilon> epd=<epsilon_decay> mine=<min_epsilon> qtn=<q_table_name>")
            
    return train, eval, print_q, num_episodes, epsilon, epsilon_decay, min_epsilon, q_table_name


