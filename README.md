janglia
-------

A moxie package for ganglia to run in Piston OpenStack environments.
These options (or similar) should be added to cloud.conf:

```
[janglia]
receive_host=127.0.0.1
ganglia_port=8649
```

This will run gmond on every host, and master elect a single gmetad server.
TODO(JMC): gmetad servers as an Agent
