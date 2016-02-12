# This is used to create the interpreter as a singleton object.
# Use this to import the interpreter to ensure you get the same module instance
# as the other files
try:
    from ExpandRegion.minterp import interpreter
except:
    # different folder name or test cases
    print(
        "Warning: Rename the folder of ExpandRegion to ExpandRegion.\n"
        "Otherwise editing files requires a restart of Sublime Text"
        "for the changes to be propagated."
    )
    try:
        from minterp import interpreter
    except:
        from .minterp import interpreter
