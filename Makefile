all: index.html data.py;

data.yaml:
	./yeet.py < input.txt > data.yaml

data.py: data.yaml
	./render.py data < data.yaml > data.py

index.html: input.txt
	./render.py render < input.txt > index.html

.PHONY: all
