<!--
  译者：Github@wizardforcel
-->

# 进行原始的sql查询 #

在*模型查询API*不够用的情况下，你可以使用原始的sql语句。django提供两种方法使用原始sql进行查询：一种是使用**Manager.raw()**方法，*进行原始查询并返回模型实例*；另一种是完全避开模型层，*直接执行自定义的sql语句*。

> **警告**
> 
> 编写原始的sql语句时，应该格外小心。每次使用的时候，都要确保转义了参数中的任何控制字符，以防受到sql注入攻击。更多信息请参阅*防止sql注入*。

## 进行原始查询 ##

**raw()**方法用于原始的sql查询，并返回模型的实例：

```
Manager.raw(raw_query, params=None, translations=None)
```

这个方法执行原始的sql查询之后，返回**django.db.models.query.RawQuerySet**的实例。**RawQuerySet**实例可以像一般的**QuerySet**那样，通过迭代来提供对象的实例。

这里最好通过例子展示一下，假设存在以下模型：

```
class Person(models.Model):
    first_name = models.CharField(...)
    last_name = models.CharField(...)
    birth_date = models.DateField(...)
```

你可以像这样执行自定义的sql语句：

```
>>> for p in Person.objects.raw('SELECT * FROM myapp_person'):
...     print(p)
John Smith
Jane Jones
```

当然，这个例子不是特别有趣，和直接使用**Person.objects.all()**的结果一模一样。但是，**raw()**拥有其它更强大的使用方法。

> **模型表的名称**
> 
> 在上面的例子中，**Person**表的名称是从哪里得到的？
> 
> 通常，Django通过将模型的名称和模型的“应用标签”（你在**manage.py startapp**中使用的名称）进行关联，用一条下划线连接他们，来组合表的名称。在这里我们假定**Person**模型存在于一个叫做**myapp**的应用中，所以表就应该叫做**myapp_person**。
> 
> 更多细节请查看**db_table**选项的文档，它也可以让你自定义表的名称。

> **警告**
> 
> 传递给**raw()**方法的sql语句并没有任何检查。django默认它会返回一个数据集，但这不是强制性的。如果查询的结果不是数据集，则会产生一个错误。

> **警告**
> 
> 如果你在mysql上执行查询，注意在类型不一致的时候，mysql的静默类型强制可能导致意想不到的结果发生。如果你在一个字符串类型的列上查询一个整数类型的值，mysql会在比较前强制把每个值的类型转成整数。例如，如果你的表中包含值**'abc'**和**'def'**，你查询**'where mycolumn=0'**，那么两行都会匹配。要防止这种情况，在查询中使用值之前，要做好正确的类型转换。

> **警告**
> 
> 虽然**RawQuerySet**可以像普通的**QuerySet**一样迭代，**RawQuerySet**并没有实现可以在**QuerySet**上使用的所有方法。例如，**\_\_bool\_\_()**和**\_\_len\_\_()**在**RawQuerySet**中没有被定义，所以所有**RawQuerySet**转化为布尔值的结果都是**True**。**RawQuerySet**中没有实现他们的原因是，在没有内部缓存的情况下会导致性能下降，而且增加内部缓存不向后兼容。

## 将查询字段映射到模型字段 ##

**raw()**方法自动将查询字段映射到模型字段。

字段的顺序并不重要。换句话说，下面两种查询的作用相同：

```
>>> Person.objects.raw('SELECT id, first_name, last_name, birth_date FROM myapp_person')
...
>>> Person.objects.raw('SELECT last_name, birth_date, first_name, id FROM myapp_person')
...
```

Django会根据名字进行匹配。这意味着你可以使用sql的**as**子句来映射二者。所以如果在其他的表中有一些**Person**数据，你可以很容易地把它们映射成**Person**实例。

```
>>> Person.objects.raw('''SELECT first AS first_name,
...                              last AS last_name,
...                              bd AS birth_date,
...                              pk AS id,
...                       FROM some_other_table''')
```

只要名字能对应上，模型的实例就会被正确创建。
又或者，你可以在**raw()**方法中使用翻译参数。翻译参数是一个字典，将表中的字段名称映射为模型中的字段名称、例如，上面的查询可以写成这样：

```
>>> name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
>>> Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)
```

## 索引访问 ##

**raw()**方法支持索引访问，所以如果只需要第一条记录，可以这样写：

```
>>> first_person = Person.objects.raw('SELECT * FROM myapp_person')[0]
```

然而，索引和切片并不在数据库层面上进行操作。如果数据库中有很多的**Person**对象，更加高效的方法是在sql层面限制查询中结果的数量：

```
>>> first_person = Person.objects.raw('SELECT * FROM myapp_person LIMIT 1')[0]
```

## 延迟加载模型字段 ##

字段也可以被省略：

```
>>> people = Person.objects.raw('SELECT id, first_name FROM myapp_person')
```

查询返回的Person对象是一个延迟的模型实例（请见 **defer()**）。这意味着被省略的字段，在访问时才被加载。例如:

```
>>> for p in Person.objects.raw('SELECT id, first_name FROM myapp_person'):
...     print(p.first_name, # This will be retrieved by the original query
...           p.last_name) # This will be retrieved on demand
...
John Smith
Jane Jones
```

