int main() {
    setuid(0);
    system("/usr/bin/python /ctf101-systems-2016/admin/create_user.py");
    return 0;
}
