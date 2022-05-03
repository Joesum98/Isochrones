There are some issues with the installation instructions on the SPISEA docs 
(https://spisea.readthedocs.io/en/latest/getting_started.html)

Start by pip installing SPISEA through git with the command

    python -m pip install git+https://github.com/astropy/SPISEA   

Then create a folder called "cdbs" somewhere on your system.
The subfolders should be set up as follows

    <your_location>/cdbs/grp/redcat/trds

with nothing else necessary in any of the sub-folders.

Go to this link for the Stellar Evolution and Atmosphere Models

    https://w.astro.berkeley.edu/~jlu/spisea/

Dowload
    spisea_models.tar.gz   
            & 
    spisea_cdbs.tar.gz    

Un-tar those files inside the trds folder. 

Un-taring might create duplicate folders ("evolution" & "grid"); just combine these.

In the end you should have 4 subfolders in trds
    1.) comp
    2.) evolution
    3.) grid
    4.) mtab


You will also need to set your path to the models you downloaded by editing your .bash_profile with
    
    export PYSYN_CDBS=/<path_to_cdbs_directory>
    export SPISEA_MODELS=/<path_to_models_directory>

However, I could not get this this to work so at the top of my code I added

    import os
    os.environ["PYSYN_CDBS"] = "<my_path>/cdbs/grp/redcat/trds"
    os.environ['SPISEA_MODELS'] = "<my_path>/cdbs/grp/redcat/trds" 
    

With this all set up and pip installed, SPISEA should work now!


