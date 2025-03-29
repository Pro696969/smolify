from redis import Sentinel
sentinel = Sentinel([('sentinel-0', 5000), ('sentinel-1', 5000), ('sentinel-2', 5000)], socket_timeout=0.1)
sentinel.discover_master('mymaster')
sentinel.discover_slaves('mymaster')