从表面上来看，看起来这个查询获取了**first_name**和**last_name**。然而，这个例子实际上执行了3次查询。只有**first_name**字段在**raw()**查询中获取，**last_name**字符按在执行打印命令时才被获取。

只有一种字段不可以被省略，就是主键。Django 使用主键来识别模型的实例，所以它在每次原始查询中都必须包含。如果你忘记包含主键的话，会抛出一个**InvalidQuery**异常。

## 增加注解 ##

你也可以在查询中包含模型中没有定义的字段。例如，我们可以使用**PostgreSQL的age()函数**来获得一群人的列表，带有数据库计算出的年龄。

```
>>> people = Person.objects.raw('SELECT *, age(birth_date) AS age FROM myapp_person')
>>> for p in people:
...     print("%s is %s." % (p.first_name, p.age))
John is 37.
Jane is 42.
...
```

## 向 **raw()** 方法中传递参数 ##

如果你需要参数化的查询，可以向**raw()** 方法传递**params**参数。

```
>>> lname = 'Doe'
>>> Person.objects.raw('SELECT * FROM myapp_person WHERE last_name = %s', [lname])
```

**params**是存放参数的列表或字典。你可以在查询语句中使用**%s**占位符，或者对于字典使用**%(key)**占位符（**key**会被替换成字典中键为key的值），无论你的数据库引擎是什么。这样的占位符会被替换成参数表中正确的参数。

> **注意**
> 
> SQLite后端不支持字典，你必须以列表的形式传递参数。

> **警告**
> 
> 不要在原始查询中使用字符串格式化！
> 
> 它类似于这种样子：
> 
```
>>> query = 'SELECT * FROM myapp_person WHERE last_name = %s' % lname
>>> Person.objects.raw(query)
```
> 使用参数化查询可以完全防止sql注入，一种普遍的漏洞使攻击者可以向你的数据库中注入任何sql语句。如果你使用字符串格式化，早晚会受到sql输入的攻击。只要你记住默认使用参数化查询，就可以免于攻击。

## 直接执行自定义sql ##

有时**Manager.raw()**方法并不十分好用，你不需要将查询结果映射成模型，或者你需要执行**UPDATE**、**INSERT**以及**DELETE**查询。

在这些情况下，你可以直接访问数据库，完全避开模型层。

**django.db.connection**对象提供了常规数据库连接的方式。为了使用数据库连接，调用**connection.cursor()**方法来获取一个游标对象之后，调用**cursor.execute(sql, [params])**来执行sql语句，调用**cursor.fetchone()**或者**curser.fetchall()**来返回结果行。

例如:

```
from django.db import connection

def my_custom_sql(self):
    cursor = connection.cursor()

    cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])

    cursor.execute("SELECT foo FROM bar WHERE baz = %s", [self.baz])
    row = cursor.fetchone()

    return row
```

注意如果你的查询中包含百分号字符，你需要写成两个百分号字符，以便能正确传递参数：

```
cursor.execute("SELECT foo FROM bar WHERE baz = '30%'")
cursor.execute("SELECT foo FROM bar WHERE baz = '30%%' AND id = %s", [self.id])
```

如果你使用了不止一个数据库，你可以使用**django.db.connections**来获取针对特定数据库的连接（以及游标）对象。**django.db.connections**是一个类似于字典的对象，允许你通过它的别名获取特定的连接

```
from django.db import connections
cursor = connections['my_db_alias'].cursor()
# Your code here...
```

通常，Python DB API会返回不带字段的结果，这意味着你需要以一个列表结束，而不是一个字典。花费一点性能之后，你可以返回一个字典形式的结果，像这样：

```
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
        dict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()
    ]
```

下面是一个体现二者区别的例子:

```
>>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2");
>>> cursor.fetchall()
((54360982L, None), (54360880L, None))

>>> cursor.execute("SELECT id, parent_id FROM test LIMIT 2");
>>> dictfetchall(cursor)
[{'parent_id': None, 'id': 54360982L}, {'parent_id': None, 'id': 54360880L}]
```

## 连接和游标 ##

连接和游标主要实现PEP 249中描述的Python DB API标准，除非它涉及到事务处理。

如果你不熟悉Python DB-API，注意**cursor.execute()**中的sql语句使用占位符**"%s"**，而不是直接在sql中添加参数。如果你使用它，下面的数据库会在必要时自动转义你的参数。

也要注意Django使用**"%s"**占位符，而不是SQLite Python绑定的**"?"**占位符。这是一致性和可用性的缘故。

```
Django 1.7中的改变。
```

**PEP 249**并没有说明游标是否可以作为上下文管理器使用。在python2.7之前，游标可以用作上下文管理器，由于魔术方法lookups中意想不到的行为(Python ticket #9220)。Django 1.7 显式添加了对允许游标作为上下文管理器使用的支持。

将游标作为上下文管理器使用:

```
with connection.cursor() as c:
    c.execute(...)
```

等价于：

```
c = connection.cursor()
try:
    c.execute(...)
finally:
    c.close()
```