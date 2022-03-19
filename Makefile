all: index.html data.py;

deploy: all
	mkdir public
	cp index.html public/
	cp data.py public/

data.yaml:
	./yeet.py < input.txt > data.yaml

data.py: data.yaml
	./render.py data < data.yaml > data.py

index.html: input.txt
	./render.py render < input.txt > index.html

clean:
	rm -rf public
	rm -rf data.yaml
	rm -rf data.py
	rm -rf index.html

.PHONY: all clean
