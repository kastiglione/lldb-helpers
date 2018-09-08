# lldb-helpers

Functions that control when a breakpoint stops. These are especially useful for frequently called functions. The functions are also useful to catch programming mistakes, such as functions being called from the wrong thread.

Inspired by [GDB's convience functions](https://sourceware.org/gdb/current/onlinedocs/gdb/Convenience-Funs.html).

## Breakpoint Criteria

These helper functions place various criteria on a breakpoint. A simple example is to make a breakpoint stop only when called by a certain function.

The types of criteria are:

1. [Caller](#caller)
2. [Stack](#stack)
3. [Threads](#threads)

### Caller

The `caller_is` and `caller_matches` helpers are used to make a breakpoint stop only when called by a specific function. Or, to stop when the caller is _not_ a specific function. Use `caller_is` for an exact caller name, and use `caller_matches` to stop based on substring or regex. Prefix the function with `not` to stop when the caller _does not_ match the name.

Examples:

```
breakpoint command add -F 'caller_is("someFunction")'
breakpoint command add -F 'not caller_is("someFunction")'
breakpoint command add -F 'caller_is("-[SomeClass theMethod:]")'
breakpoint command add -F 'caller_matches("SomeClass")'
```

In some cases, you'll want a breakpoint to stop based on the library (module) of the caller. The `caller_from` helper does just this.

Examples:

```
breakpoint command add -F 'caller_from("UIKit")'
breakpoint command add -F 'not caller_from("MyAppName")'
```

### Stack

The `any_caller_is` and `any_caller_matches` helper functions are just like `caller_is` and `caller_matches`, except they stop if any function in the call stack matches. Use `any_caller_is` to require an exact match with one of the functions in the call stack, and use `any_caller_matches` to stop based on substring or regex. Prefix the function with `not` to stop when the call stack _does not_ contain a matching function.

Examples:

```
breakpoint command add -F 'any_caller_is("someFunction")'
breakpoint command add -F 'not any_caller_is("someFunction")'
breakpoint command add -F 'any_caller_is("-[SomeClass theMethod:]")'
breakpoint command add -F 'any_caller_matches("SomeClass")'
```

When you want a breakpoint to stop when library (module) is or is not in the call stack, use `any_caller_from`.

Examples:

```
breakpoint command add -F 'any_caller_from("UIKit")'
breakpoint command add -F 'not any_caller_from("MyAppName")'
```

### Threads

The `called_on` helper function is used to stop only when a breakpoint is hit from a specific thread or queue. LLDB breakpoints have the ability to specify a specifc thread (`--thread-index`) or queue (`--queue-name`), but there is no way to specify that a breakpoint *not* stop for a specific thread or queue. The `called_on` helper can do this, and takes either a thread index, for example `1` for the main thread, or takes a thread name or queue name.

Examples:

```
breakpoint command add -F 'called_on(1)'
breakpoint command add -F 'not called_on(1)'
breakpoint command add -F 'not called_on("com.banana.eventfetch-thread")'
```

## Installation

1. Clone this repository to your prefrerred location
2. Add this `import` command to your `~/.lldbinit`:

```
command script import ~/path/to/lldb-helpers/criteria.py
```
