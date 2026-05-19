score: int = 0
lives: int = 3
smart_bombs: int = 3
level_kills: int = 0
current_wave: int = 0
next_bonus_milestone: int = 10000

# Event flags — set by systems, consumed by PlayScene each frame
player_hit: bool = False
all_humanoids_gone: bool = False
level_complete: bool = False


def reset():
    global score, lives, smart_bombs, level_kills, current_wave, next_bonus_milestone
    global player_hit, all_humanoids_gone, level_complete
    score = 0
    lives = 3
    smart_bombs = 3
    level_kills = 0
    current_wave = 0
    next_bonus_milestone = 10000
    player_hit = False
    all_humanoids_gone = False
    level_complete = False


def reset_flags():
    global player_hit, all_humanoids_gone, level_complete
    player_hit = False
    all_humanoids_gone = False
    level_complete = False


def check_bonus_milestone() -> bool:
    """Returns True if a new 10k milestone was reached this frame."""
    global next_bonus_milestone, lives, smart_bombs
    if score >= next_bonus_milestone:
        lives += 1
        smart_bombs = min(smart_bombs + 1, 9)
        next_bonus_milestone += 10000
        return True
    return False
