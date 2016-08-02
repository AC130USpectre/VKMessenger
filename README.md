# VKMessenger

Simple VK messenger on PyQt4.

Мессенджер для ВКонтакте на базе PyQt4.

Для использования мессенджера необходимо создать свой токен авторизации. Если вы не хотите пользоваться токеном, отредактируйте фрагмент кода в файле messenger.py, отвечающий за авторизацию.

Для получения токена вам необходимо выполнить следующие шаги:

1) Создать своё Standalone-приложение (https://new.vk.com/editapp?act=create) и найти его ID.

2) Будучи авторизованным ВКонтакте, перейти по ссылке (https://oauth.vk.com/authorize?client_id={id приложения}&display=page&redirect_uri=https://oauth.vk.com/blank.html&scope=friends,photos,audio,video,docs,notes,pages,status,wall,groups,messages,offline&response_type=token&v=5.52), подтвердить разрешения и скопировать токен авторизации из ссылки-редиректа.

3) Полученный токен записать в файл AccessToken.txt и положить в одну папку с файлами приложения.
