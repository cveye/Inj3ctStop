.PHONY: install run test deploy

install:
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

run:
	python -m core.run

test:
	pytest -q

deploy:
	./scripts/deploy.sh ${HOST} ${REMOTE_DIR}
