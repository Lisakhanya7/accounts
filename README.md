# Accounts Service

A Flask REST API for creating, reading, listing, updating, and deleting
accounts. Account data is stored in memory and is cleared when the service
restarts.

## Development

Create a virtual environment, install the dependencies, and start the service:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python run.py
```

The service listens on `http://localhost:8080`. Check that it is running:

```bash
curl http://localhost:8080/health
```

## API

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/health` | Health check |
| `POST` | `/accounts` | Create an account; requires `name`, accepts `email` |
| `GET` | `/accounts` | List all accounts |
| `GET` | `/accounts/{id}` | Read an account |
| `PATCH` | `/accounts/{id}` | Update an account's `name` and/or `email` |
| `DELETE` | `/accounts/{id}` | Delete an account |

Create an account with:

```bash
curl -X POST http://localhost:8080/accounts \
	-H 'Content-Type: application/json' \
	-d '{"name":"Ada Lovelace","email":"ada@example.com"}'
```

The API returns `400` when a create request has no name and `404` when an
account ID does not exist.

## Checks

Run the test suite and lint check used by GitHub Actions:

```bash
python -m unittest discover -s tests -v
flake8 service run.py
```

## Docker

Build and run the service in a container:

```bash
docker build -t accounts:latest .
docker run --rm -p 8080:8080 accounts:latest
```

## Kubernetes

Make the `accounts:latest` image available to your Kubernetes cluster, then
apply the Deployment and Service:

```bash
kubectl apply -f k8s/deployment.yaml
kubectl port-forward service/accounts 8080:8080
```

The local configuration allows requests from `http://localhost:3000` and does
not force HTTPS. Set `CORS_ORIGIN` to the frontend origin; enable
`FORCE_HTTPS=true` when serving the application behind HTTPS.

## Planning

Track stories on the [Accounts Project board](https://github.com/users/Lisakhanya7/projects/2).
The planned sprint sequence is:

- **Sprint 1:** Development environment and account CRUD.
- **Sprint 2:** Continuous integration checks; security headers and CORS.
- **Sprint 3:** Docker containerization; Kubernetes deployment; automated CD.

Move stories into Sprint Backlog when planning a sprint. Mark stories Done only
after the work is completed and verified.