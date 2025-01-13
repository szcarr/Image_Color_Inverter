<h1>Images</h1>
<p>
<b>alternate.py is a small file that can:</b><br
<ul>
    <li>Invert image/images color.</li>
    <li>Flip image/images both vertically and horizontally</li>
    <li>Mirrors image/images both vertically and horizontally</li>
</ul>
<br>
User <b>must</b> specify the arg <code>--source</code>, everything else is optional.<br>
User can combine different parameters.
</p>

<h2>--source</h2>
<p>
Specifies the target image or the directory with images to perform operations on. Please use absolute path.
  
> python3 alternate.py --source image.jpg<br>
> python3 alternate.py --source some/dir/with/images/
</p>

<h2>--save-location</h2>
<p>
Specifies the directory to save the images that have been processed. Please use absolute path.
By default the path is <code>./saved/runs(Number)</code>.

> python3 alternate.py --source some/dir/with/images/ --save-location the/directory/to/save/images/
</p>

<h2>--invert-color</h2>
<p>
Inverts the colors of the specified images from <code>--source</code>.

> python3 alternate.py --source some/dir/with/images/ --invert-color True
</p>

<h2>--flip-horizontally</h2>
<p>
Flips image/images horizontally:

> python3 alternate.py --source some/dir/with/images/ --flip-horizontally True
</p>

<h2>--flip-vertically</h2>
<p>
Flips image/images vertically:

> python3 alternate.py --source some/dir/with/images/ --flip-vertically True
</p>

<h2>--mirror-horizontally</h2>
<p>
Mirrors image/images horizontally:

> python3 alternate.py --source some/dir/with/images/ --mirror-horizontally True
</p>

<h2>--mirror-vertically</h2>
<p>
Mirrors image/images vertically:

> python3 alternate.py --source some/dir/with/images/ --mirror-vertically True
</p>

<h2>--fill-with-color</h2>
<p>
Replaces all pixels with or within the same range as the user specified target_color parameter. User can specify the confidence which can be usefull to negate the negligible pixel differences. User must also specify which color the target_color should be replaced by.

Both the color and the target-color params needs to be specified with hexcode "#FFFFFF"

The example below replaces all white pixels with black pixels
> python3 alternate.py --source some/dir/with/images/ --fill-with-color True --confidence 0.99 --target-color "#FFFFFF" --color "#000000"
</p>
