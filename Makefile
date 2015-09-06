run: client server

server:
	app/env/bin/python app/app.py

client:
	cd frontend && ember build --watch --output-path=../app/static
