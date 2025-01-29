def repeat_action(agent, action, times, *args):
    for _ in range(times):
        action(*args)

def chain_actions(agent, actions):
    for action, args in actions:
        action(*args)