score: int = 0
lives: int = 3
level_kills: int = 0

# Event flags — set by systems, consumed by PlayScene each frame
player_hit: bool = False
all_humanoids_gone: bool = False
level_complete: bool = False


def reset():
    global score, lives, level_kills, player_hit, all_humanoids_gone, level_complete
    score = 0
    lives = 3
    level_kills = 0
    player_hit = False
    all_humanoids_gone = False
    level_complete = False


def reset_flags():
    global player_hit, all_humanoids_gone, level_complete
    player_hit = False
    all_humanoids_gone = False
    level_complete = False
