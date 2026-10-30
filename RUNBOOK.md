# Runbook

## 1. Сервис не отвечает
1. Проверить контейнеры: docker compose ps (app и db должны быть Up, db healthy)
2. Посмотреть логи: docker compose logs app --tail 100
3. Проверить health: curl localhost:8000/health

## 2. Откат на предыдущую версию
1. Узнать предыдущую версию в CHANGELOG.md или во вкладке Packages на GitHub
2. Выполнить:

       export APP_VERSION=<предыдущая версия, например 1.0.0>
       docker compose pull app
       docker compose up -d --no-build

3. Подождать 10 секунд и проверить: curl localhost:8000/health (версия должна совпасть)
4. Проверить данные: curl localhost:8000/messages (записи на месте, база в volume pgdata)

## 3. База не поднимается
1. docker compose logs db --tail 50
2. Проверить, что в .env задан POSTGRES_PASSWORD и он совпадает с паролем в DATABASE_URL
3. Данные не удалять: не использовать docker compose down -v (флаг -v удаляет volume)

## 4. Новая версия сломалась после выката
1. Откатиться (раздел 2)
2. Найти причину во вкладке Actions на GitHub и в логах контейнера
3. Исправить, выпустить новый тег vX.Y.Z

## 5. Образ не скачивается (denied / not found)
1. Проверить, что образ с такой версией есть во вкладке Packages
2. Проверить, что запуск Actions для тега завершился зелёным
