#define FUSE_USE_VERSION 31

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#define _GNU_SOURCE

#ifdef linux
#define _XOPEN_SOURCE 700
#endif

#include <fuse.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>
#ifdef __FreeBSD__
#include <sys/socket.h>
#include <sys/un.h>
#endif
#include <sys/time.h>
#ifdef HAVE_SETXATTR
#include <sys/xattr.h>
#endif

#include "passthrough_helpers.h"
#include <sys/stat.h>
#include <curl/curl.h>
#include <stdlib.h>
#include "readln.h"
#include "structs.h"
#include "email.h"

//Global structures
struct userPerm createS(int n){
    struct userPerm user_perm;
    user_perm.number_users = n;
    return user_perm;
}

struct userPerm user_perm = { .number_users = 0 };

static void *xmp_init(struct fuse_conn_info *conn, struct fuse_config *cfg) {
    (void) conn;

    cfg->use_ino = 1;
    cfg->entry_timeout = 0;
    cfg->attr_timeout = 0;
    cfg->negative_timeout = 0;

    return NULL;
}

static int xmp_getattr(const char *path, struct stat *stbuf, struct fuse_file_info *fi) {
    (void) fi;
    int res;

    res = lstat(path, stbuf);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_access(const char *path, int mask) {
    int res;

    res = access(path, mask);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_readlink(const char *path, char *buf, size_t size) {
    int res;

    res = readlink(path, buf, size - 1);
    if (res == -1)
        return -errno;
    buf[res] = '\0';

    return 0;
}


static int xmp_readdir(const char *path, void *buf, fuse_fill_dir_t filler,
               off_t offset, struct fuse_file_info *fi,
               enum fuse_readdir_flags flags) {
    
    DIR *dp;
    struct dirent *de;

    (void) offset;
    (void) fi;
    (void) flags;

    dp = opendir(path);
    if (dp == NULL)
        return -errno;

    while ((de = readdir(dp)) != NULL) {
        struct stat st;
        memset(&st, 0, sizeof(st));
        st.st_ino = de->d_ino;
        st.st_mode = de->d_type << 12;

        if (filler(buf, de->d_name, &st, 0, 0))
            break;
    }

    closedir(dp);
    return 0;
}

static int xmp_mknod(const char *path, mode_t mode, dev_t rdev) {
    int res;

    res = mknod_wrapper(AT_FDCWD, path, NULL, mode, rdev);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_mkdir(const char *path, mode_t mode) {
    int res;

    res = mkdir(path, mode);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_unlink(const char *path) {
    int res;

    res = unlink(path);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_rmdir(const char *path) {
    int res;

    res = rmdir(path);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_symlink(const char *from, const char *to) {
    int res;

    res = symlink(from, to);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_rename(const char *from, const char *to, unsigned int flags) {
    int res;

    if (flags)
        return -EINVAL;

    res = rename(from, to);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_link(const char *from, const char *to) {
    int res;

    res = link(from, to);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_chmod(const char *path, mode_t mode, struct fuse_file_info *fi) {
    (void) fi;
    int res;

    res = chmod(path, mode);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_chown(const char *path, uid_t uid, gid_t gid, struct fuse_file_info *fi) {
    (void) fi;
    int res;

    res = lchown(path, uid, gid);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_truncate(const char *path, off_t size, struct fuse_file_info *fi) {
    int res;

    if (fi != NULL)
        res = ftruncate(fi->fh, size);
    else
        res = truncate(path, size);
    if (res == -1)
        return -errno;

    return 0;
}

#ifdef HAVE_UTIMENSAT
static int xmp_utimens(const char *path, const struct timespec ts[2],
               struct fuse_file_info *fi) {
    (void) fi;
    int res;

    res = utimensat(0, path, ts, AT_SYMLINK_NOFOLLOW);
    if (res == -1)
        return -errno;

    return 0;
}
#endif

static int xmp_create(const char *path, mode_t mode,
              struct fuse_file_info *fi) {
    int res;

    res = open(path, fi->flags, mode);
    if (res == -1)
        return -errno;

    fi->fh = res;
    return 0;
}

static int xmp_open(const char *path, struct fuse_file_info *fi) {
    struct stat sfile;
    int i;
    int res;
    int code;
    uid_t user_id;
    gid_t group_id;
    char *buffer_write;
    char buffer_reader[1024];
    struct userInfo *u_info;
    int number_users = user_perm.number_users;

    if((number_users == 0) && (stat(path,&sfile)==0)) {
        user_id = getuid();
        group_id = getgid();

        buffer_write = "Please, insert your email. Press enter after that.\n";
        res = write(1,buffer_write,strlen(buffer_write));
        if ((res = readln(0,buffer_reader,1024)) > 0) {
            u_info = malloc(sizeof(struct userInfo));

            //guardar email
            char email[res+1];
            strcpy(email,buffer_reader);
            email[res] = '\0';

            u_info->user_id = user_id;
            u_info->group_id = group_id;
            u_info->user_email = malloc(strlen(email) * sizeof(char));
            strcpy(u_info->user_email,email);

            user_perm.number_users++;
            user_perm.setUsers = malloc(sizeof(struct userInfo));
            user_perm.setUsers[0] = u_info;
        } else {
            printf("Read error!\n");
            return -1;
        }
    } else if((number_users > 0) && (stat(path,&sfile)==0)) {
        user_id = getuid();
        group_id = getgid();

        for(i = 0; i < number_users; i++) {
            if(user_perm.setUsers[i]->user_id == user_id) {
                break;
            }
        }

        if (i==number_users) {
            // add user
            buffer_write = "Please, insert your email. Press enter after that.\n";
            res = write(1,buffer_write,strlen(buffer_write));
            if ((res = readln(0,buffer_reader,1024)) > 0) {
                u_info = malloc(sizeof(struct userInfo));

                //guardar email
                char email[res+1];
                strcpy(email,buffer_reader);
                email[res] = '\0';

                u_info->user_id = user_id;
                u_info->group_id = group_id;
                u_info->user_email = malloc(strlen(email) * sizeof(char));
                strcpy(u_info->user_email,email);

                user_perm.setUsers = malloc(sizeof(struct userInfo));
                user_perm.setUsers[number_users] = u_info;
                user_perm.number_users++;
            } else {
                printf("Read error!\n");
                return -1;
            }
        }
    } else {
        printf("Something went worng!\n");
        return -1;
    }
    // Atualiar numbero de users
    number_users = user_perm.number_users;

    // send email
    for(i = 0; i < number_users; i++) {
        if(user_perm.setUsers[i]->user_id == user_id) { 
            code = send_email(user_perm.setUsers[i]->user_email);
            buffer_write = "Insert the code, press enter and wait 30 seconds.\n";
            res = write(1,buffer_write,strlen(buffer_write));
            break;
        }
    }

    // verify if the email was send
    if (i == number_users || (code != -1)) {
        printf("Something went worng!\n");
        return -1;
    } else {
        // verify code
        sleep(30);
        if ((res = readln(0,buffer_reader,1024)) == 6) {
            char codigo[7];
            strcpy(codigo,buffer_reader);
            codigo[6]='\0';
            if (atoi(codigo) != code) {
                printf("Wrong code!\n");
                return -1;
            } else {
                printf("Sucess!\n");
            }
        } else {
            printf("The program was not able to read the code!\n");
            return -1;
        }
    }

    //default
    res = open(path, fi->flags);
    if (res == -1) {
        return -errno;
    }
    fi->fh = res;

    return 0;
}

static int xmp_read(const char *path, char *buf, size_t size, off_t offset,
            struct fuse_file_info *fi)
{
    int fd;
    int res;

    if(fi == NULL)
        fd = open(path, O_RDONLY);
    else
        fd = fi->fh;
    
    if (fd == -1)
        return -errno;

    res = pread(fd, buf, size, offset);
    if (res == -1)
        res = -errno;

    if(fi == NULL)
        close(fd);
    return res;
}

static int xmp_write(const char *path, const char *buf, size_t size,
             off_t offset, struct fuse_file_info *fi)
{
    int fd;
    int res;

    (void) fi;
    if(fi == NULL)
        fd = open(path, O_WRONLY);
    else
        fd = fi->fh;
    
    if (fd == -1)
        return -errno;

    res = pwrite(fd, buf, size, offset);
    if (res == -1)
        res = -errno;

    if(fi == NULL)
        close(fd);
    return res;
}

static int xmp_statfs(const char *path, struct statvfs *stbuf)
{
    int res;

    res = statvfs(path, stbuf);
    if (res == -1)
        return -errno;

    return 0;
}

static int xmp_release(const char *path, struct fuse_file_info *fi)
{
    (void) path;
    close(fi->fh);
    return 0;
}

static int xmp_fsync(const char *path, int isdatasync,
             struct fuse_file_info *fi)
{
    /* Just a stub.  This method is optional and can safely be left
       unimplemented */

    (void) path;
    (void) isdatasync;
    (void) fi;
    return 0;
}

#ifdef HAVE_POSIX_FALLOCATE
static int xmp_fallocate(const char *path, int mode,
            off_t offset, off_t length, struct fuse_file_info *fi)
{
    int fd;
    int res;

    (void) fi;

    if (mode)
        return -EOPNOTSUPP;

    if(fi == NULL)
        fd = open(path, O_WRONLY);
    else
        fd = fi->fh;
    
    if (fd == -1)
        return -errno;

    res = -posix_fallocate(fd, offset, length);

    if(fi == NULL)
        close(fd);
    return res;
}
#endif

#ifdef HAVE_SETXATTR
/* xattr operations are optional and can safely be left unimplemented */
static int xmp_setxattr(const char *path, const char *name, const char *value,
            size_t size, int flags)
{
    int res = lsetxattr(path, name, value, size, flags);
    if (res == -1)
        return -errno;
    return 0;
}

static int xmp_getxattr(const char *path, const char *name, char *value,
            size_t size)
{
    int res = lgetxattr(path, name, value, size);
    if (res == -1)
        return -errno;
    return res;
}

static int xmp_listxattr(const char *path, char *list, size_t size)
{
    int res = llistxattr(path, list, size);
    if (res == -1)
        return -errno;
    return res;
}

static int xmp_removexattr(const char *path, const char *name)
{
    int res = lremovexattr(path, name);
    if (res == -1)
        return -errno;
    return 0;
}
#endif /* HAVE_SETXATTR */

#ifdef HAVE_COPY_FILE_RANGE
static ssize_t xmp_copy_file_range(const char *path_in,
                   struct fuse_file_info *fi_in,
                   off_t offset_in, const char *path_out,
                   struct fuse_file_info *fi_out,
                   off_t offset_out, size_t len, int flags)
{
    int fd_in, fd_out;
    ssize_t res;

    if(fi_in == NULL)
        fd_in = open(path_in, O_RDONLY);
    else
        fd_in = fi_in->fh;

    if (fd_in == -1)
        return -errno;

    if(fi_out == NULL)
        fd_out = open(path_out, O_WRONLY);
    else
        fd_out = fi_out->fh;

    if (fd_out == -1) {
        close(fd_in);
        return -errno;
    }

    res = copy_file_range(fd_in, &offset_in, fd_out, &offset_out, len,
                  flags);
    if (res == -1)
        res = -errno;

    close(fd_in);
    close(fd_out);

    return res;
}
#endif

static off_t xmp_lseek(const char *path, off_t off, int whence, struct fuse_file_info *fi)
{
    int fd;
    off_t res;

    if (fi == NULL)
        fd = open(path, O_RDONLY);
    else
        fd = fi->fh;

    if (fd == -1)
        return -errno;

    res = lseek(fd, off, whence);
    if (res == -1)
        res = -errno;

    if (fi == NULL)
        close(fd);
    return res;
}

static struct fuse_operations xmp_oper = {
    .init           = xmp_init,
    .getattr    = xmp_getattr,
    .access     = xmp_access,
    .readlink   = xmp_readlink,
    .readdir    = xmp_readdir,
    .mknod      = xmp_mknod,
    .mkdir      = xmp_mkdir,
    .symlink    = xmp_symlink,
    .unlink     = xmp_unlink,
    .rmdir      = xmp_rmdir,
    .rename     = xmp_rename,
    .link       = xmp_link,
    .chmod      = xmp_chmod,
    .chown      = xmp_chown,
    .truncate   = xmp_truncate,
#ifdef HAVE_UTIMENSAT
    .utimens    = xmp_utimens,
#endif
    .open       = xmp_open,
    .create     = xmp_create,
    .read       = xmp_read,
    .write      = xmp_write,
    .statfs     = xmp_statfs,
    .release    = xmp_release,
    .fsync      = xmp_fsync,
#ifdef HAVE_POSIX_FALLOCATE
    .fallocate  = xmp_fallocate,
#endif
#ifdef HAVE_SETXATTR
    .setxattr   = xmp_setxattr,
    .getxattr   = xmp_getxattr,
    .listxattr  = xmp_listxattr,
    .removexattr    = xmp_removexattr,
#endif
#ifdef HAVE_COPY_FILE_RANGE
    .copy_file_range = xmp_copy_file_range,
#endif
    .lseek      = xmp_lseek,
};

int main(int argc, char *argv[]) {
    umask(0);
    return fuse_main(argc, argv, &xmp_oper, NULL);
}
