import os
import pandas as pd
def __color_translate(wire_color, color_dict):
    '''
    Func translates color of rus symbols from table WIRES (database) to english for wire chart

    :param wire_color: string
    :return: wire_color_eng: string, translated color to english
    '''
    color1, color2 = None, None
    if len(wire_color) == 3:
        if wire_color[0] == 'К':
            color1 = 'BROWN'
            color2 = color_dict[wire_color[2]]
        elif wire_color[1] == 'К':
            color1 = color_dict[wire_color[0]]
            color2 = 'BROWN'
        wire_color_eng = color1 + ' ' + color2
    elif len(wire_color) == 2:
        if wire_color == 'Кч':
            wire_color_eng = 'BROWN'
        else:
            color1 = color_dict[wire_color[0]]
            color2 = color_dict[wire_color[1]]
            wire_color_eng = color1 + ' ' + color2
    else:  # can be just len = 1
        wire_color_eng = color_dict[wire_color]

    return wire_color_eng


def __color(wire_color, colors):
    wire_color_eng = __color_translate(wire_color, color_dict)
    res_color = wire_color_eng if (wire_color in colors) else wire_color_eng.split()[0] # если нужного цвета нет в списке цветов Преттль, берем первый
    return res_color, wire_color_eng
    # возвращаем оба варианта, потому что будет проще, если сравнить их в случае отличия печатать цвет провода в маркировке



color_dict = {'Ч': 'BLACK', 'Б': 'WHITE', 'Г': 'BLUE', 'К': 'RED', 'Кч': 'BROWN', 'Р': 'PINK', 'С': 'GRAY',
                  'Ж': 'YELLOW', 'З': 'GREEN', 'О': 'ORANGE', 'Ф': 'PURPLE'}

if os.path.exists('C:\Komax\Data\TopWin\KomaxColors.xlsx'):
    colors = pd.read_excel('C:\Komax\Data\TopWin\KomaxColors.xlsx', index_col=0)['Обозначение'].to_numpy()
    print('Y', colors)
else:
    colors = (
    'Б', 'БГ', 'БК', 'Г', 'ГБ', 'ГК', 'Ж', 'ЖГ', 'З', 'ЗК', 'К', 'КБ', 'Кч', 'О', 'ОБ', 'Р', 'РГ', 'С', 'Ф', 'Ч')
    print('N', colors)



wire_colors = ['БКч', 'БГ', 'БК', 'Г', 'ГБ', 'КБ', 'КчЖ', 'ЗГ', 'КЗ', 'БО', 'О', 'РГ', 'ГЖ']

for wire_color in wire_colors:
    print(__color(wire_color, colors)[0], '||', __color(wire_color, colors)[1])
    print('цвет:', wire_color, 'color:', __color(wire_color, colors)[0],
          'маркировка:', __color(wire_color, colors)[1] if __color(wire_color, colors)[0]!=__color(wire_color, colors)[1] else None)
