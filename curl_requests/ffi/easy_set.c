
#include "easy_set.h"

int _curl_easy_setopt(void* curl, int option, void* parameter) {
    if (option < CURLOPTTYPE_OBJECTPOINT) {
        return (int)curl_easy_setopt(curl, (CURLoption)option, *(long*)parameter);
    }
    if (CURLOPTTYPE_OFF_T <= option && option < CURLOPTTYPE_BLOB) {
        return (int)curl_easy_setopt(curl, (CURLoption)option, *(curl_off_t*)parameter);
    }
    return (int)curl_easy_setopt(curl, (CURLoption)option, parameter);
}
