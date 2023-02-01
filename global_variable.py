candies = 150
name = ""
class User:

    def __init__(self, name, total):
        print('Создание объекта User')
        self.name = name
        self.total = total
        print(f'User - {self.name}',
              f'\ntotal - {self.total}')

    async def set_total(self, total):
        self.total = total

    async def take(self, take):        
        self.total -= take

    async def get_total(self):         
        return self.total
    
    async def get_name(self):
        return self.name    

