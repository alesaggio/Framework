from itertools import imap, chain
from functools import wraps

__all__ = ("deptracker",)

class deptracker(object):
    """
    Basic dependency tracking for member methods of an object, using a decorator class

    The member methods can e.g. be decorated as follows:
    >>> @deptracker(before=("create", "eleSmear"), after="eleReg", performs=("eleSmear", "correction"))
    >>> def applyElectronSmearing(self):
    >>>     ...

    which will, when calling this method, check that no member method with `@deptracker(..., performs=("create"))`
    nor `@deptracker(..., performs=("eleSmear"))` has been called yet, and
    that a method with `@deptracker(..., performs=("eleReg", ...))` has been called.
    Furthermore, this will mark "eleSmear" and "correction" as "done", such that no other method
    with either of these in "before" can be called after (for "eleSmear": including this method;
    putting the same tag in "before" and "after" ensures that a method is called no more than once).

    This is implemented using a "__trackers" dictionary that is added to the object's attributes.
    """
    def __init__(self, before=None, after=None, performs=None, fallback=None):
        self.before   = deptracker._parse_names(before  )
        self.after    = deptracker._parse_names(after   )
        self.performs = deptracker._parse_names(performs)
        self.fallback = fallback
    @staticmethod
    def _parse_names(arg):
        from itertools import imap
        names = tuple()
        if isinstance(arg, str):
            names = (arg,)
        elif hasattr(arg, "__iter__"):
            names = arg
        return tuple(imap(deptracker._varName, names))
    @staticmethod
    def _varName(name):
        return "__{}_done".format(name)
    @staticmethod
    def _actionName(varName):
        return varName[2:-5]

    def checkInit(self, obj):
        """ ensure that the tracker dictionary is there, and our keys are present """
        if not hasattr(obj, "_trackers"):
            setattr(obj, "_trackers", dict())
        from itertools import chain
        for nm in chain(self.before, self.after, self.performs):
            if nm not in obj._trackers:
                obj._trackers[nm] = False
    @staticmethod
    def isDone(obj, name):
        """ has this action been performed for this instance? """
        return obj._trackers[name]
    @staticmethod
    def setDone(obj, name):
        """ mark this action done for this instance """
        obj._trackers[name] = True

    def __call__(deco, func):
        @wraps(func)
        def func_wrapper(*args, **kwargs):
            self = args[0]
            deco.checkInit(self)
            if any(deco.isDone(self, step) for step in deco.before):
                if deco.fallback:
                    return deco.fallback(*args, **kwargs)
                raise RuntimeError("Method {0} called after performing {1}".format(func.__name__
                    , ", ".join(deptracker._actionName(step) for step in deco.before if deco.isDone(self, step))
                    ))
            if any(not deco.isDone(self, step) for step in deco.after):
                if deco.fallback:
                    return deco.fallback(*args, **kwargs)
                raise RuntimeError("Method {0} called before performing {1}".format(func.__name__
                    , ", ".join(deptracker._actionName(step) for step in deco.after if not deco.isDone(self, step))
                    ))

            ret = func(*args, **kwargs)

            for nm in deco.performs:
                deco.setDone(self, nm)

            return ret
        return func_wrapper
