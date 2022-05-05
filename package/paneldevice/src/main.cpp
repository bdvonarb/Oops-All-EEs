/*

main.cpp panel device code, starts rfcomm server, reads data, and writes to LED display

*/

#include <stdio.h>
#include <unistd.h>
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>
#include <cerrno>
#include <string>
#include <time.h>
#include <signal.h>

#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"

#include "b64decode.h"

extern "C" {
    #include "rpi_ws281x/ws2811.h"
}

#define TARGET_FREQ             WS2811_TARGET_FREQ
#define GPIO_PIN                18
#define DMA                     10
//#define STRIP_TYPE            WS2811_STRIP_RGB		// WS2812/SK6812RGB integrated chip+leds
#define STRIP_TYPE              WS2811_STRIP_GBR		// WS2812/SK6812RGB integrated chip+leds
//#define STRIP_TYPE            SK6812_STRIP_RGBW		// SK6812RGBW (NOT SK6812RGB)

#define WIDTH                   25
#define HEIGHT                  24
#define LED_COUNT               (WIDTH * HEIGHT)

#define REC_BUFF_SIZE 2048
#define IMG_BUFF_SIZE 1024

ws2811_t ledstring =
{
    .freq = TARGET_FREQ,
    .dmanum = DMA,
    .channel =
    {
        [0] =
        {
            .gpionum = GPIO_PIN,
            .invert = 0,
            .count = LED_COUNT,
            .strip_type = STRIP_TYPE,
            .brightness = 255,
        },
        [1] =
        {
            .gpionum = 0,
            .invert = 0,
            .count = 0,
            .brightness = 0,
        },
    },
};

ws2811_led_t *matrix;

static uint8_t running = 1;

int s, client;

static void ctrl_c_handler(int signum)
{
	(void)(signum);
    printf("Shutting down\n");
    close(client);
    close(s);
    ws2811_fini(&ledstring);
    exit(1);
}

int findImgInBuf(char* recbuf, char* imgbuf, int* sizeofimg, int lastbyte) {
    *sizeofimg = IMG_BUFF_SIZE;
    for(int i = 200; i < (lastbyte < IMG_BUFF_SIZE? lastbyte : IMG_BUFF_SIZE); i++) { //make this loop faster by starting at 200, images will not be shorter than that
        if(recbuf[i] == '\n') {
            *sizeofimg = i+1;
            break;
        }
    }
    if(*sizeofimg >= IMG_BUFF_SIZE) {
        *sizeofimg = 0;
        return 0;
    } else {
        memcpy(imgbuf, recbuf, *sizeofimg);
        return 1;
    }
}

int main(int argc, char **argv) {
    ws2811_return_t ret;
    matrix = (ws2811_led_t *) malloc(sizeof(ws2811_led_t) * LED_COUNT);

    if(signal(SIGINT, ctrl_c_handler) == SIG_ERR) {
        printf("Couldn't set SIGINT handler\n");
        return -1;
    }

    if(signal(SIGTERM, ctrl_c_handler) == SIG_ERR) {
        printf("Couldn't set SIGTERM handler\n");
        return -1;
    }

    if ((ret = ws2811_init(&ledstring)) != WS2811_SUCCESS)
    {
        fprintf(stderr, "ws2811_init failed: %s\n", ws2811_get_return_t_str(ret));
        return ret;
    }

    struct sockaddr_rc loc_addr = { 0 }, rem_addr = { 0 };
    char recbuf[REC_BUFF_SIZE] = { 0 };
    char imgbuf[IMG_BUFF_SIZE] = { 0 };
    int bytes_read, last_byte, sizeofimg;
    socklen_t opt = sizeof(rem_addr);

    // allocate socket
    s = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);

    // bind socket to port 1 of the first available 
    // local bluetooth adapter
    loc_addr.rc_family = AF_BLUETOOTH;
    loc_addr.rc_bdaddr = *BDADDR_ANY;
    loc_addr.rc_channel = (uint8_t) 1;
    bind(s, (struct sockaddr *)&loc_addr, sizeof(loc_addr));

    // put socket into listening mode
    listen(s, 1);

    while(true) {
        // accept one connection
        client = accept(s, (struct sockaddr *)&rem_addr, &opt);

        ba2str( &rem_addr.rc_bdaddr, recbuf );
        printf("accepted connection from %s\n", recbuf);
        last_byte = 0;
        memset(recbuf, 0, sizeof(recbuf));
        while(true) {
            // read data from the client
            
            
            do {
                if (last_byte >= REC_BUFF_SIZE-1) {
                    printf("Receive buffer full with no image found, clearing\n");
                    memset(recbuf, 0, sizeof(recbuf));
                    last_byte = 0;
                }
                bytes_read = read(client, recbuf+last_byte, sizeof(recbuf)-last_byte);
                if (bytes_read > 0) {
                    last_byte += bytes_read;
                    if (argc > 1) {
                        printf("[%d] bytes read, [%d] bytes total\n", bytes_read, last_byte);
                        if (argc > 3) {
                            printf("bytes [%s]\n", recbuf);
                        }
                    }
                } else {
                    break;
                }
            } while (!findImgInBuf(recbuf, imgbuf, &sizeofimg, last_byte));



            if (argc > 1) {
                printf("Image found, taking [%d] bytes from recbuf\n", sizeofimg);
            }
            last_byte -= sizeofimg;
            memmove(recbuf, recbuf+sizeofimg, last_byte);
            
            
            if( sizeofimg > 0 ) {
                if (argc > 2) {
                    printf("received [%d] bytes [%.*s]\n", sizeofimg, sizeofimg, imgbuf);
                }
                std::string jpgstring = b64decode(imgbuf, sizeofimg);
                if (argc > 2) {
                    printf("decoded: [%s]\n", jpgstring);
                }
                int width,height,nchan;
                uint8_t* img = (uint8_t*)stbi_load_from_memory((stbi_uc *)jpgstring.c_str(), jpgstring.length(), &width,&height,&nchan,3);
                if (img != NULL) {
                    if (argc > 1) {
                        printf("w: %d, h: %d, n: %d\n", width, height, nchan);
                        printf("first channel: [%d]\n",img[0]);
                    }
                    //copy pixels to matrix for rendering
                    for(uint8_t h = 0; h < height; h++) {
                        for(uint8_t w = 0; w < width; w++) {
                            int srcindex = h*width*3 + w*3;
                            int destindex = h%2 ? (h*width + w):(h*width + width - 1 - w);
                            matrix[destindex] = (ws2811_led_t) img[srcindex + 2] << 16 |
                                                (ws2811_led_t) img[srcindex + 1] << 8  |
                                                (ws2811_led_t) img[srcindex + 0];
                        }
                    }

                    memcpy(ledstring.channel[0].leds,matrix,sizeof(ws2811_led_t) * LED_COUNT);

                    if ((ret = ws2811_render(&ledstring)) != WS2811_SUCCESS) {
                        printf("ws2811_render failed: %s\n", ws2811_get_return_t_str(ret));
                    } else if (argc > 1) {
                        printf("ws2811_render successful\n");
                    }
                } else {
                    printf("couldn't load image: %s\n", stbi_failure_reason());
                }
            } else {
                printf("errno [%d]\n", errno);
                break;
            }
            fflush(stdout);
        }

        // close connection
        close(client);
    }
    close(s);
    ws2811_fini(&ledstring);
    return 0;
}