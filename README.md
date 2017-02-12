# Omens
###### Handy python wrapper for asynchonous functions
---------------------
Onems allow you to benefit from the speed of asynchonous libraries and stay true to your beloved syncronous code style at the same time. This comes handy, for example, when you want to create a little script that does multiple things, but you dont want to overcomplicate it with all that asynchonous mumbo-jumbo.

For example, lets assume that we an important asynchronous function:
```python
async def very_important_function(number):
    asyncio.sleep(1)
    return number**2
```
Then lets assume that we need a couple of values returned by that function. The basic asynchronous way would be:
```python
import asyncio
from very_important import very_important_function

numbers = [1, 2, 3]
futures = [asyncio.ensure_future(very_important_function(number)) for number in numbers]
asyncio.get_event_loop().run_until_complete(asyncio.gather(futures))
results = [future.result() for future in futures]
print(resutls)
```
Now there is a lot of things that are going on, and writing all that in your simple script will make it quite less simple. Now here is how it looks using omens:
```python
from omens import AsyncioOmen
from very_important import very_important_function

numbers = [1, 2, 3]
results = [AsyncioOmen(very_important_function(number)) for number in numbers]
print(results)
```
Now that looks a lot better! By wrapping our asynchronous function in omen we avoided all the complicated parts of our script, while still getting the asynchonous speed.

When you wrap awaitable function in omen, it will behave like the return value of that function:
When you first wrap it, it creates a future object, and when you try to interact with omen object for the first time (expecting to interact with returned value), omen awaits created future. When said future is complete, omen forwards all incoming calls to the result of the future object.

Note that despite being this awesome, omens are essentially a quite leaky abstraction that shouldn't be used in serious projects. In my opinion, though, they can be useful in short scripts we often write for some tasks.
