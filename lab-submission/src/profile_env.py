import argparse, json, os, platform, sys, re
from pathlib import Path
from salt import get_student_params
ROOT=Path(__file__).resolve().parents[1]
def cpuinfo():
    try:return Path('/proc/cpuinfo').read_text()
    except OSError:return ''
def cache_linux():
    out={}
    base=Path('/sys/devices/system/cpu/cpu0/cache')
    for folder in sorted(base.glob('index*')):
        try:
            level=(folder/'level').read_text().strip(); typ=(folder/'type').read_text().strip()
            size=(folder/'size').read_text().strip(); line=int((folder/'coherency_line_size').read_text().strip())
            name=f'L{level}' + ('D' if typ=='Data' else ('I' if typ=='Instruction' else ''))
            out[name]={'size':size,'line_bytes':line}
        except (OSError,ValueError):continue
    return out

def profile(student_id):
    info=cpuinfo(); model=next((x.split(':',1)[1].strip() for x in info.splitlines() if x.startswith('model name')),platform.processor() or 'Unknown')
    mhz=next((x.split(':',1)[1].strip() for x in info.splitlines() if x.startswith('cpu MHz')),None)
    try:import psutil; physical=psutil.cpu_count(logical=False)
    except ImportError:physical=None
    if physical is None and info:
        sockets=set(); pairs=set(); phys=None
        for block in info.split('\n\n'):
            d=dict((k.strip(),v.strip()) for line in block.splitlines() if ':' in line for k,v in [line.split(':',1)])
            if 'physical id' in d and 'core id' in d:pairs.add((d['physical id'],d['core id']))
            if 'cpu cores' in d:phys=int(d['cpu cores'])
            if 'physical id' in d:sockets.add(d['physical id'])
        physical=len(pairs) if pairs else ((len(sockets) or 1)*phys if phys else None)
    return {'student_id':student_id,'cpu_model':model,'microarchitecture':'Not reliably detectable with Python standard library','reported_cpu_mhz':mhz,'physical_cores':physical,'logical_threads':os.cpu_count(),'smt_present':(os.cpu_count()>physical) if physical else None,'cache':cache_linux(),'cache_line_bytes':next((x['line_bytes'] for x in cache_linux().values()),None),'os':platform.platform(),'kernel':platform.release(),'python':sys.version,'implementation':platform.python_implementation()}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--student-id',default='230103161');args=ap.parse_args()
    (ROOT/'results').mkdir(exist_ok=True)
    for name,record in [('host_profile.json',profile(args.student_id)),('salted_params.json',get_student_params(args.student_id))]:
        (ROOT/'results'/name).write_text(json.dumps(record,indent=2)+'\n')
        print('Saved results/'+name)
