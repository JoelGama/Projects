#include <sys/stat.h>
#include <string.h>

struct userInfo {
    uid_t user_id;
    gid_t group_id;
    char *user_email;
};

struct userPerm {
    int number_users;
    struct userInfo* *setUsers;
} userPerm;
