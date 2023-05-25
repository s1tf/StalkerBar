# Вы можете расположить сценарий своей игры в этом файле.

init python:

    # Подгружаем генератор имён
    from names import Names
    names_all_json = renpy.open_file('names_all.json', encoding='utf-8')
    names_json = renpy.open_file('names.json', encoding='utf-8')
    nicknames = renpy.open_file('nicknames.json', encoding='utf-8')
    names = Names(names_all_json, names_json, nicknames)

    # Загружаем "Байки сталкеров"
    tales_ = renpy.open_file('tales.txt', encoding='utf-8').read().split('***')
    tales = []
    for t in tales_:
        tale = t.split('\n')
        tale = [t for t in tale if t]
        tales.append(tale)

    GREETINGS = ['Приветствую!', 'Приветствую, уважаемый!', 'Привет!', 'Ну, здравствуй!', 'Здарова!', 'Здарова, бармен!', 'Хай!', 'Здоровеньки!', 'Салют!', 'Доброго!', 'Алё!', 'Алё, гараж!', 'Здрасьте.', 'Здрасьте в хату.', 'Привет, буфет!', 'Моё почтение!']
    ORDERS = [('Плесни чего-нибудь покрепче, в горле саднит.', 'Налить водки', 'Налить пива'),
              ('Жрать охота', 'Дать банку тушёнки', 'Дать батон хлеба'),
              ('Выпить охота', 'Налить водки', 'Налить пива'),
              ('Выпить охота', 'Налить водки', 'Налить пива')]
    THANKS = ['Благодарю!', 'Ну, спасибо!', 'Отлично пошла!', 'Ух, мля, хорошо...', 'Спасибо!', 'Благодарствую!', 'Мерси, ёпта!', 'Пошла вода горячая!']
    BYE = ['Отлично, бывай!', 'Ещё зайду, бармен', 'Давай, увидимся!', 'До встречи, бармен!', 'Покедывай!', 'Чао!', 'Береги себя, бармен.', 'Бывай, бармен.', 'Покеда!']
    DECLINES = ['Ну и пошёл ты...', 'Ну ты и козёл!', 'От гнида.', 'Вот ты борзый.', 'Ладно...', 'Зря, бармен. Клиента лишаешься.', 'Ну, дело твоё...', 'Прогоришь ты с таким подходом.', 'Вот так, да?', 'Ладно-ладно. Я тебе это припомню.', 'Вот, блин. А ешё бар называется...', 'Ладно, пойду к конкуренту.']
    WHATS_NEW_QUESTION = ['Что нового?', 'Что слышно?', 'Что нового в Зоне?', 'Какие новости?']
    VISITORS = ['stalker1.png', 'stalker2.png', 'stalker3.png', 'stalker4.png', 'stalker5.png', 'stalker6.png', 'stalker7.png', 'stalker8.png', 'stalker9.png']

init:
    image bg bar = 'bar.jpg'  # https://www.artstation.com/artwork/1X1r8

# Игра начинается здесь
label start:

    # Подгружаем фон
    scene bg bar

    # Выбираем рандомную картинку посетителя
    $ charlook = renpy.random.choice(VISITORS)
    image visitor:
        charlook

    show visitor:
        xpos -500
        ypos 400
        linear 0.5 zoom 2.0 xpos 300 ypos 300

    # Ждём, пока посетитель дойдёт до стола
    pause 0.5

    # Показываем реплику посетителя
    # $ e = Character(names.new(), what_size=22)
    $ e = Character(names.new(), window_top_padding=-110)
    $ e(renpy.random.choice(GREETINGS), interact=True)
    $ order = renpy.random.choice(ORDERS)
    $ e(order[0], interact=True)

    # Ответ бармена посетителю
    menu:

        '[order[1]]':
            $ e(renpy.random.choice(THANKS), interact=True)
            jump ask_visitor

        '[order[2]]':
            $ e(renpy.random.choice(THANKS), interact=True)
            jump ask_visitor

        'Отказать':
            $ e(renpy.random.choice(DECLINES), interact=True)
            jump visitor_leaves

# Спросить посетителя про дела
label ask_visitor:

    $ question = renpy.random.choice(WHATS_NEW_QUESTION)
    $ bye = renpy.random.choice(BYE)

    menu:
        # Задать вопрос посетителю
        '[question]':
            $ tale = renpy.random.choice(tales)
            $ i = 0
            while i < len(tale):
                $ e(tale[i], interact=True)
                $ i += 1
            jump visitor_leaves

        # Попрощаться с посетителем
        'Бывай':
            $ e(renpy.random.choice(BYE), interact=True)
            jump visitor_leaves

# Посетитель уходит
label visitor_leaves:

    # Посетитель уходит
    show visitor:
        xpos 300
        ypos 300
        linear 0.5 zoom 1.0 xpos -600 ypos 400

    # Ждём ухода посетителя
    pause 0.5

    # Возвращаемся к новому посетителю
    jump start
