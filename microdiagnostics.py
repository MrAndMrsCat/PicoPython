import gc
import os

class MicroDiagnostics(object):
    def df():
      s = os.statvfs('//')
      return f'{(s[0]*s[3])/1048576:0.3f} MB'

    def free(detailed=False):
      free = gc.mem_free() / 1024
      allocated = gc.mem_alloc() / 1024
      total = free+allocated
      percent = '{0:.1f}%'.format(free/total*100)

      return f"{free:.0f}/{total:.0f}kB ({percent})" if detailed else percent
  