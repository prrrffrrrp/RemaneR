
    # !RemaneR
    ========

    ###### ! RemaneR is a cli program to rename files using a list of names supplied
    in a separated file.

    =========================================================================
    ### Usage:

    The user have two options:

    Type --> **python main.py -i** 

    This option starts the program in interactive mode. The user is prompted to
    enter the path to the files to be renamed and the path of the file 
    containing the names that he wants to use to rename the current files.
    Then a text menu is shown with many different option choices.
    
    or
    
    Type --> **python main.py /path/to/files_to_be_renamed /path/to/filename -r**

    This will automatically rename the files without entering the interactive
    menu.

    At this point the main dependency of !RemaneR is the Textract module.
    !RemaneR will accept any file extension supported by Textract as a source
    of new names but only .txt, .docx, .odt and .xlsx extensions have been 
    tested. 
    In addition to work properly, the names in the list of names contained by
    the file, should be either comma separated or separated by a new line 
    character.
    The .xlsx files should contain only one column with names,
    to work properly.

    ==========================================================================
    ### Work in progress:
    
    Because the it can be trycky to install the textract module and because it
    does way more than it is strictly necessary in !RemaneR, I'm working in a
    version that will be textract free.
    You can find it in the *nodependency* branch.
    Right now this version only accepts .docx, .txt and .csv files (with only
    one row of data).
    
    
