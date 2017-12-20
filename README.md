# liquify
### An Object should know how it should be represented. So let it.

liquify is a python script that reduces a class to a dictionary for JSON conversion.

The idea behind this package is to allow the knowledge of an Object's representation to live within the context of the Object itself.

### The Benefits
* Reuse & Recycle
  * Forget the days of having three separate functions that all convert the same Object to a dictionary because none of the contributors of your package found the previous function.
  * Having a one stop shop for the basic representation of data allows us to implement this OOP design pattern
* Skinny views
  * Abstracting the layout of the representation onto an Object allows for us to have simpler, more minimal views (which is how views should be)


## Examples
Without liquify:
```python
# models.py
class Artist:
  def __init__(self, first, last):
    self.first = first
    self.last = last

class Instrument:
  saxophone = [Artist("John", "Coltrane"), Artist("Ornette", "Coleman")]
  trumpet = [Artist("Miles", "Davis")]
  
  
# views.py
def get_instruments(request):
  instrument = Instrument()
  instrument_dict = dict(
    saxophone=list("{} {}".format(artist.first, artist.last) for artist in instrument.saxophone),
    trumpet=list("{} {}".format(artist.first, artist.last) for artist in instrument.trumpet)
  )
  return JsonResponse(instrument_dict)
```

With liquify:
```python
# models.py
class Artist:
  __liquify__ = ["first_name", "last_name"]
  
  def __init__(self, first_name, last_name):
    self.first_name = first_name
    self.last_name = last_name

class Instrument:
  saxophone = [Artist("John", "Coltrane"), Artist("Ornette", "Coleman")]
  trumpet = [Artist("Miles", "Davis")]
  
  __liquify__ = ["saxophone", "trumpet"]
  
  
# views.py
def get_instruments(request):
  return JsonResponse(liquify(Instrument()))
```

### Limitations
This is general purpose. Sometimes you will need to manually create dictionaries for Objects. This is not an end-all automated solution to preparing Python objects for a neutral format.

This package will only convert an Object to a dictionary. This will **not** create a json object--there exist plenty of options for converting Python dictionaries to JSON format.

Because we are only in the business of reducing Objects to dictionaries, any issue that you encounter in JSON conversion will *most likely* lie within the package that you are using for the conversion.
