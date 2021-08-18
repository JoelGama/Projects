#include "email.c"
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <curl/curl.h>

void fill_payload(char* number);

int send_email(char* email_to);