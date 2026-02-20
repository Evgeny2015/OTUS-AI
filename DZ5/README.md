# Проект
Основанный на FastAPI HTTP JWT (JSON Web Token) сервер

* путь: /jwt
* настройка и запуск [README.md](/jwt/README.md)


# Разберитесь в принципах MCP

Коротко опишите в отчёте (1–2 абзаца):
как IDE/агент подключается к MCP‑серверу;
что именно вы считаете «tool» в вашем сервере.

# MCP‑сервер
MCP (Model Context Protocol) сервер для автоматического тестирования и формирования отчетов для сервиса аутентификации JWT.
* путь: /mcp
* настройка и запуск [README.md](/mcp/README.md)

Этот сервер MCP предоставляет широкие возможности тестирования для проектов на Python, специально разработанных для службы аутентификации JWT:

- **Выполнение run_tests**: Запуск pytest с настраиваемыми параметрами
- **get_test_coverage**: Создание подробных отчетов о покрытии тестами
- **analyze_test_failures**: Анализ неудачных тестов
- **list_test_files**: Перечисление доступных тестовых файлов и функций
- **get_test_metrics**: Формирование статистики выполнения тестов и тенденций

подробнее в [README.md](/mcp/README.md)

# Подключение MCP‑сервера

## VSCode
* создать файл ./vscode/mcp.json в корневой папке проекта:
```json
{
   "inputs": [],
   "servers": {
    "jwt-test-runner-http": {
      "url": "http://localhost:8000/mcp",
      "type": "http"
     },
    "jwt-test-runner": {
      "command": "uv",
      "args": [
         "run",
         "--directory",
         "${workspaceFolder}\\mcp",
         "jwt_test_runner.py"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
   }
 }
```
* выбрать один из вариантов запуска:
    * jwt-test-runner-http
    * jwt-test-runner

## VSCode + SourceCraft
* создать файл ./codeassistant/mcp.json в корневой папке проекта:
```json
{
  "mcpServers": {
    "jwt-test-runner": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "run",
        "fastmcp",
        "run",
        "jwt_test_runner.py:mcp"
      ],
      "cwd": "${workspaceFolder}\\mcp",
      "env": {},
      "disabled": true,
      "alwaysAllow": []
    },
    "jwt-test-runner2": {
      "type": "streamable-http",
      "url": "http://localhost:8001/mcp",
      "headers": {},
      "disabled": true,
      "alwaysAllow": []
    }
  }
}
```
* в настройках SourceCraft Code Assistant Settings/MCP Servers запустить один из вариантов запуска:
    * jwt-test-runner
    * jwt-test-runner2

# Проверка

- **/test**: [запуск](test/code_assistant_task_feb-3-2026_11-45-11-am.md) pytest с настраиваемыми параметрами
- **/test2**: [cоздание](test2/code_assistant_task_feb-3-2026_2-17-02-pm.md) отчета о покрытии тестами
- **/test3**: [анализ](test3/code_assistant_task_feb-3-2026_2-48-14-pm.md) неудачных тестов
- **/test6**: [перечисление](test6/code_assistant_task_feb-3-2026_7-30-16-pm.md) доступных тестовых файлов и функций
- **/test5**: [формирование](test5/code_assistant_task_feb-3-2026_5-58-22-pm.md) статистики выполнения тестов

* mcp.log - лог файл MCP-сервера для каждого запроса

