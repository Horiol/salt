'''
Module for returning various status data about a minion. These data can be useful for compiling into stats later.
'''
import subprocess

def uptime():
    '''
    Return the uptime for this minion

    CLI Example:
    salt '*' status.uptime
    '''
    return subprocess.Popen(['uptime'],
            stdout=subprocess.PIPE).communicate()[0].strip()

def loadavg():
    '''
    Return the load averages for this minion

    CLI Example:
    salt '*' status.loadavg
    '''
    comps = open('/proc/loadavg', 'r').read().strip()
    loadavg = comps.split()
    return { 
        '1-min':  loadavg[1],
        '5-min':  loadavg[2],
        '15-min': loadavg[3],
    }

def cpustats():
    '''
    Return the CPU stats for this minon

    CLI Example:
    salt '*' status.cpustats
    '''
    stats = open('/proc/stat', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        if comps[0] == 'cpu':
            ret[comps[0]] = {
                'user':    comps[1],
                'nice':    comps[2],
                'system':  comps[3],
                'idle':    comps[4],
                'iowait':  comps[5],
                'irq':     comps[6],
                'softirq': comps[7],
                'steal':   comps[8],
            }
        elif comps[0] == 'intr':
            ret[comps[0]] = {
                'total': comps[1],
                'irqs' : comps[2:],
            }
        elif comps[0] == 'softirq':
            ret[comps[0]] = {
                'total':    comps[1],
                'softirqs': comps[2:],
            }
        else:
            ret[comps[0]] = comps[1]
    return ret

def meminfo():
    '''
    Return the CPU stats for this minon

    CLI Example:
    salt '*' status.meminfo
    '''
    stats = open('/proc/meminfo', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        comps[0] = comps[0].replace(':', '')
        ret[comps[0]] = {
            'value':    comps[1],
        }
        if len(comps) > 2:
            ret[comps[0]]['unit'] = comps[2]
    return ret

def cpuinfo():
    ''' 
    Return the CPU info for this minon

    CLI Example:
    salt '*' status.cpuinfo
    '''
    stats = open('/proc/cpuinfo', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split(':')
        comps[0] = comps[0].strip()
        if comps[0] == 'flags':
            ret[comps[0]] = comps[1].split()
        else:
            comps[1] = comps[1].strip()
            ret[comps[0]] = comps[1]
    return ret 

def diskstats():
    '''
    Return the disk stats for this minon

    CLI Example:
    salt '*' status.diskstats
    '''
    stats = open('/proc/diskstats', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        ret[comps[2]] = {
            'major':                   comps[0],
            'minor':                   comps[1],
            'device':                  comps[2],
            'reads_issued':            comps[3],
            'reads_merged':            comps[4],
            'sectors_read':            comps[5],
            'ms_spent_reading':        comps[6],
            'writes_completed':        comps[7],
            'writes_merged':           comps[8],
            'sectors_written':         comps[9],
            'ms_spent_writing':        comps[10],
            'io_in_progress':          comps[11],
            'ms_spent_in_io':          comps[12],
            'weighted_ms_spent_in_io': comps[13],
        }
    return ret

def vmstats():
    '''
    Return the virtual memory stats for this minon

    CLI Example:
    salt '*' status.vmstats
    '''
    stats = open('/proc/vmstat', 'r').read().split('\n')
    ret = {}
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        ret[comps[0]] = comps[1]
    return ret

def netstats():
    ''' 
    Return the network stats for this minon

    CLI Example:
    salt '*' status.netstats
    '''
    stats = open('/proc/net/netstat', 'r').read().split('\n')
    ret = {}
    headers = ['']
    for line in stats:
        if not line.count(' '):
            continue
        comps = line.split()
        if comps[0] == headers[0]:
            index = len(headers) - 1 
            row = {}
            for field in range(index):
                if field < 1:
                    continue
                else:
                    row[headers[field]] = comps[field]
            rowname = headers[0].replace(':', '') 
            ret[rowname] = row 
        else:
            headers = comps
    return ret 

def w():
    ''' 
    Return a list of logged in users for this minon, using the w command

    CLI Example:
    salt '*' status.w
    '''
    users = subprocess.Popen(['w -h'],
            shell=True,
            stdout=subprocess.PIPE).communicate()[0].split('\n')
    user_list = []
    for row in users:
        if not row.count(' '):
            continue
        comps = row.split()
        print comps
        rec = { 
            'user':  comps[0],
            'tty':   comps[1],
            'login': comps[2],
            'idle':  comps[3],
            'jcpu':  comps[4],
            'pcpu':  comps[5],
            'what':  ' '.join(comps[6:]),
        }   
        user_list.append( rec )
    return user_list

def all():
    '''
    Return a composite of all status data and info for this minon. Warning: There is a LOT here!

    CLI Example:
    salt '*' status.all
    '''
    return {
        'cpuinfo':   cpuinfo(),
        'cpustats':  cpustats(),
        'diskstats': diskstats(),
        'loadavg':   loadavg(),
        'meminfo':   meminfo(),
        'netstats':  netstats(),
        'uptime':    uptime(),
        'vmstats':   vmstats(),
        'w':         w(),
    }

