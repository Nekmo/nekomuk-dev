
class FilterBase(object):
    def __init__(self, xml):
        self.xml = xml
        self.action = self.xml.attrib['action'] == 'true'
        # path_mode puede ser 'name', 'relative' o 'complete'
        self.path_mode = self.xml.attrib.get('path', 'name')
        self.init()

    def _set_xml_choices(self):
        self.choices = []
        for choice in self.xml.findall('choice'):
            self.choices.append(choice.text)

    def init(self):
        pass

    def match(self, root, path, name, **kwargs):
        self.kwargs = kwargs
        if self.path_mode == 'complete':
            check_path = os.path.join(root, path, name)
        elif self.path_mode == 'relative':
            check_path = os.path.join(path, name)
        elif self.path_mode == 'name':
            check_path = name
        if self.action:
            return bool(self.get_match(check_path, root, path, name))
        else:
            return not bool(self.get_match(check_path, root, path, name))


class EndswithFilter(FilterBase):
    def init(self):
        self._set_xml_choices()

    def get_match(self, check_path, root, path, name):
        for choice in self.choices:
            if check_path.endswith(choice): return True
        return False

class StartswithFilter(FilterBase):
    def init(self):
        self._set_xml_choices()

    def get_match(self, check_path, root, path, name):
        if self.use_path:
            name = os.path.join(path, name)
        for choice in self.choices:
            if check_path.startswith(choice): return True
        return False

class EqualFilter(FilterBase):
    def init(self):
        self._set_xml_choices()

    def get_match(self, check_path, root, path, name):
        return check_path in self.choices

filters = {
    'endswith': EndswithFilter,
    'startswith': StartswithFilter,
    'equal': EqualFilter,
}

class GroupFilter(object):
    def __init__(self, xml, **kwargs):
        self.action = xml.attrib['action']
        self.childrens = []
        for children in xml.getchildren():
            if children.tag == 'filter':
                self.childrens.append(filters[children.attrib['type']](children))
            elif children.tag == 'group':
                self.childrens.append(GroupFilter(children))
            elif children.tag == 'globalfilters':
                if children.attrib['type'] == 'dirs':
                    self.children.append(kwargs['synctree'].dirsfilter)
                elif children.attrib['type'] == 'files':
                    self.children.append(kwargs['synctree'].filesfilter)


    def match(self, root, path, name):
        match_childrens = []
        for children in self.childrens:
            match_childrens.append(children.match(root, path, name))
        if self.action == 'or' and True in match_childrens:
            return True
        elif self.action == 'and' and not False in match_childrens:
            return True
        elif self.action == 'not' and len(match_childrens) > 1:
            raise Exception('Invalid not group in configuration')
        elif self.action == 'not':
            return not match_childrens[0]
        else:
            return False


class Filters(object):
    filter = None
    def __init__(self, xml, **kwargs):
        if not xml:
            return
        xml = xml[0]
        if xml.tag == 'filter':
            self.filter = filters[xml.attrib['type']](xml)
        elif xml.tag == 'group':
            self.filter = GroupFilter(xml, **kwargs)

    def match(self, root, path, name):
        if not self.filter:
            return True
        return self.filter.match(root, path, name)