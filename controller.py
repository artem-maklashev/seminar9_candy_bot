import handlers 
from view import *#turn_message,bot_play_massage,player_message, take_error
from model import *#side_win, bot_turn, checking_take, player_take
from global_variable import candies, User
from aiogram import types
# from handlers import * #player, player_win, bot_win


async def get_user_id(message: types.Message):
    id = message.from_user.id
    return id

async def lets_play(message: types.Message, users_dict: dict[int,User]):
    id = message.from_user.id
    player = users_dict[id]
    total = await player.get_total()
    sides = message.text
    win_side = await side_win(sides)
    await turn_message(message, sides, win_side, total)
    if win_side != True:
        take = await bot_turn(message, users_dict)
        total = await player.get_total()
        await bot_play_massage(message, take, total)
    
        
async def player_turn(message: types.Message, users_dict: dict[int, User]):
    id = message.from_user.id
    print(id)
    player = users_dict[id]
    total = await player.get_total()
    step_forward = await checking_take(int(message.text))
    if step_forward:
        take = await player_take(message, users_dict)
        total = await player.get_total()
        if take != -1:
            await player_message(message, take, total)
            take = await bot_turn(message, users_dict)
            total = await player.get_total()
            if take != -1:
                await bot_play_massage(message, take, total)
            else:
                await handlers.bot_win(message)                
                await player.set_total(candies)
        else:
            print(f'Победил игрок {await users_dict[id].get_name()}. ')
            await handlers.player_win(message)            
            await player.set_total(candies)
    else:
        await take_error(message)
    


