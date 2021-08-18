#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <curl/curl.h>

#define FROM "ts2019tp3@gmail.com"

struct upload_status {
    int lines_read;
};

char *payload_text[7];

static size_t payload_source(void *ptr, size_t size, size_t nmemb, void *userp) {
    struct upload_status *upload_ctx = (struct upload_status *)userp;
    const char *data;

    if((size == 0) || (nmemb == 0) || ((size*nmemb) < 1)) {
        return 0;
    }

    data = payload_text[upload_ctx->lines_read];

    if(data) {
        size_t len = strlen(data);
        memcpy(ptr, data, len);
        upload_ctx->lines_read++;
        return len;
    }
    return 0;
}

void fill_payload(char* number) {
    payload_text[0] = "From: Trabalho Prático\r\n";
    payload_text[1] = "Subject: File system securty code\r\n";
    payload_text[2] = "\r\n";
    payload_text[3] = "Hello, sending the security code\r\n";
    payload_text[4] = number;
    payload_text[5] = "\r\n";
    payload_text[6] = "Copy it to the right spot.\r\n";
}

int send_email(char* email_to) {
    CURL *curl;
    CURLcode res = CURLE_OK;
    struct curl_slist *recipients = NULL;
    struct upload_status upload_ctx;

    char string[6];
    srand(time(NULL));
    int r = 0;
    int nDigits = 0;

    while (nDigits != 6) {
        r = ((rand() % (999999 - 000000 + 1)) + 000000);
        nDigits = floor(log10(abs(r))) + 1;
    }

    sprintf(string,"%d",r);
    fill_payload(string);

    upload_ctx.lines_read = 0;
    curl = curl_easy_init();

    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, "smtp://smtp.gmail.com:587");
        curl_easy_setopt(curl, CURLOPT_USE_SSL, CURLUSESSL_ALL);
        curl_easy_setopt(curl, CURLOPT_USERNAME, "ts2019tp3@gmail.com");
        curl_easy_setopt(curl, CURLOPT_PASSWORD, "5-12-2019-tp3");
        curl_easy_setopt(curl, CURLOPT_MAIL_FROM, FROM);

        recipients = curl_slist_append(recipients, email_to);
        curl_easy_setopt(curl, CURLOPT_MAIL_RCPT, recipients);

        curl_easy_setopt(curl, CURLOPT_READFUNCTION, payload_source);
        curl_easy_setopt(curl, CURLOPT_READDATA, &upload_ctx);
        curl_easy_setopt(curl, CURLOPT_UPLOAD, 1L);

        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
            r = -1;
        }
        curl_slist_free_all(recipients);
        curl_easy_cleanup(curl);
    }
    return r;
}