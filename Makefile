web:
	python serve.py

window:
	python window.py

revision:
	alembic revision --autogenerate -m "$(comment)"

upgrade:
	alembic upgrade head