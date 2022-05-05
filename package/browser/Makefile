
all: browser

browser:
	$(CC) $(CFLAGS) -O browser.c -o browser `$(PKG_CONFIG) --cflags gtk+-3.0 --libs webkit2gtk-4.0`

clean:
	$(RM) browser
