BUILD_DIR=build
CFLAGS=-u
CC=python3

.PHONY: sys clean

sys: 
	 @echo "Opening application..."
	 $(CC) $(CFLAGS) app_frontend.py

clean:
	rm -rf $(BUILD_DIR)/*