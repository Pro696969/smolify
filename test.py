from redis import Sentinel
# sentinel = Sentinel([('sentinel-0', 5000),('sentinel-1', 5000),('sentinel-2', 5000)], socket_timeout=0.1)
sentinel = Sentinel([('172.18.0.5', 5000), ('172.18.0.6', 5000), ('172.18.0.7', 5000)], socket_timeout=0.1)
master = sentinel.discover_master('mymaster')
slave = sentinel.discover_slaves('mymaster')

print(f"Master: {master}")
print(f"Slave: {slave}")

master = sentinel.master_for('mymaster',password = "admin", socket_timeout=0.1)
slave = sentinel.slave_for('mymaster',password = "admin", socket_timeout=0.1)

master.set('foo', 'bar')
slave.get('foo')
