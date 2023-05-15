# Вы можете расположить сценарий своей игры в этом файле.

init -2 python:
    # отключает продолжение диалога по клику в любой части экрана
    config.keymap["dismiss"] = None

init python:

    # Подгружаем генератор имён
    from names import Names
    names_all_json = renpy.open_file('names_all.json', encoding='utf-8')
    names_json = renpy.open_file('names.json', encoding='utf-8')
    nicknames = renpy.open_file('nicknames.json', encoding='utf-8')
    names = Names(names_all_json, names_json, nicknames)

    GREETINGS = ['Приветствую!', 'Приветствую, уважаемый!', 'Привет!', 'Ну, здравствуй!', 'Здарова!', 'Здарова, бармен!', 'Хай!', 'Здоровеньки!', 'Салют!', 'Доброго!', 'Алё!', 'Алё, гараж!', 'Здрасьте.', 'Здрасьте в хату.', 'Привет, буфет!', 'Моё почтение!']
    ORDERS = [('Плесни чего-нибудь покрепче, в горле саднит.', 'Налить водки', 'Налить пива'),
              ('Жрать охота', 'Дать банку тушёнки', 'Дать батон хлеба'),
              ('Выпить охота', 'Налить водки', 'Налить пива'),
              ('Выпить охота', 'Налить водки', 'Налить пива')]
    THANKS = ['Благодарю!', 'Ну, спасибо!', 'Отлично, бывай!', 'Ещё зайду, бармен', 'Ух, мля, хорошо...', 'Спасибо!', 'Благодарствую!', 'Мерси, ёпта!', 'Давай, увидимся!', 'До встречи, бармен!', 'Покедывай!', 'Чао!', 'Береги себя, бармен.', 'Бывай, бармен.', 'Покеда!']
    DECLINES = ['Ну и пошёл ты...', 'Ну ты и козёл!', 'От гнида.', 'Вот ты борзый.', 'Ладно...', 'Зря, бармен. Клиента лишаешься.', 'Ну, дело твоё...', 'Прогоришь ты с таким подходом.', 'Вот так, да?', 'Ладно-ладно. Я тебе это припомню.', 'Вот, блин. А ешё бар называется...', 'Ладно, пойду к конкуренту.']
    VISITORS = ['stalker1.png', 'stalker2.png', 'stalker3.png', 'stalker4.png', 'stalker5.png', 'stalker6.png', 'stalker7.png', 'stalker8.png', 'stalker9.png']

init:
    image bg bar = 'bar.jpg'  # https://www.artstation.com/artwork/1X1r8

default vodka_offered = False
default client_is_waiting = False

default vodka_bottles = 10
default energos_cans = 10

default baton_loafs = 10
default konserva_cans = 10
default kolbasa_sticks = 10

screen wares():
    text "[vodka_bottles]":
        xalign 0.87 yalign 0.50
    imagebutton:
        xalign 0.87 yalign 0.58
        idle "vodka small"
        action If(client_is_waiting and vodka_bottles > 0, Jump('vodked'))
#        action SetVariable('vodka_offered', True)
    text "[energos_cans]":
        xalign 0.77 yalign 0.50
    imagebutton:
        xalign 0.77 yalign 0.58
        idle "energos small"
        action If(client_is_waiting and energos_cans > 0, Jump('vodked'))



# Игра начинается здесь:
label start:

    # Подгружаем фон
    scene bg bar

    show screen wares

label next:

    $ vodka_offered = False

    # Выбираем рандомную картинку посетителя
    $ charlook = renpy.random.choice(VISITORS)
    image visitor:
        charlook

#    show vodka:
#        xalign 0.0 yalign 0.0

    show visitor:
        xpos -500
        ypos 400
        linear 0.5 zoom 2.0 xpos 300 ypos 300

    # Ждём, пока посетитель дойдёт до стола
    pause 0.5

    # Показываем реплику посетителя
    $ e = Character(names.new(), advance = False)
    $ client_is_waiting = True
#    $ e(renpy.random.choice(GREETINGS) + " {p=1.5}" + renpy.random.choice(ORDERS)[0], interact=False)
    $ greet = renpy.random.choice(GREETINGS)
    $ order = renpy.random.choice(ORDERS)
#    $ e(order[0], interact=True)

    # похоже {p} не работает при interact=False
    e "[greet] {p=0.5}[order[0]]" (interact=False, mode="pause")

    pause 10

    $ e(renpy.random.choice(DECLINES), interact=False)
    $ renpy.notify("Клиент недоволен")

    pause 1
    jump leave


    # Ответ бармена посетителю
   
#    menu:
#
#        '[order[1]]':
#            $ e(renpy.random.choice(THANKS), interact=True)
#
#        '[order[2]]':
#            $ e(renpy.random.choice(THANKS), interact=True)
#
#        'Отказать':
#            $ e(renpy.random.choice(DECLINES), interact=True)

label vodked:
    $ vodka_bottles -= 1

label leave:    
    # Посетитель уходит
    $ client_is_waiting = False

    show visitor:
        xpos 300
        ypos 300
        linear 0.5 zoom 1.0 xpos -600 ypos 400

    # Ждём ухода посетителя
    pause 0.5

    # Возвращаемся к началу цикла
    jump next
