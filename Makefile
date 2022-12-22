
lint:
	pylint *.py

sample: sample.pdf

%.pdf: %.md
	pandoc --filter=pandoc_cover.py $^ -o $@

docker_bash:
	docker run -it -v `pwd`:/pandoc --entrypoint=bash dalibo/pandocker:latest
