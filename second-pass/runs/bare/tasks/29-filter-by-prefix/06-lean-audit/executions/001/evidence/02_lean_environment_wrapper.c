#include <lean/lean.h>
#include <stdbool.h>
#include <ctype.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

extern char **lean_setup_args(int argc, char **argv);
extern void lean_initialize(void);
extern lean_object *initialize_Lean(uint8_t builtin, uint8_t world);
extern lean_object *lean_shell_main(
    lean_object *args,
    uint8_t use_stdin,
    uint8_t only_deps,
    uint8_t only_src_deps,
    uint8_t deps_json,
    lean_object *opts,
    uint32_t trust_level,
    lean_object *root_dir,
    lean_object *setup_file,
    lean_object *olean_file,
    lean_object *ilean_file,
    lean_object *c_file,
    lean_object *bc_file,
    uint8_t json_output,
    lean_object *error_on_kinds,
    uint8_t print_stats,
    uint8_t run,
    lean_object *world
);
extern lean_object *l_Lean_KVMap_setNat(
    lean_object *options, lean_object *name, lean_object *value
);
extern lean_object *l_Lean_KVMap_setBool(
    lean_object *options, lean_object *name, uint8_t value
);
extern lean_object *lean_name_mk_string(
    lean_object *prefix, lean_object *component
);
extern lean_object *l_Lean_initSearchPath(
    lean_object *sysroot, lean_object *initial, lean_object *world
);

static int show_init_error(lean_object *result) {
    lean_io_result_show_error(result);
    lean_dec(result);
    return 1;
}

static lean_object *some_string(const char *value) {
    lean_object *some = lean_alloc_ctor(1, 1, 0);
    lean_ctor_set(some, 0, lean_mk_string(value));
    return some;
}

static lean_object *set_option(
    lean_object *options, const char *assignment
) {
    while (isspace((unsigned char)*assignment)) {
        ++assignment;
    }
    const char *equal = strchr(assignment, '=');
    size_t length = equal ? (size_t)(equal - assignment) : strlen(assignment);
    while (length > 0 && isspace((unsigned char)assignment[length - 1])) {
        --length;
    }
    char *name_text = malloc(length + 1);
    memcpy(name_text, assignment, length);
    name_text[length] = '\0';
    lean_object *name = lean_name_mk_string(
        lean_box(0), lean_mk_string(name_text)
    );
    free(name_text);
    const char *value = equal ? equal + 1 : "true";
    if (strcmp(value, "true") == 0 || strcmp(value, "false") == 0) {
        return l_Lean_KVMap_setBool(
            options, name, strcmp(value, "true") == 0
        );
    }
    char *end = NULL;
    unsigned long parsed = strtoul(value, &end, 10);
    if (end != value && *end == '\0') {
        return l_Lean_KVMap_setNat(options, name, lean_box(parsed));
    }
    fprintf(stderr, "unsupported Lean option value: %s\n", assignment);
    exit(2);
}

