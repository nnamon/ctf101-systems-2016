void b() {
    int stuff;
    stuff = 1;
    return;
}

void a() {
    b();
}

int main() {
    a();
}
