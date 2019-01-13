class FilterModule(object):
    def filters(self):
        return {
            'activemq_camelcase': self.rename_camelcase,
            'read_camelcase': self.read_camelcase,
            'write_camelcase': self.write_camelcase,
            'admin_camelcase': self.admin_camelcase,
            'combine_listmap': self.combine_listmap,
            'activemq_options': self.activemq_options
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

    def combine_listmap(self, default, configuration):
        updated = []
        for conf in default:
            nconf = next((item for item in configuration if item['protocol'] == conf["protocol"]), None)
            z = conf.copy()
            if nconf:
               z.update(nconf)
            updated.append(z)
        return updated

    def activemq_options(self, options):
        return '&amp;'.join([ "=".join([str(y) for y in x]) for x in options.items()])
