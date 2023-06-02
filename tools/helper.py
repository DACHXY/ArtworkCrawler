import inspect

def get_variable_name(variable):
    frame = inspect.currentframe()
    try:
        for frame in iter(lambda: frame.f_back, None):
            frame_locals = frame.f_locals
            for name in frame_locals:
                if frame_locals[name] is variable:
                    return name
    finally:
        del frame
        
def get_sub_class_names(module):
    return [cls.__name__ for cls in module.__subclasses__()]

def get_sub_classes(module):
    return [cls for cls in module.__subclasses__()]