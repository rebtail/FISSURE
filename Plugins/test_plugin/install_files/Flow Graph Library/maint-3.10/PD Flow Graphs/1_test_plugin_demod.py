source_file.js:1
<?xml version="1.0"?>
^

SyntaxError: Unexpected token <
    at Module._compile (internal/modules/cjs/loader.js:723:23)
    at Object.Module._extensions..js (internal/modules/cjs/loader.js:789:10)
    at Module.load (internal/modules/cjs/loader.js:653:32)
    at tryModuleLoad (internal/modules/cjs/loader.js:593:12)
    at Function.Module._load (internal/modules/cjs/loader.js:585:3)
    at Function.Module.runMain (internal/modules/cjs/loader.js:831:12)
    at startup (internal/bootstrap/node.js:283:19)
    at bootstrapNodeJSCore (internal/bootstrap/node.js:622:3)
Process finished with exit code 1.#!/usr/bin/python3
# test file for install/uninstall

def print_message():
    print('Hello Plugin!')

if __name__ == '__main__':
    print_message()
