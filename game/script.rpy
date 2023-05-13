# Вы можете расположить сценарий своей игры в этом файле.

init python:
    names = renpy.open_file('names.txt', encoding='utf-8').read().split('\n')
    GREETINGS = ['Приветствую!', 'Приветствую, уважаемый!', 'Привет!', 'Ну, здравствуй!', 'Здарова!', 'Здарова, бармен!', 'Хай!', 'Здоровеньки!', 'Салют!', 'Доброго!', 'Алё!', 'Алё, гараж!', 'Здрасьте.', 'Здрасьте в хату.', 'Привет, буфет!', 'Моё почтение!']
    ORDERS = [('Плесни чего-нибудь покрепче, в горле саднит.', 'Налить водки', 'Налить пива'),
              ('Жрать охота', 'Дать банку тушёнки', 'Дать батон хлеба'),
              ('Выпить охота', 'Налить водки', 'Налить пива'),
              ('Выпить охота', 'Налить водки', 'Налить пива')]
    THANKS = ['Благодарю!', 'Ну, спасибо!', 'Отлично, бывай!', 'Ещё зайду, бармен', 'Ух, мля, хорошо...', 'Спасибо!', 'Благодарствую!', 'Мерси, ёпта!', 'Давай, увидимся!', 'До встречи, бармен!', 'Покедывай!', 'Чао!']
    DECLINES = ['Ну и пошёл ты...', 'Ну ты и козёл!', 'От гнида.', 'Вот ты борзый.', 'Ладно...', 'Зря, бармен. Клиента лишаешься.', 'Ну, дело твоё...', 'Прогоришь ты с таким подходом.', 'Вот так да?', 'Ладно-ладно. Я тебе это припомню.', 'Вот, блин. А ешё бар называется...', 'Ладно, пойду к конкуренту.']
    VISITORS = ['stalker1.png', 'stalker2.png', 'stalker3.png', 'stalker4.png', 'stalker5.png', 'stalker6.png', 'stalker7.png', 'stalker8.png', 'stalker9.png']

init:
    # image black = "#000000"
    image bg bar = 'bar.jpg'  # https://www.artstation.com/artwork/1X1r8
    # image stalker = 'stalker.png'  # https://imgpng.ru/download/63129
    # image stalker:
    #    ypos 1
    # image eileen happy = "eileen1.png"
    # image eileen sad = "eileen2.png"
    # image eileen surprised = "eileen3.png"

# Определение персонажей игры.
# define e = Character('Эйлин', color="#c8ffc8")
# define visitor = Character('Сталкер')
# define visitor = Character(name=generate_name(), dynamic=True)

# Вместо использования оператора image можете просто
# складывать все ваши файлы изображений в папку images.
# Например, сцену bg room можно вызвать файлом "bg room.png",
# а eileen happy — "eileen happy.webp", и тогда они появятся в игре.

# Игра начинается здесь:
label start:

    # Подгружаем фон
    scene bg bar

    # Появляется посетитель
    # $ renpy.random.shuffle(VISITORS)
    # $ print(VISITORS)
    # $ image_name = f'stalker{renpy.random.randint(0, 8)}.png'
    # image visitor = VISITORS[0]
    # $ image_id = renpy.random.randint(0, 8)
    # image visitor = 'stalker1.png'
    
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
    $ e = Character(renpy.random.choice(names))
    $ e(renpy.random.choice(GREETINGS), interact=True)
    $ order = renpy.random.choice(ORDERS)
    $ e(order[0], interact=True)

    # Ответ бармена посетителю
    menu:

        '[order[1]]':
            $ e(renpy.random.choice(THANKS), interact=True)

        '[order[2]]':
            $ e(renpy.random.choice(THANKS), interact=True)

        'Отказать':
            $ e(renpy.random.choice(DECLINES), interact=True)

    # Посетитель уходит
    show visitor:
        xpos 300
        ypos 300
        linear 0.5 zoom 1.0 xpos -600 ypos 400

    # Ждём ухода посетителя
    pause 0.5

    # Возвращаемся к началу цикла
    jump start