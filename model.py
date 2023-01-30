from random import randint
import global_variable
# from controller import total
import controller


async def side_win(sides):
    side = 1 if sides == 'Орел' else 0
    win_side = randint(0, 1)
    if side == win_side:
        return True
    return False


async def bot_turn():
    if 28 >= controller.total > 0:
        take = controller.total
    else:
        chance = randint(0,10) #Шанс на победу игрока
        if chance % 2 == 0:
            print('это шанс')
            take = randint(1, 28)
        else:
            print('никаких шансов')
            take = controller.total % 29 if controller.total % 29 != 0 else randint(
            1, 28)
    controller.total -= take
    if await check_win():
        return -1
    return take


async def player_take(take):

    controller.total -= take
    if await check_win():
        return -1
    return take


async def get_total(take):
    controller.total -= take


async def checking_take(take):
    return True if 0 < take <= 28 else False


async def check_win():
    return True if controller.total <= 0 else False
