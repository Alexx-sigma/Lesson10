# Список покупок с бюджетом — командный Telegram-бот (урок 10)

Учебный стартовый проект для команды из 2–3 человек. Есть рабочие `/start` и `/help`, независимые модули, SQLite, офлайн-заглушка ИИ и тесты. **Не содержит реальных токенов.**

## Структура
```text
bot.py             Telegram handlers и запуск
 db.py             SQLite и функции хранения
 ai.py             офлайн-заглушка ИИ
 parser.py         разбор фейковых данных
 tests/            pytest
 docs/             ТЗ, user stories, задачи, карточка команды
 .env.example      шаблон переменных окружения
 .gitignore        защита секретов
 requirements.txt  зависимости
```

## Что умеет бот
`/add Чай 100` · `/list` · `/total` · `/clear` · `/ask вопрос` · `/help`. Подробности — в `docs/TZ.md`, user stories — `docs/USER_STORIES.md`, задачи — `docs/ISSUES.md`.

## Запуск (Windows PowerShell)
```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
# Откройте .env и вставьте личный токен BotFather
python bot.py
```
Если PowerShell запрещает запуск скриптов, используйте CMD: `.venv\Scripts\activate.bat`.

## Запуск (Ubuntu / macOS)
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
# Откройте .env и вставьте личный токен BotFather
python bot.py
```

Проверьте в Telegram команды `/start` и `/help`. Завершить polling: Ctrl+C.

## Тесты (интернет и токен не нужны)
```bash
python -m pytest -q
```

## Командный Git workflow
```bash
git init
git add .
git commit -m "Initial bot skeleton"
git branch -M main
# Создайте пустой репозиторий GitHub и подключите его URL:
git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin main

git switch -c feature/help-text
# Измените текст /help или добавьте тест
git add .
git commit -m "Improve help text"
git push -u origin feature/help-text
```
Затем откройте PR через GitHub. Каждому участнику — своя ветка и свой PR. Сначала согласуйте, кто делает initial commit.

## Безопасность
- Никогда не добавляйте `.env`, токен Telegram или ключи ИИ в GitHub, Issues, PR и сообщения ChatGPT.
- Если токен утёк, отзовите его через BotFather и создайте новый. Простое удаление из файла не очищает историю Git.
- Не логируйте секреты и личные сообщения пользователей.
- `ai.py` пока не обращается к внешнему ИИ — это безопасная заглушка.

## Проверка секретов
Перед каждым push и в конце урока:
```bash
git log -p | grep -Ei "bot_token=[0-9]+:|api_key=.{10,}"   # пусто = хорошо
git status --short | grep -E "\.env$"                     # пусто = .env не в коммите
```
Если нашли токен — отзовите его в BotFather.

## Критерии сдачи
Репозиторий, заполненная `docs/TEAM_WORKSHEET.md`, 4–6 Issues, GitHub Project, `/start` и `/help`, работающие тесты, PR от каждого участника.
