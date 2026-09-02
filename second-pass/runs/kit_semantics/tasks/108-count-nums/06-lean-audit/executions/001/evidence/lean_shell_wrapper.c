#include <lean/lean.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern void lean_initialize(void);
extern void lean_set_panic_messages(bool flag);
extern char **lean_setup_args(int argc, char **argv);
extern lean_object *initialize_Lean_Shell(
    uint8_t builtin, lean_object *world);
extern lean_object *initialize_Lean_Data_Options(
    uint8_t builtin, lean_object *world);
extern lean_object *l_Lean_KVMap_empty;
extern lean_object *l_Lean_Options_empty;
extern lean_object *l_Lean_initSearchPath(
    lean_object *, lean_object *, lean_object *);
extern lean_object *
l___private_Lean_Shell_0__Lean_shellMain___boxed(lean_object **);

struct parsed {
    const char *file;
    const char *root;
    const char *setup;
    const char *olean;
    const char *ilean;
    const char *cfile;
    const char *bcfile;
    bool only_deps;
    bool only_src_deps;
    bool json;
    bool stats;
    bool run;
};

static lean_object *mk_list1(const char *value) {
    if (value == NULL) {
        return lean_box(0);
    }
    lean_object *cell = lean_alloc_ctor(1, 2, 0);
    lean_ctor_set(cell, 0, lean_mk_string(value));
    lean_ctor_set(cell, 1, lean_box(0));
    return cell;
}

static lean_object *mk_empty_options(void) {
    return lean_box(0);
}

static lean_object *mk_optional_string(const char *value) {
    if (value == NULL) {
        return lean_box(0);
    }
    lean_object *result = lean_alloc_ctor(1, 1, 0);
    lean_ctor_set(result, 0, lean_mk_string(value));
    return result;
}

static bool take_value(int argc, char **argv, int *index, const char **out) {
    if (*index + 1 >= argc) {
        return false;
    }
    *out = argv[++*index];
    return true;
}

static bool parse_args(int argc, char **argv, struct parsed *out) {
    memset(out, 0, sizeof(*out));
    for (int i = 1; i < argc; ++i) {
        const char *arg = argv[i];
        if (!strcmp(arg, "-D") || !strcmp(arg, "-s") ||
            !strcmp(arg, "-T") || !strcmp(arg, "-M") ||
            !strcmp(arg, "-j")) {
            const char *ignored;
            if (!take_value(argc, argv, &i, &ignored)) return false;
        } else if (!strncmp(arg, "-D", 2) && strlen(arg) > 2) {
            continue;
        } else if (!strcmp(arg, "-o")) {
            if (!take_value(argc, argv, &i, &out->olean)) return false;
        } else if (!strcmp(arg, "-i")) {
            if (!take_value(argc, argv, &i, &out->ilean)) return false;
        } else if (!strcmp(arg, "-c")) {
            if (!take_value(argc, argv, &i, &out->cfile)) return false;
        } else if (!strcmp(arg, "-b")) {
            if (!take_value(argc, argv, &i, &out->bcfile)) return false;
        } else if (!strcmp(arg, "-R")) {
            if (!take_value(argc, argv, &i, &out->root)) return false;
        } else if (!strcmp(arg, "--setup")) {
            if (!take_value(argc, argv, &i, &out->setup)) return false;
        } else if (!strcmp(arg, "--deps")) {
            out->only_deps = true;
        } else if (!strcmp(arg, "--src-deps")) {
            out->only_src_deps = true;
        } else if (!strcmp(arg, "--json")) {
            out->json = true;
        } else if (!strcmp(arg, "--stats")) {
            out->stats = true;
        } else if (!strcmp(arg, "--run")) {
            out->run = true;
        } else if (arg[0] == '-') {
            fprintf(stderr, "lean recovery wrapper: unsupported option %s\n", arg);
            return false;
        } else if (out->file == NULL) {
            out->file = arg;
        } else {
            fprintf(stderr, "lean recovery wrapper: extra file argument %s\n", arg);
            return false;
        }
    }
    return out->file != NULL;
}

int main(int argc, char **argv) {
    const char *prefix = getenv("LEAN_FIXED_PREFIX");
    if (prefix == NULL) {
        prefix = "/opt/elan/toolchains/leanprover--lean4---v4.22.0";
    }
    if (argc == 2 && (!strcmp(argv[1], "-v") || !strcmp(argv[1], "--version"))) {
        puts("Lean (version 4.22.0, x86_64-unknown-linux-gnu, commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)");
        return 0;
    }
    if (argc == 2 && !strcmp(argv[1], "--print-prefix")) {
        puts(prefix);
        return 0;
    }
    if (argc == 2 && !strcmp(argv[1], "--print-libdir")) {
        printf("%s/lib/lean\n", prefix);
        return 0;
    }

    struct parsed parsed;
    if (!parse_args(argc, argv, &parsed)) {
        return 1;
    }

    lean_setup_args(argc, argv);
    lean_initialize();
    lean_set_panic_messages(false);
    lean_object *initialized = initialize_Lean_Shell(1, lean_io_mk_world());
    if (lean_io_result_is_error(initialized)) {
        lean_io_result_show_error(initialized);
        lean_dec(initialized);
        return 1;
    }
    lean_dec(initialized);
    lean_object *options_initialized =
        initialize_Lean_Data_Options(1, lean_io_mk_world());
    if (lean_io_result_is_error(options_initialized)) {
        lean_io_result_show_error(options_initialized);
        lean_dec(options_initialized);
        return 1;
    }
    lean_dec(options_initialized);
    fprintf(stderr, "lean recovery wrapper: globals kv=%p options=%p\n",
            (void *)l_Lean_KVMap_empty, (void *)l_Lean_Options_empty);
    fprintf(stderr, "lean recovery wrapper: initialize search path\n");
    lean_object *path_result = l_Lean_initSearchPath(
        lean_mk_string(prefix), lean_box(0), lean_io_mk_world());
    if (lean_io_result_is_error(path_result)) {
        lean_io_result_show_error(path_result);
        lean_dec(path_result);
        return 1;
    }
    lean_dec(path_result);
    fprintf(stderr, "lean recovery wrapper: invoke frontend\n");
    lean_set_panic_messages(true);
    lean_io_mark_end_initialization();
    lean_init_task_manager();

    lean_object *arguments[18] = {
        mk_list1(parsed.file),
        lean_box(0),
        lean_box(parsed.only_deps),
        lean_box(parsed.only_src_deps),
        lean_box(0),
        mk_empty_options(),
        lean_box_uint32(0),
        mk_optional_string(parsed.root),
        mk_optional_string(parsed.setup),
        mk_optional_string(parsed.olean),
        mk_optional_string(parsed.ilean),
        mk_optional_string(parsed.cfile),
        mk_optional_string(parsed.bcfile),
        lean_box(parsed.json),
        lean_mk_empty_array(),
        lean_box(parsed.stats),
        lean_box(parsed.run),
        lean_io_mk_world(),
    };
    lean_object *result =
        l___private_Lean_Shell_0__Lean_shellMain___boxed(arguments);

    lean_finalize_task_manager();
    if (lean_io_result_is_error(result)) {
        lean_io_result_show_error(result);
        lean_dec(result);
        return 1;
    }
    uint32_t code = lean_unbox_uint32(lean_io_result_get_value(result));
    lean_dec(result);
    return (int)code;
}
