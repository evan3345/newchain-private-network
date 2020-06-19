
all: build

build:
	@mkdir -p repo && cd repo && git clone git@github.com:newtonproject/newchain.git && cd newchain && make all
	@cp -f repo/newchain/build/bin/* .
