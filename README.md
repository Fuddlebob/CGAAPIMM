# CGAAPIMM
The Community Guided Abstract Art / Post-Ironic Meme Machine is a Facebook bot that applies filters and/or transforms to an image sequentially based off reactions on Facebook. The results can be found on Facebook at: https://www.facebook.com/Community-Guided-Abstract-Art-Post-Ironic-Meme-Machine-107375434280777/

## Transforms
The transform system is designed so that new filters/transforms can be created and added with as little hassle as possible. Each transform exists in a single, self-contained file, which will be automatically imported when added to the transform folder.

A transform should inherit from the Abstract Transform base class, and implement the methods contained therein. The ConcreteTransform class exists to serve as an example, and can be copied and edited to create a new transform.

The required methods are briefly explained in the comments of the ConcreteTransform class, but I shall go over them here:

### name()
Returns the name of the transform as a string. This should be relatively short, and be unique from all other transforms.

### description()
Returns a longer description of what the transform actually does. This, along with the name, is shown on Facebook so users have an idea of what the Transform will do.

### transform(image)
This is the function that actualy transforms the image. Takes in an openCV2 image (the image to transform) and transforms it, returning the new image. This design is so that multiple transforms can be strung together, without losing performance by constantly saving and opening images.
