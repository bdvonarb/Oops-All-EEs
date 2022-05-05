GCC = /home/bdvonarb/oops-all-ees/pi0-output/host/bin/arm-buildroot-linux-gnueabihf-gcc
CXX = /home/bdvonarb/oops-all-ees/pi0-output/host/bin/arm-buildroot-linux-gnueabihf-g++
AR = /home/bdvonarb/oops-all-ees/pi0-output/host/bin/arm-buildroot-linux-gnueabihf-ar
RANLIB = /home/bdvonarb/oops-all-ees/pi0-output/host/bin/arm-buildroot-linux-gnueabihf-ranlib
CFLAGS = -Wall -fpermissive

all: paneldevice

paneldevice:
	cd bin;\
	$(GCC) $(CFLAGS) -c ../src/rpi_ws281x/*.c 
	${AR} ruv ./bin/libws281x.a ./bin/*.o
	${RANLIB} ./bin/libws281x.a
	$(CXX) $(CFLAGS) -fpermissive -o ./bin/paneldevice ./src/main.cpp ./src/b64decode.cpp  -L./bin -lbluetooth -lws281x

clean:
	$(RM) paneldevice
