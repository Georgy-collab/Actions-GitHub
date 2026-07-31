# Деплой

Автоматическая сборка и развёртывание через GitHub Actions.

Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

## Как это работает

1. **Job `build-and-push`** — собирает Docker-образ и пушит его в [GitHub Container Registry](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry) (GHCR).
2. **Job `deploy`** — по SSH подключается к серверу, скачивает образ из GHCR и запускает контейнер.

Триггеры:

- push в ветку `main`
- ручной запуск (`workflow_dispatch`) во вкладке **Actions**

## Образ

| Параметр | Значение |
|----------|----------|
| Registry | `ghcr.io` |
| Имя | `ghcr.io/<owner>/<repo>` (в нижнем регистре) |
| Теги | `latest`, `<commit-sha>` |
| Контейнер на сервере | `time-api` |
| Порт | `8002` |

Пример: `ghcr.io/georgy-collab/actions-github:latest`

## Секреты репозитория

Settings → Secrets and variables → Actions → **New repository secret**.

| Секрет | Описание |
|--------|----------|
| `SSH_HOST` | IP или домен сервера |
| `SSH_USER` | пользователь SSH |
| `SSH_PRIVATE_KEY` | приватный ключ (содержимое файла `id_rsa` / `.pem`) |
| `SSH_PORT` | порт SSH (опционально, по умолчанию `22`) |

Отдельный `GHCR_TOKEN` **не нужен**: для `docker login` на сервере передаётся встроенный `GITHUB_TOKEN` из Actions.

Альтернатива без логина вообще — сделать пакет в GHCR публичным (Package settings → Change visibility → Public), тогда `docker pull` можно без токена.
## Требования к серверу

- установлен Docker
- пользователь из `SSH_USER` может запускать `docker` (в группе `docker` или через root)
- открыт порт `8002` (или настроен reverse proxy)
- публичный ключ, парный к `SSH_PRIVATE_KEY`, добавлен в `~/.ssh/authorized_keys`

## Что выполняется на сервере

```bash
docker login ghcr.io
docker pull <image>:latest
docker stop time-api || true
docker rm time-api || true
docker run -d --name time-api --restart unless-stopped -p 8002:8002 <image>:latest
```

## Проверка после деплоя

На сервере:

```bash
docker ps
curl http://127.0.0.1:8002/time
curl http://127.0.0.1:8002/date
```

Снаружи (если порт открыт):

```bash
curl http://<SSH_HOST>:8002/time
```

## Локальная проверка образа

```bash
docker build -t time-api .
docker run -p 8002:8002 time-api
```
