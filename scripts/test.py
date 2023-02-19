class enemy():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.hp = 10
    def kill(self):
        del self



enemy1 = enemy()
enemy1.kill()
del enemy1
