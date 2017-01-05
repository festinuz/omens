# omens
###### Handy python wrapper for asynchonous functions
---------------------

Omens can be used to simplify programming in asynchonous way by building an abstraction on top of it. 
Example:
```python
>>> future = asyncio.ensure_future(async_get_dictionary())
>>> asyncio.get_event_loop().run_until_complete(future)
>>> result = future.result()
>>> print(result)
{'foo': 'bar'}


# all the code above is equivalent to this:

>>> result = AsyncioOmen(async_get_dictionary())
>>> print(result)
{'foo': 'bar'}
```

When you wrap awaitable function in omen, you can assume that omen is a response from that function. On the first call to the omen, wrapped function will be awaited, after which omen will behave almost exactly like a variable returned.

The only substantional difference you need to remember, is that you're still working with an omen. This affects two functions: **isinstance** and **type**:

```python
>>> print(isinstance(result, dict))
False
>>> print(type(result))
<class '__main__.AsyncioOmen'>
```
