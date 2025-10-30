# 控制台设置
import pygame

from include import variable
from include import card as include_card
from include.card import card_functions_all

pygame.init()
console_surf_h = 200
console_input = ""  # 输入的字符串
console_output = ("", "null")  # 输出的字符串与输出类型
debug_mode = []
console_input_inn = []  # 过往输入
console_input_inn_index = 0  # 过往输入索引


def console_hint_all(input_str=""):
    """
    控制台提示
    :param input_str: 输入的字符串
    :return: 提示字符串
    """

    hint = ""
    input = input_str.strip(" ").split(" ")
    if len(input) > 0:
        hint = ""
        # g
        if len(input) == 1 and input[0] in "g":
            hint += "g "
        if len(input) == 1 and input[0] == "g":
            hint = "".join([str(f["ID"]) + ":" + f["name"].replace(" ", "") + "  " for f in card_functions_all])
        if len(input) == 2 and input[0] == "g":
            if input[1].isdigit():
                hint = "".join(
                    [str(f["ID"]) + ":" + f["name"].replace(" ", "") + "  " for f in card_functions_all if
                     f["ID"] == int(input[1])])
            elif input[1] == "f":
                hint = "".join(
                    [f["value"].replace(" ", "") + "  " for f in card_functions_all if
                     f["type"] == 'function'])

        # debug
        if len(input) == 1 and input[0] in "debug":
            hint += "debug "
        if len(input) == 1 and input[0] == "debug":
            hint = "1:immortal 2:seckill"
        # Card
        if len(input) == 1 and input[0] in "card":
            hint += "card "
        if len(input) == 1 and input[0] == "card":
            hint = "add set"
        if len(input) == 2 and input[0] == "card":
            hint = ""
            if input[1] in 'add':
                hint += "add "
            if input[1] in 'set':
                hint += "set "
        # Repeat
        if len(input) == 1 and input[0] in "repeat":
            hint += "repeat "
    if hint == "":
        hint += "g "
        hint += "debug "
        hint += "card "
        hint += "repeat "
    return hint


console_hint = console_hint_all("")
console_font = pygame.font.Font(None, 36)  # 控制台字体


def console_input_up():
    global console_input, console_hint, console_input_inn, console_input_inn_index
    console_input_inn_index += 1
    try:
        console_input = console_input_inn[-console_input_inn_index]
    except IndexError:
        console_input_inn_index -= 1
    console_hint = console_hint_all(console_input)


def console_input_down():
    global console_input, console_hint, console_input_inn, console_input_inn_index
    if console_input_inn_index > 1:
        console_input_inn_index -= 1
        try:
            console_input = console_input_inn[-console_input_inn_index]
        except IndexError:
            console_input_inn_index += 1
    else:
        console_input = ""
        if console_input_inn_index > 0:
            console_input_inn_index -= 1
    console_hint = console_hint_all(console_input)


def console_input_text(text):
    global console_input, console_hint
    console_input += text  # 记录输入的字符
    console_input = console_input.lower()
    console_hint = console_hint_all(console_input)


def console_backspace():
    global console_input, console_hint
    console_input = console_input[:-1]
    console_hint = console_hint_all(console_input)


def console_execute():
    global console_input, console_output, console_input_inn, console_input_inn_index, out_put, output_type, debug_mode
    console_input_inn.append(console_input)
    console_input_inn_index = 0
    out_put = console_input
    output_type = "null"
    command_input = console_input.split(" ")
    repeat_num = 1
    if command_input[0] == "repeat":  # 重复执行上一次指令
        if len(command_input) == 2 and command_input[1].isdigit():
            repeat_num = int(command_input[1])
            if len(console_input_inn) > 1:
                last_input = console_input_inn[-2]
                i = 0
                if "repeat" in last_input:
                    while "repeat" in last_input:
                        i += 1
                        try:
                            last_input = console_input_inn[-2 - i]
                            command_input = last_input.split(" ")
                        except IndexError:
                            out_put = "can't repeat repeat"
                            output_type = "error"
                            repeat_num = 0
                            break
                else:
                    command_input = last_input.split(" ")
            else:
                out_put = "no command to repeat"
                output_type = "error"
                repeat_num = 0
        else:
            out_put = "no command to repeat"
            output_type = "error"
            repeat_num = 0
    for _ in range(repeat_num):
        if command_input[0] == "g":  # 获取卡片
            if len(command_input) == 2:
                card_ID = command_input[1]
                out_put = include_card.card_function(card_ID)
                output_type = "success" if out_put == "success" else "error"
            else:
                out_put = console_input
                output_type = "null"
        elif command_input[0] == "debug":  # 调试模式
            if len(command_input) == 2:
                if command_input[1] == "1":  # debug模式1
                    if 1 in debug_mode:
                        debug_mode.remove(1)
                    else:
                        debug_mode.append(1)
                    out_put = "success"
                    output_type = "success"
                elif command_input[1] == "2":  # debug模式2
                    if 2 in debug_mode:
                        debug_mode.remove(2)
                    else:
                        debug_mode.append(2)
                    out_put = "success"
                    output_type = "success"
                elif command_input[1] == "3":  # debug模式3
                    if 3 in debug_mode:
                        debug_mode.remove(3)
                    else:
                        debug_mode.append(3)
                    out_put = "success"
                    output_type = "success"
                elif command_input[1] == "4":  # debug模式4
                    if 4 in debug_mode:
                        debug_mode.remove(4)
                    else:
                        debug_mode.append(4)
                    out_put = "success"
                    output_type = "success"
        elif command_input[0] == "card":  # 卡牌处理
            if len(command_input) == 2:
                if command_input[1] == "add":
                    variable.can_card_choose_number += 1
                    out_put = "success"
                    output_type = "success"
            if len(command_input) == 3 and command_input[2].isdigit():
                if command_input[1] == "add":
                    variable.can_card_choose_number += int(command_input[2])
                    out_put = "success"
                    output_type = "success"
                if command_input[1] == "set":
                    variable.can_card_choose_number = int(command_input[2])
                    out_put = "success"
                    output_type = "success"
        else:
            out_put = console_input
            output_type = "null"
    # 清空输入，显示输出
    console_output = (out_put, output_type)
    console_input = ""
