#!/usr/bin/env python

import os

from savage import moxie
from savage import utils
from savage.command import template
from savage.command.utils import job
from savage.utils import config as utils_config


def cfg_dir(*args):
    return utils.path('etc', 'ganglia', *args)


_TEMPLATE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))

def template_path(*args):
    return os.path.join(_TEMPLATE_DIR, *args)


class GangliaTask(moxie.Task):

    DEPENDS = ['group:basic', 'group:firewall-conf', 'group:hosts']
    GROUPS = ['janglia']
    VERSION = 1
    SCHEMA = {
        "floating_ip": {"type": "string", "format": "ipv4"},
        "interface":   {"$ref": "piston://#interface"},
        "ganglia_port":{"$ref": "piston://#port-int"},
        "ganglia_host":{"type": "string"}
    }


    def initialize(self, cluster_conf):
        self.receive_host = cluster_conf.get('janglia', {}).get('receive_host', '127.0.0.1')
        self.ganglia_port = cluster_conf.get('janglia', {}).get('ganglia_port', 8649)
        self.cluster_name = cluster_conf.get('janglia', {}).get('cluster_name', "Piston OpenStack Cluster")
        self.depends.stamp_as_service(self, self.ganglia_port)

    def migrate_0_to_1(self):
	    self.ganglia_port = 8649
	    self.receive_host = '127.0.0.1'
	    self.cluster_name = "Piston OpenStack Cluster"
        self.depends.stamp_as_service(self, self.ganglia_port)

    def configure(self, bootflags, **_kw):
        self.logger.debug('Running configuration phase during %s', bootflags)
        GangliaJob(task=self).configure()

    def start(self, bootflags, **_kw):
        self.logger.debug('Running start phase during %s', bootflags)
        GangliaJob(task=self).restart()

    def finalize(self, bootflags, **_kw):
        self.logger.debug('Running finalize phase during %s', bootflags)


class GmondConfig(utils_config.GenericConfig):

    __output__ = cfg_dir('gmond.conf')  # Final location. Must be specified.
    #__owner__  = 'root'       # default is root
    #__group__  = 'root'       # default is root
    #__dir_owner_ = 'root'     # default is __owner__
    #__dir_group_ = 'root' # default is __group__

    # Finally, the umasks for the file and containing directory. The defaults
    # for these are special; if the group is root, the default umask is 077,
    # otherwise the umask is 0027
    #__umask__     = 0027
    #__dir_umask__ = 0027

    def build(self):
        data = {
            "cluster_name": self.task.cluster_name,
            "receive_host": self.task.receive_host,
            "ganglia_port": self.task.ganglia_port,
        }
        return template.build_template(template_path('gmond.conf.template'), data)


class GangliaJob(job.BaseUpstartJob):
    __jobfile__ = 'ganglia.conf'
    __template__ = template_path('ganglia-upstart.template')
    __config__ = (GmondConfig,)

    def build_context(self):
        data = super(GangliaJob, self).build_context()
        data['config_file'] = GmondConfig.__output__
        return data
