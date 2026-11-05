import functools


# def custom_decorator_name(func_passed_as_arg):
#     @functools.wraps(func_passed_as_arg)
#     def decorator_wrapper(*args, **kwargs):
#         # Code block runs before (or instead of) the wrapped function
#         return func_passed_as_arg(*args, **kwargs)

#     return decorator_wrapper


# @custom_decorator_name
# def func_name(*args, **kwargs):
#     # Function body
#     pass


# func_name(any_and_as_many_args)


# def print_args(*args):
#     return args

# def print_kwargs(**kwargs):
#     return kwargs

# def print_args_kwargs(*args, **kwargs):
#     print(args)
#     print(kwargs)


# print(print_args(1, 2, 3, 4))
# print()
# print(print_kwargs(kwarg1=1, kwarg2=2, kwarg3=3))
# print()
# print_args_kwargs(1, 2, 3, 4, kwarg1=1, kwarg2=2)

# def print_args(func):
#     @functools.wraps(func)
#     def decorator_wrapper(*args, **kwargs):
#         print(func.__name__)

#         for idx, e in enumerate(args):
#             print(f"{idx}: {e}")

#         return func(*args, **kwargs)
#     return decorator_wrapper


# def auth_logged_in(func):
#     @functools.wraps(func)
#     def decorator_wrapper(*args, **kwargs):
#         if logged_in == False:
#             return print("Please login to perform this action.")
#         return func(*args, **kwargs)

#     return decorator_wrapper


# @auth_logged_in
# def sum_num(*args):
#     return sum(list(args))

# @print_args
# def sum_num(*args):
#     return sum(list(args))

# @print_args
# def concatenate_str(*args):
#     return " ".join(args)



# def sum_num(*args):
#     print(sum_num.__name__)

#     for idx, e in enumerate(args):
#         print(f"{idx}: {e}")

#     return sum(list(args))

# def concatenate_str(*args):
#     print(sum_num.__name__)

#     for idx, e in enumerate(args):
#         print(f"{idx}: {e}")

#     return " ".join(args)

# print(sum_num(1,2,3))
# print()
# print(concatenate_str("hello", "I", "am", "Mina"))


def only_strings(func):
    @functools.wraps(func)
    def decorator_wrapper(*args, **kwargs):
        print(args[0])
        new_list = list(args[0])

        for idx, e in enumerate(new_list):
            new_list[idx] = str(e)

        args = (new_list,)
        return func(*args, **kwargs)

    return decorator_wrapper


@only_strings
def string_joined(list_of_strings):
    return ", ".join(list_of_strings), type(list_of_strings)

print(string_joined(["hello", "everyone"]))