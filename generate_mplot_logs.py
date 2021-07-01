#!/usr/local/bin/python3
"""
generate_mplot_logs.py logfile

Usage:
    generate_mplot_logs.py [options]

Options:
    -h --help           Show this text.
    --log <mongodb log> MongoDB log to convert
"""

import json
import re
from docopt import docopt

def convert_log_line(logfile):
    log = open(logfile, 'r') 

    # count = 0
    for line in log.readlines():
        # count = count + 1
        # print("line:{}".format(count))
        try:
            obj = json.loads(line)
        except Exception:
            continue
        c = obj["c"]
        dt = obj['t']['$date']
        dt = re.sub('(\+\d\d):(\d\d)$',r'\1\2', dt)
        s = obj['s']
        ctx = obj['ctx']
        attr = []
        if 'msg' in obj and obj['msg'] != 'Slow query':
            if obj['msg'] == 'Connection ended':
                attr.append('end connection')
            elif obj['msg'] == 'Connection accepted':
                attr.append('connection accepted')
            elif obj['msg'] == 'Authentication succeeded':
                attr.append('Successfully authenticated')
            else:
                attr.append(obj['msg'])
        if c == 'CONTROL' and 'attr' in obj and 'host' in obj['attr']:
            pid = obj['attr']['pid']
            port = obj['attr']['port']
            arch = obj['attr']['architecture']
            host = obj['attr']['host']
            attr.pop()
            attr.append("pid={} port={} {} host={}".format(pid, port, arch, host))
        elif c == 'ACCESS':
            if 'attr' in obj:
                for key in obj['attr']:
                    if key == 'principalName':
                        attr.append('as principal ' + str(obj['attr'][key]))
                    elif key == 'authenticationDatabase':
                        attr.append('on ' + obj['attr'][key])
                    elif key == 'remote':
                        attr.append('from client '+str(obj['attr'][key]))
        elif c == 'NETWORK':
            if 'attr' in obj:
                for key in obj['attr']:
                    if key == 'remote':
                        if obj['msg'] == 'Connection ended':
                            attr.append(obj['attr'][key])
                        else:
                            attr.append('from '+obj['attr'][key])
                    elif key == 'connectionId' and obj['msg'] != 'Connection ended':
                        attr.append('#'+str(obj['attr'][key]))
                    elif key == 'client':
                        attr.append(obj['attr'][key]+':')
                    elif key == 'doc':
                        attr.append(json.dumps(obj['attr'][key]))
                    elif key == 'connectionCount':
                        attr.append('('+str(obj['attr'][key])+ ' connections now open)')
        elif c == 'COMMAND' or c == 'WRITE' or c == 'QUERY':
            if 'attr' in obj:
                for key in obj['attr']:
                    if key == 'type' or key == 'ns':
                        attr.append(obj['attr'][key])
                    elif key == 'command':
                        command = ''
                        cmd = ''
                        ctr = 0
                        for key in obj['attr']['command']:
                            ctr = ctr + 1
                            if ctr > 1:
                                command = command + ', '
                            else:
                                cmd = 'command: ' + key
                            command = command + key + ': ' + json.dumps(obj['attr']['command'][key])
                        command = '{ ' + command + ' }'
                        # cmd = 'command: ' + list(obj['attr']['command'].keys())[0]
                        attr.append(cmd)
                        attr.append(command)
                    elif key == 'durationMillis':
                        attr.append(str(obj['attr'][key]) + 'ms')
                    else:
                        attr.append(key + ':' + json.dumps(obj['attr'][key]))
        else:
            continue
        attrstr = ' '.join(attr)
        print("{} {} {}  [{}] {}".format(dt, s, c, ctx, attrstr))

def main():
    opts = docopt(__doc__)
    logfile = opts['--log']
    convert_log_line(logfile)

if __name__ == '__main__':
    main()
