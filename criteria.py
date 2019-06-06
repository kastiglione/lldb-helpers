try:
    import __builtin__
except ImportError:
    import builtins
    __builtin__ = builtins
import re
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

def break_criteria(predicate):
    def decorator(*args):
        def breakpoint_command(frame, location, _):
            return predicate(frame, *args)
        return breakpoint_command
    setattr(__builtin__, predicate.__name__, decorator)
    return decorator

# breakpoint command add -F 'caller_is("theCaller")'
# breakpoint command add -F 'not caller_is("theCaller")'
@break_criteria
def caller_is(frame, symbol):
    return frame.parent.name == symbol

# breakpoint command add -F 'any_caller_is("someCaller")'
# breakpoint command add -F 'not any_caller_is("someCaller")'
@break_criteria
def any_caller_is(frame, symbol):
    callers = islice(frame.thread, 1, None) # skip current frame
    return any(f.name == symbol for f in callers)

# breakpoint command add -F 'caller_contains("theCaller")'
# breakpoint command add -F 'not caller_contains("theCaller")'
@break_criteria
def caller_contains(frame, substring):
    return substring in frame.parent.name

# breakpoint command add -F 'any_caller_contains("someCaller")'
# breakpoint command add -F 'not any_caller_contains("someCaller")'
@break_criteria
def any_caller_contains(frame, substring):
    callers = islice(frame.thread, 1, None) # skip current frame
    return any(substring in f.name for f in callers)

_CACHED_REGEX = {}

# breakpoint command add -F 'caller_matches("thisCaller|thatCaller")'
# breakpoint command add -F 'not caller_matches("thisCaller|thatCaller")'
@break_criteria
def caller_matches(frame, pattern):
    global _CACHED_REGEX
    regex = _CACHED_REGEX.get(pattern) or re.compile(pattern)
    return regex.search(frame.parent.name) is not None

# breakpoint command add -F 'any_caller_matches("oneCaller|anotherCaller")'
# breakpoint command add -F 'not any_caller_matches("oneCaller|anotherCaller")'
@break_criteria
def any_caller_matches(frame, pattern):
    global _CACHED_REGEX
    regex = _CACHED_REGEX.get(pattern) or re.compile(pattern)
    callers = islice(frame.thread, 1, None) # skip current frame
    return any(regex.search(f.name) for f in callers)

# breakpoint command add -F 'caller_from("FrameworkKit")'
# breakpoint command add -F 'not caller_from("libThat")'
@break_criteria
def caller_from(frame, module):
    return frame.parent.module.file.basename == module

# breakpoint command add -F 'any_caller_from("FrameworkKit")'
# breakpoint command add -F 'not any_caller_from("libThat")'
@break_criteria
def any_caller_from(frame, module):
    callers = islice(frame.thread, 1, None) # skip current frame
    return any(f.module.file.basename == module for f in callers)

# breakpoint command add -F 'not called_on(1)'
# breakpoint command add -F 'called_on("namedThread")'
@break_criteria
def called_on(frame, thread_id):
    if isinstance(thread_id, int):
        return thread_id == frame.thread.idx
    else:
        return thread_id in (frame.thread.name, frame.thread.queue)