int main(int argc, char **argv) {
    if (argc == 2 && strcmp(argv[1], "--version") == 0) {
        puts("Lean (version 4.22.0, x86_64-unknown-linux-gnu, "
             "commit ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05, Release)");
        return 0;
    }
    if (argc == 2 && strcmp(argv[1], "--githash") == 0) {
        puts("ba2cbbf09d4978f416e0ebd1fceeebc2c4138c05");
        return 0;
    }
    if (argc == 2 && strcmp(argv[1], "--print-prefix") == 0) {
        const char *root = getenv("LEAN_SYSROOT");
        puts(root ? root : "/opt/elan/toolchains/leanprover--lean4---v4.22.0");
        return 0;
    }

    lean_object *options = lean_box(0);
    lean_object *root_dir = lean_box(0);
    lean_object *setup_file = lean_box(0);
    lean_object *olean_file = lean_box(0);
    lean_object *ilean_file = lean_box(0);
    lean_object *c_file = lean_box(0);
    lean_object *bc_file = lean_box(0);
    bool json_output = false;
    uint32_t trust_level = 0;
    const char *input_file = NULL;
    for (int index = 1; index < argc; ++index) {
        const char *arg = argv[index];
        if (strcmp(arg, "-D") == 0 && index + 1 < argc) {
            options = set_option(options, argv[++index]);
        } else if (strncmp(arg, "-D", 2) == 0) {
            options = set_option(options, arg + 2);
        } else if (
            (strcmp(arg, "-s") == 0 || strcmp(arg, "-j") == 0 ||
             strcmp(arg, "-M") == 0 || strcmp(arg, "-T") == 0) &&
            index + 1 < argc
        ) {
            ++index;
        } else if (
            (strcmp(arg, "-t") == 0 || strcmp(arg, "--trust") == 0) &&
            index + 1 < argc
        ) {
            trust_level = (uint32_t)strtoul(argv[++index], NULL, 10);
        } else if (
            (strcmp(arg, "-o") == 0 || strcmp(arg, "--o") == 0) &&
            index + 1 < argc
        ) {
            olean_file = some_string(argv[++index]);
        } else if (strcmp(arg, "-i") == 0 && index + 1 < argc) {
            ilean_file = some_string(argv[++index]);
        } else if (strcmp(arg, "-c") == 0 && index + 1 < argc) {
            c_file = some_string(argv[++index]);
        } else if (
            (strcmp(arg, "-b") == 0 || strcmp(arg, "--bc") == 0) &&
            index + 1 < argc
        ) {
            bc_file = some_string(argv[++index]);
        } else if (strcmp(arg, "--setup") == 0 && index + 1 < argc) {
            setup_file = some_string(argv[++index]);
        } else if (strncmp(arg, "--setup=", 8) == 0) {
            setup_file = some_string(arg + 8);
        } else if (strcmp(arg, "--root") == 0 && index + 1 < argc) {
            root_dir = some_string(argv[++index]);
        } else if (strncmp(arg, "--root=", 7) == 0) {
            root_dir = some_string(arg + 7);
        } else if (strcmp(arg, "--json") == 0) {
            json_output = true;
        } else if (arg[0] == '-') {
            fprintf(stderr, "unsupported Lean argument: %s\n", arg);
            return 2;
        } else if (input_file == NULL) {
            input_file = arg;
        } else {
            fprintf(stderr, "unexpected Lean input: %s\n", arg);
            return 2;
        }
    }
    if (input_file == NULL) {
        fprintf(stderr, "no Lean input file\n");
        return 2;
    }

    const char *sysroot = getenv("LEAN_SYSROOT");
    if (sysroot != NULL) {
        const char *existing = getenv("LEAN_PATH");
        size_t needed = strlen(sysroot) + strlen("/lib/lean") + 1;
        if (existing != NULL && *existing != '\0') {
            needed += strlen(existing) + 1;
        }
        char *search_path = malloc(needed);
        if (existing != NULL && *existing != '\0') {
            snprintf(
                search_path, needed, "%s:%s/lib/lean", existing, sysroot
            );
        } else {
            snprintf(search_path, needed, "%s/lib/lean", sysroot);
        }
        setenv("LEAN_PATH", search_path, 1);
        free(search_path);
    }

    argv = lean_setup_args(argc, argv);
    lean_initialize();
    lean_set_panic_messages(false);
    lean_object *initialized = initialize_Lean(1, 1);
    lean_set_panic_messages(true);
    lean_io_mark_end_initialization();
    if (lean_io_result_is_error(initialized)) {
        return show_init_error(initialized);
    }
    lean_dec(initialized);
    const char *search_root = getenv("LEAN_SYSROOT");
    if (search_root == NULL) {
        search_root = "/opt/elan/toolchains/leanprover--lean4---v4.22.0";
    }
    initialized = l_Lean_initSearchPath(
        lean_mk_string(search_root), lean_box(0), lean_io_mk_world()
    );
    if (lean_io_result_is_error(initialized)) {
        return show_init_error(initialized);
    }
    lean_dec(initialized);
    lean_init_task_manager();

    lean_object *args = lean_alloc_ctor(1, 2, 0);
    lean_ctor_set(args, 0, lean_mk_string(input_file));
    lean_ctor_set(args, 1, lean_box(0));
    lean_object *result = lean_shell_main(
        args,
        false,
        false,
        false,
        false,
        options,
        trust_level,
        root_dir,
        setup_file,
        olean_file,
        ilean_file,
        c_file,
        bc_file,
        json_output,
        lean_mk_empty_array(),
        false,
        false,
        lean_io_mk_world()
    );
    int exit_code;
    if (lean_io_result_is_error(result)) {
        lean_io_result_show_error(result);
        exit_code = 1;
    } else {
        exit_code = (int)lean_unbox(lean_io_result_get_value(result));
    }
    lean_dec(result);
    lean_finalize_task_manager();
    return exit_code;
}
