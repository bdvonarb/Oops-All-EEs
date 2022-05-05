prefix=/usr

all: kweb kweb3

kweb: kweb.c
	$(CC) $(CFLAGS) -O kweb.c -o kweb `$(PKG_CONFIG) --cflags gtk+-2.0 --libs webkit-1.0`

kweb3: kweb3.c
	$(CC) $(CFLAGS) -O kweb3.c -o kweb3 `$(PKG_CONFIG) --cflags gtk+-3.0 --libs webkit2gtk-4.0`

clean:
	rm ./kweb
	rm ./kweb3

install: all
	$(INSTALL) -d -m 0755 kweb $(TARGET_DIR)/usr/bin
	$(INSTALL) -d -m 0755 kweb3 $(TARGET_DIR)/usr/bin
	$(CP) kweb.desktop $(TARGET_DIR)/usr/share/applications
	$(CP) kweb3.desktop $(TARGET_DIR)/usr/share/applications
	$(CP) minimalkioskbrowser.png $(TARGET_DIR)/usr/share/pixmaps
	$(CP) kweb.1.gz $(TARGET_DIR)/usr/share/man/man1
	$(CP) kwebhelper.py $(TARGET_DIR)/usr/local/bin
	$(CP) kwebhelper_settings.py $(TARGET_DIR)/usr/local/bin
	$(CP) kwebhelper_set.py $(TARGET_DIR)/usr/local/bin
	$(CP) check.py $(TARGET_DIR)/usr/local/bin/kwebcheck.py
	$(CP) preparekweb $(TARGET_DIR)/usr/local/bin
	$(CP) omxplayergui $(TARGET_DIR)/usr/local/bin
	$(CP) dbuscontrolm.sh $(TARGET_DIR)/usr/local/bin
	$(CP) ginstall-ytdl $(TARGET_DIR)/usr/local/bin
	$(CP) update-ytdl $(TARGET_DIR)/usr/local/bin
	$(CP) makebin-ytdl $(TARGET_DIR)/usr/local/bin
	$(CP) kweb_bookmark.py $(TARGET_DIR)/usr/local/bin
	$(CP) kweb_edit.py $(TARGET_DIR)/usr/local/bin
	$(CP) ytdl_server.py $(TARGET_DIR)/usr/local/bin
	$(INSTALL) -d -m 0755 $(TARGET_DIR)/usr/local/share/kweb
	$(CP) about.css $(TARGET_DIR)/usr/local/share/kweb
	$(CP) about.css $(TARGET_DIR)/usr/local/share/kweb/white.css
	$(CP) black.css $(TARGET_DIR)/usr/local/share/kweb
	$(CP) grey.css $(TARGET_DIR)/usr/local/share/kweb
	$(CP) color.css $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_about_p.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_about_o.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_about_k.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_about_m.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_about_c.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) load_config.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) nogui.preset $(TARGET_DIR)/usr/local/share/kweb
	$(CP) trueaspect.preset $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kwebhelper_settings.py $(TARGET_DIR)/usr/local/share/kweb/default.preset
	$(CP) ktop $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_manual.pdf $(TARGET_DIR)/usr/local/share/kweb
	$(CP) omxplayerGUI_manual.pdf $(TARGET_DIR)/usr/local/share/kweb
	$(CP) kweb_changelog.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) empty.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) buttons_template.html $(TARGET_DIR)/usr/local/share/kweb
	$(CP) desktop.txt $(TARGET_DIR)/usr/local/share/kweb
	$(CP) omxplayergui.png $(TARGET_DIR)/usr/share/pixmaps
	$(CP) omxplayergui.desktop $(TARGET_DIR)/usr/share/applications
	$(CP) $(TARGET_DIR)/usr/local/share/kweb/ktop ~/ktop

remove: kweb
	rm $(TARGET_DIR)/usr/bin/kweb
	rm $(TARGET_DIR)/usr/bin/kweb3
	rm $(TARGET_DIR)/usr/share/applications/kweb.desktop
	rm $(TARGET_DIR)/usr/share/applications/kweb3.desktop
	rm $(TARGET_DIR)/usr/share/pixmaps/minimalkioskbrowser.png
	rm $(TARGET_DIR)/usr/share/man/man1/kweb.1.gz
	rm $(TARGET_DIR)/usr/share/pixmaps/omxplayergui.png
	rm $(TARGET_DIR)/usr/share/applications/omxplayergui.desktop
	rm $(TARGET_DIR)/usr/local/bin/kwebhelper.py
	rm $(TARGET_DIR)/usr/local/bin/kwebhelper_settings.py
	rm $(TARGET_DIR)/usr/local/bin/kwebhelper_set.py
	rm $(TARGET_DIR)/usr/local/bin/kweb_bookmark.py
	rm $(TARGET_DIR)/usr/local/bin/kweb_edit.py
	rm $(TARGET_DIR)/usr/local/bin/ytdl_server.py
	rm $(TARGET_DIR)/usr/local/bin/omxplayergui
	rm $(TARGET_DIR)/usr/local/bin/kwebcheck.py
	rm $(TARGET_DIR)/usr/local/bin/preparekweb
	rm $(TARGET_DIR)/usr/local/bin/ginstall-ytdl
	rm $(TARGET_DIR)/usr/local/bin/update-ytdl
	rm $(TARGET_DIR)/usr/local/bin/makebin-ytdl
	rm $(TARGET_DIR)/usr/local/share/kweb/*
	rmdir $(TARGET_DIR)/usr/local/share/kweb
	rm ~/ktop
	rm ~/kweb_about_c.html
	rm ~/.kweb.conf

