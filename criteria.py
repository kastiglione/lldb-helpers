import re
import __builtin__
from itertools import islice

# These functions are for adding breakpoint criteria. They are useful for
# constraining when a breakpoint stops, for example only stopping when called
# by this function or from that library.
#
# These helper functions make use of a subtle behavior of breakpoint commands.
# A breakpoint function that returns False tells lldb to continue running the
# process. Think of False as "No, don't stop".
#
# These functions were inspired by:
# https://sourceware.org/gdb/current/onlinedocs/gdb/Convenience-Funs.html

# breakpoint command add -F 'caller_is("theCaller")'
# breakpoint command add -F 'not caller_is("theCaller")'
def caller_is(name):
    def check(frame, loc, _):
        return frame.parent.name == name
    return check
__builtin__.caller_is = caller_is

# breakpoint command add -F 'any_caller_is("someCaller")'
# breakpoint command add -F 'not any_caller_is("someCaller")'
def any_caller_is(name):
    def check(frame, loc, _):
        callers = islice(frame.thread, 1, None) # skip current frame
        return any(f.name == name for f in callers)
    return check
__builtin__.any_caller_is = any_caller_is

# breakpoint command add -F 'caller_matches("theCaller")'
# breakpoint command add -F 'not caller_matches("theCaller")'
def caller_matches(pattern):
    regex = re.compile(pattern, re.I)
    def check(frame, loc, _):
        return regex.search(frame.parent.name) != None
    return check
__builtin__.caller_matches = caller_matches

# breakpoint command add -F 'any_caller_matches("someCaller")'
# breakpoint command add -F 'not any_caller_matches("someCaller")'
def any_caller_matches(pattern):
    regex = re.compile(pattern, re.I)
    def check(frame, loc, _):
        callers = islice(frame.thread, 1, None) # skip current frame
        return any(regex.search(f.name) for f in callers)
    return check
__builtin__.any_caller_matches = any_caller_matches

# breakpoint command add -F 'caller_from("thatLibrary")'
# breakpoint command add -F 'not caller_from("thatLibrary")'
def caller_from(name):
    def check(frame, loc, _):
        return frame.parent.module.file.basename == name
    return check
__builtin__.caller_from = caller_from

# breakpoint command add -F 'any_caller_from("thatLibrary")'
# breakpoint command add -F 'not any_caller_from("thatLibrary")'
def any_caller_from(name):
    def check(frame, loc, _):
        callers = islice(frame.thread, 1, None) # skip current frame
        return any(f.module.file.basename == name for f in callers)
    return check
__builtin__.any_caller_from = any_caller_from
