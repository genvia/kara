tags:
	ctags -R .
test:
	pytest	tests
init:
	pip install -r requirements.txt
publish:
	python setup.py register
	python setup.py sdist
	python setup.py bdist_wheel
clean:
	rm -rf build dist .eggs kara.egg-info .cache .ropeproject logs/* .DS_store

