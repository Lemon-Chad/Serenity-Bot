from cogs.entities import DisCharacter, Enemy


class RPGContext:
    player: DisCharacter
    
    def __init__(self, player: DisCharacter):
        self.player = player

        
class BattleContext(RPGContext):
    enemy: Enemy
    
    def __init__(self, player: DisCharacter, enemy: Enemy, battle):
        super().__init__(player)
        self.enemy = enemy
        self.battle = battle
