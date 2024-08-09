Project 2: Advanced Data Structures with Programmatically
Generated Classes
background
As you have learned from previous lectures, we can overload operators to customize our
classes, which is a powerful feature as we embark on this project. So this project require
you to design and implement a complex data structure that integrates dynamically generated named tuples with an advanced dictionary list, showcasing skills in class design,
operator overloading, iterators, and string manipulation in Python.
requirement
Create a module called mynamedtuple.py to handle all the following work.
Create a function mynamedtuple that generates customized namedtuple classes dynamically.
Details
The function header is:
def mynamedtuple(type name, field names, mutable=False, defaults={}):
pass
An example to call this is coordinate = mynamedtuple(’coordinate’, [’x’,’y’], mutable=False)
Typically, a mynamedtuple can include any number of field names, and it’s crucial to
maintain the sequence of these names in subsequent code (as illustrated in the init
header below). For instance, coordinate = mynamedtuple(’coordinate’, ’x,y’) signifies
something different from coordinate = mynamedtuple(’coordinate’, ’y,x’), despite both
having identical field names. The difference in their order matters because certain methods rely on this specific arrangement.
The type and field names must begin with a letter and can be followed by any combination of letters, digits, or underscores. Additionally, they must not conflict with Python
keywords. You can check against a list of Python keywords, which is available as kwlist
from the keyword module.
The parameters should be structured as follows:
1. type name should conform to the naming rules outlined above.
2. field names can either be a list of valid names or a single string where names are
separated by spaces or commas, or a combination of both. For example, field names
1
can be specified as [’x’, ’y’], ’x y’, or ’x, y’. Duplicate names should be ignored, using
a method to filter out duplicates as described in the course notes.
3. If any names are invalid, a SyntaxError should be raised with a relevant message.
defaults should be a dictionary where keys are field names and values are their
corresponding default values. This association is important and will be elaborated
upon in the init definition. If any keys in the defaults dictionary do not match
the field names, a SyntaxError should be raised with an appropriate message.
Important: The main job of this function is to compute a large string that describes the
class and then return the class object it represents. You will not writing a class in the function!!! Because it is dynamically generated and that’s what we mean a program writes
program.
To implement the coordinate class:
class coordinate:
_fields = [’x’,’y’]
_mutable = False
Next, define an init method that has all the field names as parameters (in the order they appear in the second argument to mynamedtuple) and initializes every instance
name (using these same names) with the value bound to its parameter.
def __init__(self, x, y):
self.x = x
self.y = y
SO in your string manipulation, it will be
" def __init__(self, x, y):\n self.x = x\n self.y = y\n"
Finally, in the definition of init , include each field name that appears as a key in
the defaults dictionary as a parameter, assigning it the specified default value. For instance, if you define a mynamedtuple like coordinate = mynamedtuple(’coordinate’, ’x
y’, defaults=’y’: 0), the corresponding init method should be formatted as follows: def
init (self, x, y=0):. This ensures that any default values are correctly applied when the
namedtuple is instantiated.
Define a repr method that returns a string, which when passed to eval returns a
newly constructed object that has all the same instance names and values(==) as the object repr was called on. For coordinate, if we defined origin = coordinate(0,0) then
calling repr(origin) would return ’coordinate(x=0,y=0)’.
Define straightforward query/accessor methods for each field name in the namedtuple. The naming convention for these methods should begin with get followed by the
field name. For instance, for a namedtuple called coordinate, you would implement two
such methods:
2
def get_x(self):
return self.x
def get_y(self):
return self.y
Overloading proper method to overload the indexing operator for this class: an index
of 0 returns the value of the first field name in the field names list; an index of 1 returns
the value of the second field name in the field names list, etc. So if I have the above origin:
origin[0] # -> this gives me 0
Next: Overload the == operator so that it returns True when the two named tuples
come from the same class and have all their name fields bound to equal values
Next: Define the asdict method, which takes no arguments; it returns the mynamedtuple as a dict of names associated with their values. In the case of origin above, calling
origin. asdict() should return a dictionary with ’x’: 0, ’y’: 0
Also, define the make method, which takes one iterable argument (and no self argument: the purpose of make is to make a new object; see how it is called below); it returns
a new object whose fields (in the order they were specified) are bound to the values in the
interable (in that same order). For example, if we called coordinate. make((0,1)) the result
returned is a new coordinate object whose x attribute is bound to 0 and whose y attribute
is bound to 1.
Next: Define a replace method, which takes **kargs as a parameter. This allows the
name kargs to be used in the method as a dict of parameter names and their matching
argument values. The semantics of the replace method depends on the value stored in
the instance name self. mutable:
1. If True, the instance names of the object it is called on are changed and the method
returns None. So, if origin = coordinate(0,0) and we call origin. replace(y=5), then
print(origin) would display as coordinate(x=0,y=5) because origin is mutated.
2. If False, it returns a new object of the same class, whose instance name’s values are
the same, except for those specified in kargs. So, if origin = coordinate(0,0) and we
call new origin = origin. replace(y=5), then print(origin,new origin) would display
as coordinate(x=0,y=0) coordinate(x=0,y=5) because origin is not mutated.
Define the setattr method so after init finishes, if the mutable parameter is False,
the named tuple will not allow any instance names to be changed: it will raise an AttributeError with an appropriate message. (Do not attempt this one unless you have all other
methods working)
3
example useage
coordinate = mynamedtuple(’coordinate’, ’x y’)
p = coordinate(0, 0)
print(p) # coordinate(x=0,y=0)
print(p._asdict()) #{’x’: 0, ’y’: 0}
So we are done with our program write its own program. The following step is to
define an class that can store, handle, and munipulated this customized tuple.
Define a class called DictTuple that manages Tuples with keys and supports operator
overloading.
Some sample usage:
coordinate = mynamedtuple(’coordinate’, ’x y’)
d = DictTuple({’c1’: coordinate(1, 2)}, {’c1’: coordinate(3, 4)})
print(d)
Define an init method that has one parameter: it matches one or more arguments,
where each argument is expected to be a dictionary. See the example above, which creates
a DictTuple object with two dictionaries.
If there are no dictionaries or if any argument is not a dictionary, or if any dictionary is
empty, this method must raise an AssertionError exception with an appropiate message.
For example, in my code writing DictTuple(1) raises AssertionError with the message
DictTuple. init : 1 is not a dictionary.
It’s crucial to use the attribute name self.dt to store the list of dictionaries passed as arguments to the class. This attribute name is referenced in some test files, so it’s important
to maintain consistency. Only this attribute should be stored within the class; no other
instance variables should be defined.
Define a len method that returns the number of distinct keys so in the above example it will return 1.
Define a bool method that returns False if the object stores only one dictionary; it
returns True if it stores more than one dictionary.
Define a repr method for the DictTuple class that returns a string representation
of the object. This string, when executed with eval, should reconstruct a DictTuple instance with identical dictionary arguments as the original object on which repr was
called. The order of keys and values in each dictionary does not affect the outcome due
to dictionary properties in Python. For the above example it should return the string:
"DictTuple({’p1’: coordinate(1, 2)}, {’p1’: coordinate(3, 4)})"
4
Define a contains method so that in returns whether or not its first argument is a
key in any of the dictionaries in a DictTuple; it returns True if such a key is in any dictionary and False if such a key is not in any of the dictionaries.
Define a proper method so that calling d[k] on DictTuple d returns the value associated
with the latest dictionary (the one with the highest index) in d’s list that has k as a key.
If the key is in no dictionaries in the list, this method must raise the KeyError exception
with an appropriate message.
For example, if call
d["p1"] # -> return to the coordinate of coordinate(3, 4)
d["origin"] # -> raise error
Define a proper method so that executing d[k] = v on DictTuple d works as follows:
1. If the key k exists in one or more dictionaries, update its value to v only in the
dictionary where k appears last (the one with the highest index). The total number
of dictionaries should remain unchanged.
2. If k does not exist in any dictionary, add a new dictionary to the end of the list that
contains a single entry: k associated with v. This addition will increase the number
of dictionaries in the list by one.
Define a proper method so that executing del d[k] on DictTuple d works as follows:
1. if k is in at least one dictionary, then delete all k from all dictionaries
2. if k is not in any dictionaries, then raise a KeyError exception with an appropriate
message.
Define a proper method so that call d(k) on DictTuple d works as follows:
1. if k is in at least one dictionary, return a list of all values that associate with K in a
format of list
2. if k is not in any dictionary, then return an empty list
For example, if call
d("p1") # -> return [[1,2], [3,4]]
d("origin") # -> return []
Define an iter method so that it produces keys such that: Each key is produced
only once, from the last (highest) index dictionary in which it appears and all the keys in
each dictionary are produced in alphabetically sorted order.
Define the == operator for comparing two DictTuples or for comparing a DictTuple
and a dict for equality. We define the meaning of d1 == d2 as follows:
5
1. The keys in the left operand are the same as the keys in the right operand. Here, the
keys in a DictTuple are all the keys appearing in any of the its dictionaries; the keys
in a dict operand are all the keys in that dictionary.
2. For all of the keys k computed above, d1[k] == d2[k]. [k] in a DictTuple is the value
associated with k in the latest dictionary (the one with the highest index in the list);
[k] in a dict is the value associated with key k .
Define adding two DictTuples and adding a DictTuple and a dict as follows.
1. To add two DictTuples, create a new DictTuple with a list of dictionaries that contains a copy of all the dicts in the left DictTuple operand (in order) followed by a
copy of all the dicts in the right DictTuple operand (in order). For example,
d1 = DictTuple({’c1’: coordinate(1, 2)}, {’c1’: coordinate(3, 4)})
d2 = DictTuple({’c2’: coordinate(1, 2)}, {’c3’: coordinate(3, 4)})
d1+d2 - > DictTuple({’c1’: coordinate(1, 2)},
{’c1’: coordinate(3, 4)},{’c2’: coordinate(1, 2)},
{’c3’: coordinate(3, 4)})
d2+d1 -> DictTuple({’c2’: coordinate(1, 2)},
{’c3’: coordinate(3, 4)}, {’c1’: coordinate(1, 2)},
{’c1’: coordinate(3, 4)})
(So addition is not commutative for the DictTuple class: d1+d2 produces a different
result than d2+d1.)
2. To add DictTuple + dict, create a new DictTuple with a list of dictionaries that contains a copy of all the dicts in the DictTuple operand (in order) followed by a copy
of the dict operand. For example,
adt = DictTuple({’c1’: coordinate(1, 2)}, {’c1’: coordinate(3, 4)})
adict = {’c3’: coordinate(3, 4)}
adt+adict ->
DictTuple({’c1’: coordinate(1, 2)}, {’c1’: coordinate(3, 4)},
{’c3’: coordinate(3, 4)})
3. To add dict + DictTuple, create a new DictTuple with a list of dictionaries that contains a copy of dict operand followed a copy of all the dicts in the DictTuple operand
(in order). For example,
adt = DictTuple({’c1’: coordinate(1, 2)}, {’c1’: coordinate(3, 4)})
adict = {’c3’: coordinate(3, 4)}
adict + adt ->
DictTuple({’c3’: coordinate(3, 4)}, {’c1’: coordinate(1, 2)},
{’c1’: coordinate(3, 4)})
6
4. If the right operand isn’t a a DictTuple or a dict, raise TypeError with an appropriate
message.
Define a setattr method that ensures objects in the DictTuple class cannot store new
attributes: they store only dt. The methods you will write should never bind any instance
names (except in init , which initializes dt) but exclusively returns newly constructed
DictTuple objects with the correct values. If an attempt is made to add new attributes to
an object (by defining a new attribute or rebinding an existing attribute), raise an AssertionError with an appropriate message. (Do not attempt this method unless you have all
above finished and working)
Store this class in DictTuple.py.
7
