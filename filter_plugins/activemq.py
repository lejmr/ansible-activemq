class FilterModule(object):
    def filters(self):
        return {
            'activemq_camelcase': self.rename_camelcase,
            'read_camelcase': self.read_camelcase,
            'write_camelcase': self.write_camelcase,
            'admin_camelcase': self.admin_camelcase,
        }

    def rename_camelcase(self, tpl):
        read, write, admin, groups = tpl
        others = [x for x in read if '.' not in x]
        others += [x for x in write if '.' not in x]
        others += [x for x in admin if '.' not in x]
        others += groups
        tq = [ "{}.Read".format(x) for x in read if '.' in x]
        tq += [ "{}.Write".format(x) for x in write if '.' in x]
        tq += [ "{}.Admin".format(x) for x in admin if '.' in x]
        return set(others + [ ''.join(x.capitalize() or '.' for x in word.split('.')) for word in tq])

    def xxx_camelcase(self, q, state="Read"):
        nq = "{}.{}".format(q,state)
        return ''.join(x.capitalize() or '.' for x in nq.split('.'))

    def read_camelcase(self, q):
        return self.xxx_camelcase(q, "Read")

    def write_camelcase(self, q):
        return self.xxx_camelcase(q, "Write")

    def admin_camelcase(self, q):
        return self.xxx_camelcase(q, "Admin")
