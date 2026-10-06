#include <stdio.h>
#include <string.h>

#define OVERLAY_LEN 30
#define DEEP_LEN 19

static const unsigned char overlay[] = {
    0x0e, 0x69, 0xd6, 0x46, 0x99, 0x25, 0xb9, 0x4a,
    0x32, 0x48, 0xce, 0x6f, 0xd6, 0x3f, 0xeb, 0x45,
    0x05, 0x54, 0xa0, 0x64, 0xbd, 0x7f, 0xeb, 0x1c,
    0x36, 0x51, 0xa5, 0x63, 0xd3, 0x36
};

static const unsigned char deep[] = {
    0x0e, 0x69, 0xd6, 0x46, 0x99, 0x7b, 0xfe, 0x1e,
    0x28, 0x50, 0xa5, 0x7e, 0xbd, 0x38, 0xee, 0x1d,
    0x6d, 0x08, 0xec
};

static const unsigned char k[] = {
    0x5A, 0x3C, 0x91, 0x07, 0xE2, 0x4B, 0x88, 0x2D
};

static void decode(const unsigned char *src, int n, char *out)
{
    int i;
    for (i = 0; i < n; i++) {
        out[i] = (char)(src[i] ^ k[i % 8]);
    }
    out[n] = '\0';
}

int main(int argc, char **argv)
{
    char a[64];
    char b[64];

    puts("Night Hatch Numune Etiketleyici  v0.94");
    puts("Redhollow Basin saha birimi");
    puts("----------------------------------");

    if (argc < 2) {
        puts("kullanim: bone_tagger <numune-id>");
        return 1;
    }

    decode(overlay, OVERLAY_LEN, a);
    decode(deep, DEEP_LEN, b);

    if (strcmp(argv[1], "SF-074") == 0) {
        puts("Numune SF-074 kuyruga alindi.");
        puts("Park kapisi: MUHURLU (Agu 1994).");
        puts("Katman acildi.");
        puts(a);
        return 0;
    }

    if (strcmp(argv[1], "SF-074-DEEP") == 0) {
        puts("Ikinci katman.");
        puts(b);
        return 0;
    }

    puts("GECERSIZ NUMUNE");
    return 2;
}
