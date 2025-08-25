// easy interfaces
void *curl_easy_init();
int _curl_easy_setopt(void *curl, int option, void *param);
int curl_easy_getinfo(void *curl, int option, void *ret);
int curl_easy_perform(void *curl);
void curl_easy_cleanup(void *curl);
void curl_easy_reset(void *curl);
int curl_easy_impersonate(void *curl, char *target, int default_headers);
void *curl_easy_duphandle(void *curl);
int curl_easy_upkeep(void *curl);

char *curl_version();

// slist interfaces
struct curl_slist {
   char *data;
   struct curl_slist *next;
};
struct curl_slist *curl_slist_append(struct curl_slist *list, char *string);
void curl_slist_free_all(struct curl_slist *list);

// callbacks
extern "Python" size_t buffer_callback(void *ptr, size_t size, size_t nmemb, void *userdata);
extern "Python" size_t write_callback(void *ptr, size_t size, size_t nmemb, void *userdata);
extern "Python" int debug_function(void *curl, int type, char *data, size_t size, void *clientp);

// multi interfaces
struct CURLMsg {
   int msg;       /* what this message means */
   void *easy_handle; /* the handle it concerns */
   union {
     void *whatever;    /* message-specific data */
     int result;   /* return code for transfer */
   } data;
};
void *curl_multi_init();
int curl_multi_cleanup(void *curlm);
int curl_multi_add_handle(void *curlm, void *curl);
int curl_multi_remove_handle(void *curlm, void *curl);
int curl_multi_socket_action(void *curlm, int sockfd, int ev_bitmask, int *running_handle);
int curl_multi_setopt(void *curlm, int option, void* param);
int curl_multi_assign(void *curlm, int sockfd, void *sockptr);
int curl_multi_perform(void *curlm, int *running_handle);
int curl_multi_timeout(void *curlm, long *timeout_ms);
int curl_multi_wait(void *curlm, void *extra_fds, unsigned int extra_nfds, int timeout_ms, int *numfds);
int curl_multi_poll(void *curlm, void *extra_fds, unsigned int extra_nfds, int timeout_ms, int *numfds);
int curl_multi_wakeup(void *curlm);
const char *curl_multi_strerror(int code);
struct CURLMsg *curl_multi_info_read(void* curlm, int *msg_in_queue);

// multi callbacks
extern "Python" void socket_function(void *curl, int sockfd, int what, void *clientp, void *socketp);
extern "Python" void timer_function(void *curlm, int timeout_ms, void *clientp);

// websocket
struct curl_ws_frame {
  int age;              /* zero */
  int flags;            /* See the CURLWS_* defines */
  uint64_t offset;    /* the offset of this data into the frame */
  uint64_t bytesleft; /* number of pending bytes left of the payload */
  size_t len;
  ...;
};

int curl_ws_recv(void *curl, void *buffer, size_t buflen, size_t *recv, const struct curl_ws_frame **meta);
int curl_ws_send(void *curl, const void *buffer, size_t buflen, size_t *sent, int fragsize, unsigned int sendflags);

// mime
void *curl_mime_init(void* curl);  // -> form
void *curl_mime_addpart(void *form);  // -> part/field
int curl_mime_name(void *field, char *name);
int curl_mime_data(void *field, char *name, int datasize);
int curl_mime_type(void *field, char *type);
int curl_mime_filename(void *field, char *filename);
int curl_mime_filedata(void *field, char *filename);
void curl_mime_free(void *form);

#define CURLOPT_URL 10002
#define CURLOPT_HTTPHEADER 10023
#define CURLOPT_POSTFIELDS 10015
#define CURLOPT_WRITEFUNCTION 20011
//#define CURLOPT_HEADERFUNCTION 20079
#define CURLOPT_TIMEOUT 13
#define CURLOPT_HTTPGET 80
#define CURLOPT_POST 47
#define CURLOPT_CUSTOMREQUEST 10036
#define CURLOPT_SSL_VERIFYPEER 64
#define CURLOPT_SSL_VERIFYHOST 81
#define CURLINFO_RESPONSE_CODE 2097154
const long CURLOPT_CONNECTTIMEOUT;
const long CURLE_COULDNT_CONNECT;
const long CURLE_OPERATION_TIMEDOUT;
const long CURLE_COULDNT_RESOLVE_HOST;
const long CURLOPT_HEADERFUNCTION;
const long CURLOPT_COOKIEFILE;
const long CURLOPT_FOLLOWLOCATION;
const long CURLOPT_MAXREDIRS;

const long CURLOPT_PROXY;   /* Name of proxy to use. */
const long CURLOPT_PROXYPORT;  /* Port of the proxy, can be set in the proxy string as well with:"[host]:[port]" */
const long CURLOPT_PROXYTYPE;  /* indicates type of proxy. accepted values are CURLPROXY_HTTP (default),
     CURLPROXY_HTTPS, CURLPROXY_SOCKS4, CURLPROXY_SOCKS4A and
     CURLPROXY_SOCKS5. */
const long CURLPROXY_HTTP;
const long CURLPROXY_SOCKS4;
const long CURLPROXY_SOCKS5;
const long CURLPROXY_SOCKS5_HOSTNAME;

const long CURLOPT_PROXYUSERPWD;  /* "user:password" to use with proxy. */

const long CURLOPT_ACCEPT_ENCODING; /* Set the Accept-Encoding string */

const long CURLOPT_POSTFIELDSIZE;  /* size of the POST input data, if strlen() is not good to use */

const long CURLOPT_MIMEPOST;

int add(int a, int b);