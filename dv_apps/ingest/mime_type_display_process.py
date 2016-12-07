from mime_type_display import file_type_info

class FileInfo(object):

    def __init__(self, info):
        # get mimetype and name
        self.mimetype, self.name = info

        # set mimetype to lowercase
        self.mimetype = self.mimetype.lower()

        self.dv_classes = []

    def __str__(self):
        return '%s (%s)' % (self.name, self.mimetype)

    def is_class_image(self):

        if self.mimetype.startswith('image/'):
            return True

        if self.mimetype == 'image/fits':
            return True

        return False

    def is_class_astro(self):

        if self.mimetype in ['image/fits', 'application/fits']:
            return True
        return False

    def is_class_audio(self):

        if self.mimetype.startswith('audio/'):
            return True
        return False

    def is_class_code(self):
        """The following are the "control card/syntax" formats
        that we recognize as "code"
        """
        code_syntaxes = ["application/x-r-syntax", "text/x-stata-syntax",
                "text/x-spss-syntax", "text/x-sas-syntax"]
        if self.mimetype in code_syntaxes:
            return True
        return False


def add_more_info(ftype_info):

    for info in ftype_info:
        finfo = FileInfo(info)
        print finfo




if __name__=='__main__':
    add_more_info(file_type_info)
