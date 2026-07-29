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
| Порт | `8000` |

Пример: `ghcr.io/georgy-collab/actions-github:latest`

## Секреты репозитория

Settings → Secrets and variables → Actions → **New repository secret**.

| Секрет | Описание |
|--------|----------|
| `SSH_HOST` | IP или домен сервера |
| `SSH_USER` | пользователь SSH |
| `SSH_PRIVATE_KEY` | приватный ключ (содержимое файла `id_rsa` / `.pem`) |
| `SSH_PORT` | порт SSH (обычно `22`) |
| `GHCR_TOKEN` | Personal Access Token с правом `read:packages` |

`GITHUB_TOKEN` для пуша образа в GHCR Actions выдаёт сам — отдельно создавать не нужно.

### Как создать `GHCR_TOKEN`

1. GitHub → **Settings** → **Developer settings** → **Personal access tokens**.
2. Создай token (classic) с правом `read:packages` (для приватных пакетов также `repo`).
3. Добавь его в секреты репозитория как `GHCR_TOKEN`.

## Требования к серверу

- установлен Docker
- пользователь из `SSH_USER` может запускать `docker` (в группе `docker` или через root)
- открыт порт `8000` (или настроен reverse proxy)
- публичный ключ, парный к `SSH_PRIVATE_KEY`, добавлен в `~/.ssh/authorized_keys`

## Что выполняется на сервере

```bash
docker login ghcr.io
docker pull <image>:latest
docker stop time-api || true
docker rm time-api || true
docker run -d --name time-api --restart unless-stopped -p 8000:8000 <image>:latest
```

## Проверка после деплоя

На сервере:

```bash
docker ps
curl http://127.0.0.1:8000/time
curl http://127.0.0.1:8000/date
```

Снаружи (если порт открыт):

```bash
curl http://<SSH_HOST>:8000/time
```

## Локальная проверка образа

```bash
docker build -t time-api .
docker run -p 8000:8000 time-api
```
