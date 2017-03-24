VERSION		:= 4.2
HTML_FILE	:= make.html_node.tar.gz 
TARGET		:= GNU_Make.docset
DOC_URL		:= https://www.gnu.org/software/make/manual/make.html_node.tar.gz
CONTENT_DIR	:= $(TARGET)/Contents/
RES_DIR		:= $(CONTENT_DIR)/Resources/
DOC_DIR		:= $(RES_DIR)/Documents/
ICONS		:= icon.png icon@2x.png

all: $(TARGET)
	@echo "Build Dash docset for GNU Make Manual"

$(TARGET): $(HTML_FILE) $(ICONS) Info.plist
	@echo "Uncompress document archive..."
	mkdir -p $(DOC_DIR)
	tar xf $(HTML_FILE) -C $(DOC_DIR)
	cp $(ICONS) $(CONTENT_DIR)/../
	cp Info.plist $(CONTENT_DIR)/
	@echo "Generating index database..."
	./gen_index.py $(TARGET)

$(HTML_FILE):
	@echo "Downloading GNU Make Manual..."
	wget ${MAKE_DOC_URL} -O ${HTML_FILE}

.PHONY: all clean
clean:
	rm -rf $(TARGET)

# vi:ai:noet:ts=4 sw=4 tw=77
