import FirmBehaviorSearch as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        import random
        yield Introduction
        yield Decide, dict(
            quality=random.randrange(1, C.MAXIMUM_QUALITY),
        )
        yield Price, dict(price=random.randrange(50, 200))
        yield Results