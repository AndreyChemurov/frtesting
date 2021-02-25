# Система опросов пользователей: Фабрика решений.

## Информация
- Приложения работает на порту ```8000```.
- На транспортном уровне выполняется проверка валидности переданных в теле метода аргументов. Хендлеры формируют JSON-ответ на основе строго-типизировнных данных.
- На бизнес уровне создаются запросы и коннекшены с базой данных.
- Использовалось при создании: python 3.7, postgres 13.2, django 2.2.10, linux debian 10, docker.

## Запуск приложения
```bash
git clone https://github.com/AndreyChemurov/frtesting.git
cd frtesting/
[sudo] docker-compose up
```

## Примеры запросов
![admin_auth](https://user-images.githubusercontent.com/58785926/109211042-bb9c3400-77be-11eb-8884-02e97d2b4b09.png)
![poll_create](https://user-images.githubusercontent.com/58785926/109211050-bdfe8e00-77be-11eb-87b1-5d5318ee28e8.png)
![poll_update](https://user-images.githubusercontent.com/58785926/109211055-bf2fbb00-77be-11eb-8447-aac1cc07744d.png)
![poll_delete](https://user-images.githubusercontent.com/58785926/109211057-c060e800-77be-11eb-9e2b-567b2506ecca.png)
![q_create](https://user-images.githubusercontent.com/58785926/109211061-c22aab80-77be-11eb-849d-89b357b8103d.png)
![q_delete](https://user-images.githubusercontent.com/58785926/109211069-c3f46f00-77be-11eb-8db7-68c0403867d4.png)
![complete](https://user-images.githubusercontent.com/58785926/109211080-c6ef5f80-77be-11eb-922a-db36fce98b88.png)
