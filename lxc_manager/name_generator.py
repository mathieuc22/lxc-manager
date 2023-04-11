import secrets

ADJECTIVES = [
    "agile",
    "brave",
    "calm",
    "daring",
    "eager",
    "fierce",
    "graceful",
    "happy",
    "intelligent",
    "jovial",
    "keen",
    "lively",
    "magnificent",
    "noble",
    "optimistic",
    "plucky",
    "quick",
    "resilient",
    "strong",
    "tenacious",
    "upbeat",
    "vibrant",
    "wise",
    "xenodochial",
    "youthful",
    "zealous",
]

NOUNS = [
    "antelope",
    "bear",
    "cat",
    "dog",
    "eagle",
    "fox",
    "giraffe",
    "hawk",
    "iguana",
    "jaguar",
    "kangaroo",
    "lion",
    "monkey",
    "narwhal",
    "octopus",
    "panther",
    "quokka",
    "rabbit",
    "snake",
    "tiger",
    "urchin",
    "vulture",
    "walrus",
    "xerus",
    "yak",
    "zebra",
]


def generate_container_name(prefix):
    adjective = secrets.choice(ADJECTIVES)
    noun = secrets.choice(NOUNS)

    return f"{prefix}-{adjective}-{noun}"
