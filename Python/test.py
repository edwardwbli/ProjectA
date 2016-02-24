class Descriptor(object):
 
    def __get__(self, instance, owner):
        return self.d_name
 
    def __set__(self, instance, nam):
        self.d_name = nam.title()
 
    def __delete__(self, instance):
        del self.d_name

class Human(object):
    def __init__(self,**kwargs):
      for key in kwargs:
            setattr(self,key,kwargs[key])

    

class Person(Human):
    name = Descriptor()
    sex  = Descriptor()

a = Person(name='edward',sex='man')
print a.name
print a.sex
