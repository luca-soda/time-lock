test:
	cd src && python -m unittest tests/*.py

dev:
	cd src && uvicorn main:app --reload

run:
	cd src && uvicorn main:app