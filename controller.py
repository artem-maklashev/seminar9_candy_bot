from aiogram import types
import view
import model
from global_variable import candies


game_status = False
player_name = ''
global total
total = candies

async def lets_play(message: types.Message):
    sides = message.text
    win_side = await model.side_win(sides)
    await view.turn_message(message, sides, win_side)
    if win_side != True:
        take = await model.bot_turn()        
        await view.bot_play_massage(message, take)
    
        


async def player_turn(message: types.Message):
    global total
    step_forward = await model.checking_take(int(message.text))
    if step_forward:
        take = await model.player_take(int(message.text))
        if take != -1:
            await view.player_message(message, take)
            take = await model.bot_turn()
            if take != -1:
                await view.bot_play_massage(message, take)
            else:
                await view.bot_win(message)                
                total = candies
        else:
            print('Победил игрок. Далее сообщение о победе')
            await view.player_win(message)            
            total = candies
    else:
        await view.take_error(message)
    


