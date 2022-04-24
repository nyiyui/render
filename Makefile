all: index.html index2.html data.py;

deploy: clean all
	mkdir public
	cp index.html public/
	cp index2.html public/
	cp data.py public/

data.yaml:
	./yeet.py < input.txt > data.yaml

data.py: data.yaml
	./render.py data < data.yaml > data.py

index.html: input.txt
	./render.py render < input.txt > index.html

index2.html: input.txt
	./render.py render 1 < input.txt > index2.html

clean:
	rm -rf public
	rm -rf data.yaml
	rm -rf data.py
	rm -rf index.html
	rm -rf index2.html

.PHONY: all clean
