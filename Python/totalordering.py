def total_ordering(cls):
      """Class decorator that fills in missing ordering methods"""
      convert = {
          '__lt__': [('__gt__', lambda self, other: other < self),
                     ('__le__', lambda self, other: not other < self),
                     ('__ge__', lambda self, other: not self < other)],
          '__le__': [('__ge__', lambda self, other: other <= self),
                     ('__lt__', lambda self, other: not other <= self),
                     ('__gt__', lambda self, other: not self <= other)],
          '__gt__': [('__lt__', lambda self, other: other > self),
                     ('__ge__', lambda self, other: not other > self),
                     ('__le__', lambda self, other: not self > other)],
          '__ge__': [('__le__', lambda self, other: other >= self),
                     ('__gt__', lambda self, other: not other >= self),
                     ('__lt__', lambda self, other: not self >= other)]
      }
      roots = set(dir(cls)) & set(convert)
     
      if not roots:
          raise ValueError('must define at least one ordering operation: < > <= >=')
      root = max(roots)       # prefer __lt__ to __le__ to __gt__ to __ge__
      for opname, opfunc in convert[root]:
          if opname not in roots:
              opfunc.__name__ = opname
              opfunc.__doc__ = getattr(int, opname).__doc__
              setattr(cls, opname, opfunc)
      return cls

@total_ordering
class Student:
    def __init__(self,lastname,firstname):
        self.lastname = lastname
        self.firstname = firstname

    def __eq__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) ==
                (other.lastname.lower(), other.firstname.lower()))
    def __lt__(self, other):
        return ((self.lastname.lower(), self.firstname.lower()) <
                (other.lastname.lower(), other.firstname.lower()))

St1 = Student("li","zue")
St2 = Student("li","yan")

print St1 >= St2
