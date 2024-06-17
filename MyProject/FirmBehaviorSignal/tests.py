import FirmBehaviorSignal as pages
from . import *
c = cu

class PlayerBot(Bot):
    def play_round(self):
        import random
        yield Introduction
        yield Decide, dict(
            quality=random.randrange(1, C.MAXIMUM_QUALITY),
            informalSignal = random.randrange(1, 100),
            formalSignal=round(random.randrange(0, 1),0),
        )
        yield Price, dict(price=random.randrange(100, 200))
        yield Results