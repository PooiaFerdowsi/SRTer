SRT files delay calculator
==========================
This simple program requires [1](#info):
1. File (subtitle) to read data from
2. File (subtitle) to write data to
3. Delay (can be either negative or positive)

The program *adds* the value you gave it as delay to
the timecodes of all frames of the subtitle in millisecond.

There's no problem with values more than 999, because
the program will automatically adjust timecodes. [2](#timecode_corrector)


Use
----
### usage notes
* Ensure that you always have one and only one blankline between frames
* Ensure that the first line of the file is frame number
* Ensure that last frame has at least two blanklines after its caption

### usage guide
If you want to use this program:
* Ensure python is installed
* Do any of following:
	* Double click on the file
	* `py $filename.py`
	* `python3 $filename.py`
	* Defer to WWW if these didn't sufficed
* Fill the requested question with your desired values
	* First and second argument require file path and the
	the one requires an integer value
* You nailed it!

Please issue if it doesn't work. TNX


CUSTOMIZATION
--------------
Feel free to change `getInfo()`:
	It's only duty is to assign a value to
	`FROM`, `TO` and `OFFSET` variables.
	You can add a GUI with editting this function.

Feel a bit free to change `do(frame)`:
	If you did it, you'd changed the operation
	of the program severely and you'll make
	an average portion of the program useless.
	It's useful if you have other expectations
	of the program than just Calculating Delays.


LICENSE
-------
Usage is divided by two categories:

NOTE: *in all conditions except Partial non-commercial
Author name and email must be mentioned*
* Partial: a small amount of the code
	* non-commercial use: It's free to use.
	* commercial use: Just [email][1] me

* Total: a large amount or the complete code
	* non-commercial use: Just [email][1] me.
	* commercial use: [email][1] me and await my allowance.

TODO
------
- [ ] Raise different Exceptions for different situations
(Program raise `Exception` for all kind of Exceptions)
- [ ] Write `hh:mm:ss,[0-9]{1,3}` instead of `h:m:s,ms`
- [ ] Microsecond acts (and stands) for millisecond (micro = milli!)

Mechanisms
----------
If you want to get the hang of this program, then
		**Heres for you!**

### info
`getInfo()` provides the program with the three required info.
* `FROM`: File (subtitle) to read data from
* `TO`: File (subtitle) to write data to
* `OFFSET`: Delay (can be either negative or positive)

### main `for` loop
The only `for` loop in the program do half the work:
It parses the `.srt` files to a dictionary! See:
pure SRT file:
```SRT
1
00:00:00,000 --> 00:00:02:355
Hello World! It's SRT

```
After the `for` loop parsed it:
```py
{'frame': 1,
timecodes: (datetime.time(0, 0, 0, 0), datetime.time(0, 0, 2, 355)),
caption: "Hello World! It's SRT"
}
```
The dictionary is stored in the `frame` variable wich change
every time the loop loops.

### Dew it!
the `do(frame)` function do the work. Whatever it be!
In this case it use the `time_sum(tm, offset)` function
to calculate and apply the offset, so remove the delay.

Meanwhile after the function returned its value
the `for` loop writes (or appends) the result
of the `do`function to the specified file (`TO`)

#### timecode_corrector
What happens if the timecode be `00:00:02,600` and
we want to add `450`ms to it? will it become the right
one (`00:00:03,050`) or be incorrect (`00:00:02,1050`)?

This program adjust for this problem. However it *do not*
use the same solution as you use when solving 2,3... digit
math sums! instead it use the following solution wich reduce
program boiler-plate:
* the program converts `hh:mm:ss,ms` to pure millisecond
	* `ms + ((h * 60 + m) * 60 + s) * 1000`
* after the calculation is done,
 the program converts the result to `hh:mm:ss,ms` form

 The main cause for this solution is to reduce boiler-plate


[1]: mailto:pooia.ferdowsi.is.developer@gmail.com
