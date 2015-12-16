'''
Abstract base class for subcommands that output to a file (or stdout).
'''
from __future__ import absolute_import

from abc import abstractmethod
import io

from bokeh.util.string import decode_utf8

from ..subcommand import Subcommand
from ..util import build_single_handler_applications

class FileOutputSubcommand(Subcommand):
    ''' Abstract subcommand to output applications as some type of file.

    '''

    extension = None # subtype must set this to file extension

    @classmethod
    def files_arg(cls, output_type_name):
        """ Subtypes must use this to make a files arg and include it in their args. """
        return ('files', dict(
            metavar='DIRECTORY-OR-SCRIPT',
            nargs='+',
            help=("The app directories or scripts to generate %s for" % (output_type_name)),
            default=None
        ))

    def filename_from_route(self, route, ext):
        if route == "/":
            base = "index"
        else:
            base = route[1:]

        return "%s.%s" % (base, ext)

    def invoke(self, args):
        applications = build_single_handler_applications(args.files)

        for (route, app) in applications.items():
            doc = app.create_document()

            filename = self.filename_from_route(route, self.extension)

            self.write_file(args, filename, doc)

    def write_file(self, args, filename, doc):
        contents = self.file_contents(args, doc)
        with io.open(filename, "w", encoding="utf-8") as file:
            file.write(decode_utf8(contents))
        self.after_write_file(args, filename, doc)

    # can be overridden optionally
    def after_write_file(self, args, filename, doc):
        pass

    @abstractmethod
    def file_contents(self, args, doc):
        """ Subtypes must override this to return the contents of the output file for the given doc."""
        raise NotImplementedError("file_contents")
