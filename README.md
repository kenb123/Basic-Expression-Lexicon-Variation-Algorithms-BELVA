OWASP Basic Expression & Lexicon Variation Algorithms (BELVA)
==

Contents
--
1. Dedication
2. Information / Resources
3. Running pyOwaspBELVA
4. Known Issues
5. To Do


1. Dedication
--

This app is dedicated to my dad. 

Please see DEDICATION file for more info.


2. Information / Resources
--

Find general info and FAQ on owasp.org project page:
https://www.owasp.org/index.php/OWASP_Basic_Expression_&_Lexicon_Variation_Algorithms_%28BELVA%29_Project

How to & videos to come.....


3. Running pyOwaspBELVA
--

To Run:

1. Download zip from git
2. Unzip downloaded file into folder
3. Open command prompt and change directories into unzipped folder
4. Type ./pyOwaspBELVA.py and hit ENTER


Potential issues
--

To make the py files executable you *may* need to type:

	chmod 755 ./*.py -R 


Follow py instructions to install additional libraries 
	such as QT4 if needed


4. Known Issues
--

The interface needs better responsiveness: it can be sluggish and may appear unresponsive. 

To verify app is working:

Change to outFile/outfile.txt directory (or your selected outfile directory) and type:

	tail -f outfile.txt

You will see new dictionary words being generated if past the import stage.


5. To Do
--

1. Word selection / automated weighing of which words to use
2. Interface improvements: better responsiveness
3. Non-GUI version that directs output to stdout
4. Expand functionality and add more plug-ins
	- Additional permutation dictionaries
	- Additional applied and removal policies
	- Additional username creation policies
5. Other types of permutations in addition to just usernames and passwords (i.e., email addresses, sub-domain names)


Developed on Linux and not tested on other platforms so Windows/OSX mileage may vary (as of 2016 March 29)
--
