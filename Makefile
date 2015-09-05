run: client server

server:
	app/env/bin/python app/app.py

client:
	cd frontend && ember build --output-path=../app/static
