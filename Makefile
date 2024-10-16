interface:
	python serve.py

revision:
	alembic revision --autogenerate -m "$(comment)"

upgrade:
	alembic upgrade head